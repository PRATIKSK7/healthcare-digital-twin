import pytest
from fastapi.testclient import TestClient
from main import app
import os

# Create client
client = TestClient(app)

# Test headers
HEADERS = {"X-API-Key": os.getenv("API_KEY", "dev_secret_key_123")}
BAD_HEADERS = {"X-API-Key": "wrong_key"}

def test_health_check():
    response = client.get("/api/v1/health", headers=HEADERS)
    assert response.status_code == 200
    
def test_health_check_unauthorized():
    response = client.get("/api/v1/health", headers=BAD_HEADERS)
    assert response.status_code == 401
def test_predict_risk():
    payload = {
        "patient_id": "test_123",
        "telemetry": {
            "patient_id": "test_123",
            "age": 50,
            "gender": "Male",
            "bmi": 24.5,
            "blood_pressure_sys": 120,
            "blood_pressure_dia": 80,
            "heart_rate": 70,
            "spO2": 98.0,
            "respiratory_rate": 14,
            "temperature": 98.6,
            "blood_glucose": 95,
            "symptoms": ["chest_pain"]
        }
    }
    response = client.post("/api/v1/predict/risk", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "test_123"
    assert "severity_score" in data
    assert "priority" in data

def test_invalid_payload_validation():
    # Intentionally bad schema
    payload = {"wrong_field": "test"}
    response = client.post("/api/v1/predict/risk", json=payload, headers=HEADERS)
    assert response.status_code == 422
