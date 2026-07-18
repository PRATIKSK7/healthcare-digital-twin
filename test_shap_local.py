import json, joblib, pandas as pd
from backend.models.manager import ModelManager
import backend.models.inference as inference

manager = ModelManager()
patient = {
    'age': 98, 'gender': 'Male', 'hr': 143, 'sbp': 250, 'dbp': 90, 'spo2': 82, 'temp': 39, 'glucose': 110,
    'symptoms': ['chest pain', 'shortness of breath', 'blurred vision'],
    'symptom_duration_days': 10
}
res = inference.predict_triage_severity(patient, manager.model, manager.preprocessor, manager.feature_list, True)
print(json.dumps(res, indent=2))
