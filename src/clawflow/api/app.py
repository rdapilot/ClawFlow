from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from clawflow.app import create_application_context

app = FastAPI(title="ClawFlow API", version="0.1.0")
context = create_application_context()


class RunRequest(BaseModel):
    prompt: str


@app.get("/")
def dashboard() -> FileResponse:
    ui_path = Path(__file__).resolve().parent.parent / "ui" / "index.html"
    return FileResponse(ui_path)


@app.get("/api/v1/status")
def status() -> dict[str, object]:
    return {
        "app": context.settings.app_name,
        "adapter": context.settings.adapter_name,
        "connected": context.gateway.connect(),
        "monitoring": context.monitoring.as_dict(),
        "latest_pipeline_id": context.store.latest().id if context.store.latest() else None,
    }


@app.get("/api/v1/pipelines")
def pipelines() -> list[dict[str, object]]:
    items = []
    for pipeline in context.store.list():
        items.append(
            {
                "id": pipeline.id,
                "prompt": pipeline.prompt,
                "status": pipeline.status.value,
                "tasks": [
                    {
                        "id": task.id,
                        "name": task.name,
                        "agent": task.assigned_agent,
                        "dependencies": task.dependencies,
                    }
                    for task in pipeline.tasks
                ],
                "final_output": pipeline.final_output,
            }
        )
    return items


@app.post("/api/v1/run")
def run_pipeline(request: RunRequest) -> dict[str, object]:
    pipeline = context.orchestrator.run(request.prompt)
    return {
        "id": pipeline.id,
        "status": pipeline.status.value,
        "final_output": pipeline.final_output,
        "task_count": len(pipeline.tasks),
    }
