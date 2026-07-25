from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_status():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "db_row_counts" in data
