import requests, json
payload = {
    'age': 98, 'gender': 'Male', 'hr': 143, 'sbp': 250, 'spo2': 82, 
    'symptoms': ['chest pain', 'shortness of breath', 'blurred vision'],
    'symptom_duration_days': 10
}
res = requests.post('http://127.0.0.1:8000/api/v1/predict/frontend', json=payload, headers={'X-API-Key': 'dev_secret_key_123'})
print(json.dumps(res.json(), indent=2))
