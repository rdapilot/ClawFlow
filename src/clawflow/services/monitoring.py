from __future__ import annotations

from dataclasses import asdict, dataclass, field

from clawflow.domain.models import PipelineRun, TaskResult, TaskStatus


@dataclass(slots=True)
class MonitoringSnapshot:
    pipelines_run: int = 0
    task_successes: int = 0
    task_failures: int = 0
    average_latency_ms: float = 0.0
    last_pipeline_status: str = TaskStatus.pending.value


@dataclass(slots=True)
class MonitoringService:
    snapshot: MonitoringSnapshot = field(default_factory=MonitoringSnapshot)

    def bootstrap(self, pipelines: list[PipelineRun]) -> None:
        self.snapshot = MonitoringSnapshot()
        for pipeline in reversed(pipelines):
            self.record_pipeline(pipeline)

    def record_pipeline(self, pipeline: PipelineRun) -> None:
        self.snapshot.pipelines_run += 1
        self.snapshot.last_pipeline_status = pipeline.status.value
        latencies = [result.latency_ms for result in pipeline.results]
        self.snapshot.task_successes += sum(
            1 for result in pipeline.results if result.status == TaskStatus.completed
        )
        self.snapshot.task_failures += sum(
            1 for result in pipeline.results if result.status == TaskStatus.failed
        )
        if latencies:
            self.snapshot.average_latency_ms = sum(latencies) / len(latencies)

    def summarize_task_results(self, results: list[TaskResult]) -> dict[str, int]:
        return {
            "completed": sum(1 for result in results if result.status == TaskStatus.completed),
            "failed": sum(1 for result in results if result.status == TaskStatus.failed),
        }

    def as_dict(self) -> dict[str, int | float | str]:
        return asdict(self.snapshot)
