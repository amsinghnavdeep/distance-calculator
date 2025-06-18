import pytest
from fastapi.testclient import TestClient
from app import app
from utils import haversine

client = TestClient(app)


# ----------------------------
# Unit Test for haversine
# ----------------------------
def test_haversine_ny_la():
    # Approximate distance between New York and LA
    ny_lat, ny_lon = 40.7128, -74.0060
    la_lat, la_lon = 34.0522, -118.2437
    dist = haversine(ny_lat, ny_lon, la_lat, la_lon)
    assert 3900 < dist < 4000


# ----------------------------
# API Tests
# ----------------------------

def test_missing_fields():
    res = client.post("/calculate", json={"source": "Delhi"})
    assert res.status_code == 422  # destination missing


def test_invalid_locations():
    res = client.post("/calculate", json={"source": "asdf", "destination": "qwerty"})
    assert res.status_code == 400
    assert "Could not geocode" in res.text or "detail" in res.json()


def test_valid_query():
    res = client.post("/calculate", json={"source": "New York", "destination": "Boston"})
    assert res.status_code == 200
    data = res.json()
    assert "distance_km" in data
    assert "distance_miles" in data
    assert data["distance_km"] > 0


def test_history_endpoint():
    res = client.get("/history")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    if data:
        assert "source" in data[0]
        assert "destination" in data[0]
        assert "distance_km" in data[0]


# Optional: Smoke test for startup
def test_startup():
    assert app.title.lower() in ["fastapi", "ai distance calculator", "distance calculator"]
