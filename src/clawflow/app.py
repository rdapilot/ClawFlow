from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from clawflow.adapters.openclaw.mock import MockOpenClawGateway
from clawflow.config import ClawFlowSettings
from clawflow.services.agent_allocator import AgentAllocator
from clawflow.services.intent_engine import IntentEngine
from clawflow.services.monitoring import MonitoringService
from clawflow.services.orchestrator import Orchestrator
from clawflow.services.pipeline_store import JsonPipelineStore
from clawflow.services.scheduler import Scheduler
from clawflow.services.synthesizer import ResultSynthesizer
from clawflow.services.task_decomposer import TaskDecomposer


@dataclass(slots=True)
class ApplicationContext:
    settings: ClawFlowSettings
    orchestrator: Orchestrator
    monitoring: MonitoringService
    store: JsonPipelineStore
    gateway: MockOpenClawGateway


def create_application_context() -> ApplicationContext:
    settings = ClawFlowSettings()
    monitoring = MonitoringService()
    store = JsonPipelineStore(path=Path(".clawflow") / "pipelines.json")
    monitoring.bootstrap(store.list())
    gateway = MockOpenClawGateway()
    orchestrator = Orchestrator(
        gateway=gateway,
        intent_engine=IntentEngine(),
        task_decomposer=TaskDecomposer(),
        agent_allocator=AgentAllocator(),
        scheduler=Scheduler(),
        synthesizer=ResultSynthesizer(),
        monitoring=monitoring,
        store=store,
    )
    return ApplicationContext(
        settings=settings,
        orchestrator=orchestrator,
        monitoring=monitoring,
        store=store,
        gateway=gateway,
    )
