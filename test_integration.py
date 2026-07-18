import sys
sys.path.append('backend')
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
headers = {"X-API-Key": "dev_secret_key_123"}

# Test Predict Frontend
print("Testing /predict/frontend...")
payload_predict = {
    "age": 45,
    "gender": "Male",
    "symptoms": ["chest pain", "shortness of breath", "fever"],
    "hr": 120,
    "sbp": 150,
    "smoking": True,
    "symptom_duration_days": 2,
    "symptom_severity": 8
}
response = client.post("/api/v1/predict/frontend", json=payload_predict, headers=headers)
print(response.status_code)
print(response.json())

# Test Simulate Frontend
print("\nTesting /simulate/frontend...")
payload_simulate = {
    "name": "John Doe",
    "age": 45,
    "gender": "Male",
    "symptoms": ["chest pain", "shortness of breath", "fever"],
    "hr": 120,
    "sbp": 150,
    "dbp": 90,
    "temp": 39.0,
    "spo2": 88,
    "glucose": 130,
    "bmi": 28.5,
    "crp": 12.0,
    "scenario": "Standard Care"
}
response = client.post("/api/v1/simulate/frontend", json=payload_simulate, headers=headers)
print(response.status_code)
print(response.json())
