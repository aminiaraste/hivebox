import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from datetime import datetime, timezone
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


@patch("app.main.requests.get")
def test_temperature(mock_get):
    """Verify the /temperature endpoint returns parsed sensor data."""
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "sensors": [
            {
                "title": "Temperatur",
                "unit": "°C",
                "lastMeasurement": {
                    "createdAt": now,
                    "value": "20.0"
                }
            }
        ]
    }

    response = client.get("/temperature")

    assert response.status_code == 200
    assert response.json() == {"temperature": 20.0}
