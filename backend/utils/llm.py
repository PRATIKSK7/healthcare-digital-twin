from typing import Dict, Any

def generate_clinical_explanation(ml_prediction_data: Dict[str, Any]) -> str:
    """
    Simulates calling Claude API.
    CRITICAL RULE: Claude MUST NEVER decide the disease or risk level.
    This function ONLY accepts the finalized prediction from the ML model
    and explains it in natural language for the clinician.
    """
    
    top_disease = ml_prediction_data["top_5_diseases"][0]["disease"]
    probability = ml_prediction_data["probability"]
    confidence = ml_prediction_data["confidence"]
    risk_level = ml_prediction_data["risk_level"]
    tests = ", ".join(ml_prediction_data["next_medical_tests"])
    
    # In production, we'd send a prompt to Claude here with strict guardrails
    explanation = (
        f"The machine learning model has identified {top_disease} as the primary condition "
        f"with a probability of {probability:.1%}. The overall confidence in this diagnostic "
        f"assessment is {confidence:.1%}, stratifying the patient into a {risk_level} risk category. "
        f"Based on the model's feature importance weights (e.g., elevated heart rate variability), "
        f"it is recommended to proceed with: {tests} to confirm the diagnosis."
    )
    
    return explanation
