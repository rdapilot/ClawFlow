from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from clawflow.domain.models import Intent, PipelineRun, TaskNode, TaskResult, TaskStatus


@dataclass(slots=True)
class JsonPipelineStore:
    path: Path

    def save(self, pipeline: PipelineRun) -> PipelineRun:
        pipelines = self._load()
        pipelines.append(self._serialize_pipeline(pipeline))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(pipelines, indent=2), encoding="utf-8")
        return pipeline

    def list(self) -> list[PipelineRun]:
        return [self._deserialize_pipeline(item) for item in reversed(self._load())]

    def latest(self) -> PipelineRun | None:
        pipelines = self._load()
        return self._deserialize_pipeline(pipelines[-1]) if pipelines else None

    def _load(self) -> list[dict[str, object]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _serialize_pipeline(self, pipeline: PipelineRun) -> dict[str, object]:
        payload = asdict(pipeline)
        payload["status"] = pipeline.status.value
        payload["started_at"] = pipeline.started_at.isoformat()
        payload["completed_at"] = pipeline.completed_at.isoformat() if pipeline.completed_at else None
        return payload

    def _deserialize_pipeline(self, payload: dict[str, object]) -> PipelineRun:
        intent_payload = payload["intent"]
        task_payloads = payload["tasks"]
        result_payloads = payload["results"]
        return PipelineRun(
            id=str(payload["id"]),
            prompt=str(payload["prompt"]),
            intent=Intent(**intent_payload),
            tasks=[TaskNode(**task_payload) for task_payload in task_payloads],
            results=[
                TaskResult(
                    **{
                        **result_payload,
                        "status": TaskStatus(result_payload["status"]),
                    }
                )
                for result_payload in result_payloads
            ],
            final_output=str(payload["final_output"]),
            status=TaskStatus(str(payload["status"])),
            started_at=datetime.fromisoformat(str(payload["started_at"])),
            completed_at=(
                datetime.fromisoformat(str(payload["completed_at"]))
                if payload["completed_at"]
                else None
            ),
        )
