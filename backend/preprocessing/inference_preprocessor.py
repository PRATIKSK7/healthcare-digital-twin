import re
import json
from typing import Dict, Any, List, Tuple

class InferencePreprocessor:
    def __init__(self):
        self.known_symptoms = {
            "chest_pain": 2.5, "shortness_of_breath": 2.0, "dizziness": 1.5,
            "nausea": 1.0, "headache": 0.8, "fatigue": 0.5,
            "palpitations": 1.8, "cough": 0.5, "fever": 1.0
        }
        
        # Expanded Physiological and Demographic limits
        self.limits = {
            "age": [0, 120],
            "bmi": [10.0, 60.0],
            "heart_rate": [20, 300],
            "blood_pressure_sys": [50, 250],
            "blood_pressure_dia": [30, 150],
            "spO2": [50, 100],
            "respiratory_rate": [5, 60],
            "temperature": [80.0, 110.0],
            "blood_glucose": [20.0, 1000.0],
            "symptom_duration_days": [0, 3650],
            "symptom_severity": [1, 10]
        }
        
        self.medians = {
            "age": 45,
            "bmi": 26.5,
            "heart_rate": 75,
            "blood_pressure_sys": 120,
            "blood_pressure_dia": 80,
            "spO2": 98.0,
            "respiratory_rate": 16,
            "temperature": 98.6,
            "blood_glucose": 100.0,
            "symptom_duration_days": 1,
            "symptom_severity": 3
        }
        
    def _sanitize_string(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[^a-z0-9_ ]', '', text)
        return text.replace(" ", "_")

    def process_symptoms(self, symptoms: List[str]) -> Tuple[List[str], float, Dict[str, Any]]:
        stats = {"duplicates_removed": 0, "unknown_mapped": 0}
        if not symptoms:
            return [], 0.0, stats
            
        initial_count = len(symptoms)
        clean_symptoms = set(self._sanitize_string(s) for s in symptoms if s)
        stats["duplicates_removed"] = initial_count - len(clean_symptoms)
        
        processed_list = []
        total_weight = 0.0
        
        for sym in clean_symptoms:
            if sym in self.known_symptoms:
                processed_list.append(sym)
                total_weight += self.known_symptoms[sym]
            else:
                processed_list.append("other_unknown")
                total_weight += 0.2
                stats["unknown_mapped"] += 1
                
        return processed_list, total_weight, stats

    def validate_and_preprocess(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        stats = {"imputed_values": 0, "warnings": []}
        processed_data = data.copy()
        
        # 1. Bounds checking and Imputation
        missing_count = 0
        total_features = len(self.limits)
        
        for feature, (min_val, max_val) in self.limits.items():
            val = processed_data.get(feature)
            if val is None:
                processed_data[feature] = self.medians[feature]
                stats["imputed_values"] += 1
                missing_count += 1
                stats["warnings"].append(f"Missing {feature}, imputed with {self.medians[feature]}")
            else:
                if not (min_val <= val <= max_val):
                    raise ValueError(f"Impossible value for {feature}: {val}. Must be between {min_val} and {max_val}.")
        
        if missing_count / total_features > 0.4:
            raise ValueError(f"Data confidence too low. {missing_count}/{total_features} core vitals are missing.")
            
        # 2. Boolean Logic & Constraints
        # Impute missing bools to False
        for bool_feat in ['smoking', 'alcohol', 'pregnancy']:
            if processed_data.get(bool_feat) is None:
                processed_data[bool_feat] = False
                
        # Reject impossible pregnancy
        if processed_data.get('pregnancy') and processed_data.get('gender', '').lower() == 'male':
            raise ValueError("Pregnancy=True is impossible for gender=Male.")
            
        # 3. Handle Lists (Counts for Model Compatibility)
        list_features = ['comorbidities', 'medical_history', 'family_history', 'previous_diseases', 'current_medication', 'vaccination_history']
        for feat in list_features:
            lst = processed_data.get(feat, [])
            if not isinstance(lst, list):
                lst = []
            processed_data[f"{feat}_count"] = len(lst)
            
        # 4. Symptom Handling
        raw_symptoms = processed_data.get("symptoms", [])
        final_symptoms, symptom_weight, sym_stats = self.process_symptoms(raw_symptoms)
        processed_data["symptoms_clean"] = final_symptoms
        processed_data["symptom_severity_weight"] = symptom_weight
        stats["symptom_stats"] = sym_stats
        
        # 5. Feature Engineering
        processed_data["pulse_pressure"] = processed_data["blood_pressure_sys"] - processed_data["blood_pressure_dia"]
        
        return processed_data, stats
