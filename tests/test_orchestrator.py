from pathlib import Path

from clawflow.app import create_application_context
from clawflow.services.pipeline_store import JsonPipelineStore


def test_orchestrator_runs_pipeline() -> None:
    context = create_application_context()
    pipeline = context.orchestrator.run("launch a social media marketing campaign for a startup")

    assert pipeline.status.value == "completed"
    assert pipeline.intent.domain == "marketing"
    assert len(pipeline.tasks) == 6
    assert all(task.assigned_agent for task in pipeline.tasks)
    assert "Deliverables:" in pipeline.final_output


def test_scheduler_layers_respect_dependencies() -> None:
    context = create_application_context()
    tasks = context.orchestrator.task_decomposer.decompose(
        context.orchestrator.intent_engine.analyze("build a product launch campaign")
    )

    layers = context.orchestrator.scheduler.execution_layers(tasks)
    assert [task.id for task in layers[0]] == ["research"]
    assert sorted(task.id for task in layers[-1]) == ["launch"]


def test_pipeline_store_persists_runs(tmp_path: Path) -> None:
    context = create_application_context()
    context.store = JsonPipelineStore(path=tmp_path / "pipelines.json")
    context.orchestrator.store = context.store

    pipeline = context.orchestrator.run("build a product launch campaign")
    reloaded_store = JsonPipelineStore(path=tmp_path / "pipelines.json")
    reloaded = reloaded_store.latest()

    assert reloaded is not None
    assert reloaded.id == pipeline.id
    assert reloaded.status.value == "completed"
