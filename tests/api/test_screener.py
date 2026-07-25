from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_screener():
    response = client.get("/screener?min_roe=15")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_invalid_parameter():
    response = client.get("/screener?min_roe=abc")
    assert response.status_code == 400