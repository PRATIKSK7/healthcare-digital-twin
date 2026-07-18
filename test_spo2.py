import requests

api_url = "http://localhost:8000/api/v1"
headers = {"Content-Type": "application/json"}

base_patient = {
    "patient_id": "Sens1",
    "age": 45, "gender": "Male", "bmi": 24, "smoking": False,
    "hr": 70, "sbp": 120, "dbp": 80,
    "spo2": 98, "temp": 37.0, "respiratory_rate": 16, "glucose": 100,
    "symptoms": ["chest pain"], "symptom_duration_days": 5
}

def pred(payload):
    r = requests.post(f"{api_url}/predict/frontend", json=payload, headers=headers)
    return r.json().get("severity_score", 0)

print(f"Base: {pred(base_patient)}")
p1 = base_patient.copy()
p1["hr"] = 170
print(f"HR 170: {pred(p1)}")
p2 = base_patient.copy()
p2["spo2"] = 82
print(f"SpO2 82: {pred(p2)}")
