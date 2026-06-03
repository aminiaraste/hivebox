import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "0.0.1"}


def test_temperature():
    response = client.get("/temperature")

    assert response.status_code == 200
    assert "temperature" in response.json()
    temperature = response.json()["temperature"]

    assert isinstance(temperature, float)