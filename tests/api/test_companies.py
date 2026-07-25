from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_companies():
    response = client.get("/companies")
    assert response.status_code == 200


def test_get_tcs():
    response = client.get("/companies/TCS")
    assert response.status_code == 200


def test_invalid_company():
    response = client.get("/companies/INVALID")
    assert response.status_code == 404
