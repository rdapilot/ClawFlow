from __future__ import annotations

import json

import typer

from clawflow.app import create_application_context

app = typer.Typer(help="ClawFlow orchestration CLI.")


def _context():
    return create_application_context()


@app.command("run")
def run(prompt: str) -> None:
    """Execute a prompt through the orchestration pipeline."""
    pipeline = _context().orchestrator.run(prompt)
    typer.echo(json.dumps(
        {
            "id": pipeline.id,
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
        },
        indent=2,
    ))


@app.command()
def activate() -> None:
    """Initialize ClawFlow and verify the configured adapter."""
    activate_entrypoint()


@app.command()
def status() -> None:
    """Report engine and adapter status."""
    context = _context()
    typer.echo(json.dumps(
        {
            "app": context.settings.app_name,
            "adapter": context.settings.adapter_name,
            "connected": context.gateway.connect(),
            "pipelines_run": context.monitoring.snapshot.pipelines_run,
            "latest_pipeline_id": context.store.latest().id if context.store.latest() else None,
        },
        indent=2,
    ))


@app.command()
def pipelines() -> None:
    """List recent pipelines."""
    context = _context()
    typer.echo(json.dumps(
        [
            {
                "id": pipeline.id,
                "status": pipeline.status.value,
                "prompt": pipeline.prompt,
            }
            for pipeline in context.store.list()
        ],
        indent=2,
    ))


def activate_entrypoint() -> None:
    """Initialize ClawFlow and verify the configured adapter."""
    context = _context()
    ready = context.gateway.connect()
    typer.echo(
        json.dumps(
            {
                "activated": True,
                "adapter": context.settings.adapter_name,
                "connected": ready,
                "agents_discovered": len(context.gateway.discover_agents()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    app()
