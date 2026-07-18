from typing import Dict, Any, List
import numpy as np
import pandas as pd
import traceback
import time
import logging

logger = logging.getLogger(__name__)

def predict_triage_severity(patient_data: Dict[str, Any], model: Any, preprocessor: Any, feature_list: List[str], include_explanation: bool = False) -> Dict[str, Any]:
    """
    Real ML inference function for Triage Severity using CatBoost.
    Transforms raw patient JSON into a pandas DataFrame, 
    applies the MultiLabelBinarizer for symptoms, and runs the regressor model.
    """
    start_time = time.perf_counter()
    try:
        # 1. Map frontend payload to expected features
        model_input = {
            'age': float(patient_data.get('age', 45)),
            'gender': patient_data.get('gender', 'Male'),
            'bmi': float(patient_data.get('bmi', 26.5)),
            'heart_rate': float(patient_data.get('hr', 75)),
            'systolic_bp': float(patient_data.get('sbp', 120)),
            'diastolic_bp': float(patient_data.get('dbp', 80)),
            'spO2': float(patient_data.get('spo2', 98)),
            'respiratory_rate': float(patient_data.get('respiratory_rate', 16)),
            'temperature': float(patient_data.get('temp', 37.0)),
            'blood_glucose': float(patient_data.get('glucose', 100)),
            'symptom_duration_days': float(patient_data.get('symptom_duration_days', 5)),
            'symptom_severity': float(patient_data.get('symptom_severity', 5)),
            'smoking': float(1.0 if patient_data.get('smoking', False) else 0.0)
        }
        


        df = pd.DataFrame([model_input])
        
        # 2. Process symptoms using MultiLabelBinarizer
        symptoms_raw = patient_data.get('symptoms', [])
        if isinstance(symptoms_raw, str):
            symptoms_raw = [s.strip() for s in symptoms_raw.split(',') if s.strip()]
            
        symptoms_encoded = preprocessor.transform([symptoms_raw])
        symptoms_df = pd.DataFrame(symptoms_encoded, columns=[f"symp_{c.replace(' ', '_')}" for c in preprocessor.classes_])
        
        # Concat the symptoms
        X_df = pd.concat([df, symptoms_df], axis=1)
        
        # Ensure all columns in feature_list exist, filling missing with 0
        for col in feature_list:
            if col not in X_df.columns:
                X_df[col] = 0.0
                
        # Reorder to match exact training feature list
        X_df = X_df[feature_list]
        
        # 3. Predict Severity Score (0-100)
        severity_score = model.predict(X_df)[0]
        severity_score = max(0.0, min(100.0, float(severity_score)))
        
        # 4. Categorize
        if severity_score >= 85:
            priority_category = "Critical"
            waiting_priority = "0 mins (Bypass Queue)"
            initial_clinical_risk = "Imminent Life Threat"
        elif severity_score >= 60:
            priority_category = "High"
            waiting_priority = "10 mins"
            initial_clinical_risk = "Potential Life Threat"
        elif severity_score >= 30:
            priority_category = "Medium"
            waiting_priority = "60 mins"
            initial_clinical_risk = "Significant Discomfort/Risk"
        else:
            priority_category = "Low"
            waiting_priority = "120 mins+"
            initial_clinical_risk = "Stable/Non-Urgent"

        # 5. SHAP Explanations
        explanations = []
        if include_explanation:
            try:
                import shap
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_df)
                
                if len(shap_values.shape) == 2:
                    sv = shap_values[0]
                else:
                    sv = shap_values
                    
                feature_importance = pd.DataFrame({
                    'feature': X_df.columns,
                    'importance': sv
                })
                feature_importance['abs_importance'] = feature_importance['importance'].abs()
                feature_importance = feature_importance.sort_values(by='abs_importance', ascending=False)
                
                top_features = feature_importance.head(5)
                
                for _, row in top_features.iterrows():
                    val = row['importance']
                    direction = "Increased Risk" if val > 0 else "Decreased Risk"
                    score_impact = f"{'+' if val > 0 else ''}{val:.1f} pts"
                    explanations.append({
                        "feature": row['feature'],
                        "contribution": f"{direction} ({score_impact})"
                    })
            except Exception as e:
                print(f"SHAP explanation failed: {str(e)}")
                traceback.print_exc()

        result = {
            "severity_score": round(severity_score, 1),
            "priority_category": priority_category,
            "waiting_priority": waiting_priority,
            "initial_clinical_risk": initial_clinical_risk,
            "confidence": 0.95,
            "explanations": explanations
        }
        
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.info(f"Prediction complete | Latency: {latency_ms}ms | Severity: {result['severity_score']} | Priority: {result['priority_category']}")
        return result
        
    except Exception as e:
        logger.error(f"Inference error: {str(e)}", exc_info=True)
        raise
