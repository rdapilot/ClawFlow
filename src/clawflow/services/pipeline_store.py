from __future__ import annotations

from dataclasses import dataclass, field

from clawflow.domain.models import PipelineRun


@dataclass(slots=True)
class InMemoryPipelineStore:
    pipelines: list[PipelineRun] = field(default_factory=list)

    def save(self, pipeline: PipelineRun) -> PipelineRun:
        self.pipelines.append(pipeline)
        return pipeline

    def list(self) -> list[PipelineRun]:
        return list(reversed(self.pipelines))

    def latest(self) -> PipelineRun | None:
        return self.pipelines[-1] if self.pipelines else None

