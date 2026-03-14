from fastapi.testclient import TestClient

from clawflow.api.app import app


client = TestClient(app)


def test_status_endpoint() -> None:
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["adapter"] == "mock-openclaw"
    assert payload["connected"] is True


def test_run_pipeline_endpoint() -> None:
    response = client.post("/api/v1/run", json={"prompt": "launch a product campaign"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["task_count"] == 6
