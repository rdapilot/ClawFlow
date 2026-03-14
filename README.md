# ClawFlow

ClawFlow is a Python-first orchestration layer designed to sit in front of OpenClaw. It accepts a high-level prompt, decomposes it into a task graph, allocates agents, executes the graph, and synthesizes a final result.

This repository is scaffolded from the provided SRS with two priorities:

1. Keep the orchestration core independent from OpenClaw specifics.
2. Make the eventual OpenClaw integration a single adapter swap instead of a rewrite.

## Current scaffold

- `src/clawflow/services`: orchestration pipeline components
- `src/clawflow/adapters/openclaw`: integration boundary and a mock adapter
- `src/clawflow/api`: FastAPI app for status, pipelines, and execution
- `src/clawflow/ui`: lightweight dashboard served by the API
- `tests`: basic orchestration and CLI coverage

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
activate-clawflow
clawflow run "launch a social media marketing campaign for a startup"
uvicorn clawflow.api.app:app --reload
```

## CLI

- `activate-clawflow`: initialize the engine and verify the configured adapter
- `clawflow run "<prompt>"`: run a prompt through the orchestration pipeline
- `clawflow status`: view engine status
- `clawflow pipelines`: inspect recent pipeline runs

## OpenClaw integration plan

The `OpenClawGateway` protocol in `src/clawflow/adapters/openclaw/base.py` is the integration contract. To wire in OpenClaw later, replace the mock gateway with a concrete implementation that:

- discovers agents from the OpenClaw registry
- dispatches task payloads to the OpenClaw execution interface
- collects results, failures, and agent health metrics

The orchestrator and API should not require structural changes once that adapter is implemented.

