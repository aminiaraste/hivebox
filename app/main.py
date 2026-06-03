from datetime import datetime, timezone, timedelta

import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

VERSION = "0.0.1"

SENSEBOX_IDS = [
    "5eba5fbad46fb8001b799786",
    "5c21ff8f919bf8001adf2488",
    "5ade1acf223bd80019a1011c",
]


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "UP"}


@app.get("/version")
def get_version():
    """Return application version."""
    return {"version": VERSION}


@app.get("/temperature")
def get_temperature():
    """Return average temperature from senseBoxes."""
    temperatures = []

    for box_id in SENSEBOX_IDS:
        url = f"https://api.opensensemap.org/boxes/{box_id}"
        response = requests.get(url, timeout=10)
        print(response.json())
        response.raise_for_status()
        box = response.json()
        for sensor in box.get("sensors", []):
            if sensor.get("unit") == "°C":
                last_measurement = sensor.get("lastMeasurement")    
                if not last_measurement:
                    continue

                created_at = last_measurement.get("createdAt")
                value = last_measurement.get("value")

                measurement_time = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                )

                if datetime.now(timezone.utc) - measurement_time <= timedelta(hours=1):
                    temperatures.append(float(value))

    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperature data newer than 1 hour found",
        )

    average = sum(temperatures) / len(temperatures)

    return {"temperature": round(average, 2)}

