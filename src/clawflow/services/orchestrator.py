from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from uuid import uuid4

from clawflow.adapters.openclaw.base import OpenClawGateway
from clawflow.domain.models import PipelineRun, TaskResult, TaskStatus
from clawflow.services.agent_allocator import AgentAllocator
from clawflow.services.intent_engine import IntentEngine
from clawflow.services.monitoring import MonitoringService
from clawflow.services.pipeline_store import JsonPipelineStore
from clawflow.services.scheduler import Scheduler
from clawflow.services.synthesizer import ResultSynthesizer
from clawflow.services.task_decomposer import TaskDecomposer


class Orchestrator:
    def __init__(
        self,
        gateway: OpenClawGateway,
        intent_engine: IntentEngine,
        task_decomposer: TaskDecomposer,
        agent_allocator: AgentAllocator,
        scheduler: Scheduler,
        synthesizer: ResultSynthesizer,
        monitoring: MonitoringService,
        store: JsonPipelineStore,
    ) -> None:
        self.gateway = gateway
        self.intent_engine = intent_engine
        self.task_decomposer = task_decomposer
        self.agent_allocator = agent_allocator
        self.scheduler = scheduler
        self.synthesizer = synthesizer
        self.monitoring = monitoring
        self.store = store

    def run(self, prompt: str) -> PipelineRun:
        intent = self.intent_engine.analyze(prompt)
        tasks = self.task_decomposer.decompose(intent)
        tasks = self.agent_allocator.allocate(tasks, self.gateway.discover_agents())
        layers = self.scheduler.execution_layers(tasks)

        results: list[TaskResult] = []
        for layer in layers:
            with ThreadPoolExecutor(max_workers=len(layer)) as executor:
                layer_results = list(executor.map(self.gateway.execute_task, layer))
            results.extend(layer_results)

        final_output = self.synthesizer.synthesize(intent, results)
        status = (
            TaskStatus.completed
            if all(result.status == TaskStatus.completed for result in results)
            else TaskStatus.failed
        )
        pipeline = PipelineRun(
            id=str(uuid4()),
            prompt=prompt,
            intent=intent,
            tasks=tasks,
            results=results,
            final_output=final_output,
            status=status,
            completed_at=datetime.now(tz=timezone.utc),
        )
        self.store.save(pipeline)
        self.monitoring.record_pipeline(pipeline)
        return pipeline
