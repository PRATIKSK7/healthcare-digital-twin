import os
import json
import pandas as pd
import numpy as np
import joblib
from catboost import CatBoostRegressor
import shap

def run_verification():
    report = ["# V2 Integration Validation Report\n"]
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    REPORTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "reports"))
    
    # Check 1: Model Loading
    try:
        model_path = os.path.join(BASE_DIR, "catboost_triage_v2.cbm")
        cb = CatBoostRegressor()
        cb.load_model(model_path)
        report.append(f"## 1. Model Loading\n**Status: PASS**\n- Path: `{model_path}`\n- Successfully loaded CatBoostRegressor V2.\n")
    except Exception as e:
        report.append(f"## 1. Model Loading\n**Status: FAIL**\n- Error: {str(e)}\n")
        
    # Check 2: Feature List
    try:
        with open(os.path.join(BASE_DIR, "feature_list.json"), "r") as f:
            feature_list = json.load(f)
        
        # Verify CatBoost internal feature names match our JSON
        cb_features = cb.feature_names_
        if feature_list == cb_features:
            report.append(f"## 2. Feature Ordering\n**Status: PASS**\n- `feature_list.json` exactly matches model's expected inputs (Length: {len(feature_list)}).\n")
        else:
            report.append(f"## 2. Feature Ordering\n**Status: FAIL**\n- Mismatch detected between JSON and Model.\n")
    except Exception as e:
        report.append(f"## 2. Feature Ordering\n**Status: FAIL**\n- Error: {str(e)}\n")
        
    # Check 3: Preprocessor Vocabulary
    try:
        mlb = joblib.load(os.path.join(BASE_DIR, "preprocessor.joblib"))
        classes = list(mlb.classes_)
        expected = ["blurred vision", "shortness of breath", "depression", "abdominal pain"]
        missing = [c for c in expected if c not in classes]
        if not missing and len(classes) == 28:
            report.append(f"## 3. Preprocessor Vocabulary\n**Status: PASS**\n- Vocabulary contains {len(classes)} symptoms.\n- Verified presence of all key symptoms.\n- Classes: {classes}\n")
        else:
            report.append(f"## 3. Preprocessor Vocabulary\n**Status: FAIL**\n- Missing: {missing}\n")
    except Exception as e:
        report.append(f"## 3. Preprocessor Vocabulary\n**Status: FAIL**\n- Error: {str(e)}\n")
        
    # Check 4: Patient Prediction (Extreme)
    def predict_patient(overrides):
        base = {f: 0 for f in feature_list}
        base['age'] = 98
        base['gender'] = 'Male'
        base['bmi'] = 24.0
        base['smoking'] = 0
        base['heart_rate'] = 143
        base['systolic_bp'] = 250
        base['diastolic_bp'] = 110
        base['respiratory_rate'] = 28
        base['spO2'] = 82
        base['temperature'] = 37.0
        base['blood_glucose'] = 100
        base['symptom_duration_days'] = 10
        base['symptom_severity'] = 8
        base['symp_chest_pain'] = 1
        base['symp_shortness_of_breath'] = 1
        base['symp_blurred_vision'] = 1
        for k, v in overrides.items():
            base[k] = v
        df = pd.DataFrame([base])[feature_list]
        return cb.predict(df)[0], df

    try:
        score_base, df_base = predict_patient({})
        if score_base >= 60:
            report.append(f"## 4. Extreme Patient Scenario\n**Status: PASS**\n- Predicted Severity: {score_base:.2f}\n- Correctly identified as High/Critical.\n")
        else:
            report.append(f"## 4. Extreme Patient Scenario\n**Status: FAIL**\n- Predicted Severity: {score_base:.2f} (Too Low)\n")
    except Exception as e:
        report.append(f"## 4. Extreme Patient Scenario\n**Status: FAIL**\n- Error: {str(e)}\n")
        
    # Check 5: SpO2 Correction
    try:
        score_spo2, _ = predict_patient({'spO2': 98})
        diff = score_base - score_spo2
        if diff > 10:
            report.append(f"## 5. SpO₂ Correction Sensitivity\n**Status: PASS**\n- Corrected SpO₂ (82 -> 98)\n- Severity dropped significantly (from {score_base:.2f} to {score_spo2:.2f}).\n")
        else:
            report.append(f"## 5. SpO₂ Correction Sensitivity\n**Status: FAIL**\n- Severity only dropped to {score_spo2:.2f}.\n")
    except Exception as e:
        report.append(f"## 5. SpO₂ Correction Sensitivity\n**Status: FAIL**\n- Error: {str(e)}\n")
        
    # Check 6: HR Correction
    try:
        score_hr, _ = predict_patient({'heart_rate': 72})
        diff = score_base - score_hr
        if diff > 5:
            report.append(f"## 6. HR Correction Sensitivity\n**Status: PASS**\n- Corrected HR (143 -> 72)\n- Severity dropped (from {score_base:.2f} to {score_hr:.2f}).\n")
        else:
            report.append(f"## 6. HR Correction Sensitivity\n**Status: FAIL**\n- Severity only dropped to {score_hr:.2f}.\n")
    except Exception as e:
        report.append(f"## 6. HR Correction Sensitivity\n**Status: FAIL**\n- Error: {str(e)}\n")
        
    # Check 7: SHAP Dominance
    try:
        explainer = shap.TreeExplainer(cb)
        shap_values = explainer.shap_values(df_base)
        shap_df = pd.DataFrame({'feature': feature_list, 'shap': np.abs(shap_values[0])}).sort_values(by='shap', ascending=False)
        top_5 = shap_df.head(5)['feature'].tolist()
        
        expected_dominant = ['spO2', 'heart_rate']
        if all(f in top_5 for f in expected_dominant):
            report.append(f"## 7. SHAP Dominance Validation\n**Status: PASS**\n- Top Contributors: {top_5}\n- SpO₂ and HR correctly dominate the extreme patient's prediction.\n")
        else:
            report.append(f"## 7. SHAP Dominance Validation\n**Status: FAIL**\n- Top Contributors: {top_5}\n")
    except Exception as e:
        report.append(f"## 7. SHAP Dominance Validation\n**Status: FAIL**\n- Error: {str(e)}\n")
        
    # Final Verdict
    if "FAIL" not in "".join(report):
        report.append("\n## FINAL VERDICT\n**ALL TESTS PASSED.**\nRecommendation: Proceed with replacing the production model.")
    else:
        report.append("\n## FINAL VERDICT\n**FAILURES DETECTED.**\nRecommendation: DO NOT integrate into production until fixed.")
        
    with open(os.path.join(REPORTS_DIR, "v2_integration_validation.md"), "w") as f:
        f.write("\n".join(report))
        
    print("Verification complete.")

if __name__ == "__main__":
    run_verification()
