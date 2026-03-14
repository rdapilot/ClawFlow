from clawflow.api.app import RunRequest, run_pipeline, status


def test_status_endpoint() -> None:
    payload = status()
    assert payload["adapter"] == "mock-openclaw"
    assert payload["connected"] is True
    assert "monitoring" in payload


def test_run_pipeline_endpoint() -> None:
    payload = run_pipeline(RunRequest(prompt="launch a product campaign"))
    assert payload["status"] == "completed"
    assert payload["task_count"] == 6
