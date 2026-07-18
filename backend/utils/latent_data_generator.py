import os
import numpy as np
import pandas as pd
import random

# Fix seeds for reproducibility
np.random.seed(42)
random.seed(42)

def generate_latent_dataset(num_samples=5000, output_path="backend/datasets/triage_patient_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    data = []
    
    for _ in range(num_samples):
        # 1. PRIORS
        age = np.random.randint(18, 95)
        gender = np.random.choice(["Male", "Female"])
        bmi = round(np.random.uniform(18.5, 45.0), 1)
        smoking = np.random.choice([0, 1], p=[0.8, 0.2])
        
        # 2. LATENT VARIABLES (0.0 to 1.0)
        age_factor = max(0, (age - 50) / 100.0) 
        
        L_inf = np.random.beta(a=1, b=5)
        L_resp = np.random.beta(a=1 + age_factor, b=5)
        L_card = np.random.beta(a=1 + age_factor + (smoking * 0.5), b=5)
        L_neuro = np.random.beta(a=1, b=8)
        
        # Correlated latents
        L_deh = np.clip(np.random.beta(a=1, b=5) + (L_inf * 0.3), 0, 1)
        L_met = np.clip(np.random.beta(a=1, b=6) + (L_inf * 0.2) + ((bmi - 25)/100.0 if bmi > 25 else 0), 0, 1)
        
        # 3. OBSERVABLE VITALS
        hr_base = 70.0
        hr_effect = (L_inf * 45) + (L_card * 30) + (L_deh * 35) + (L_resp * 20)
        hr = int(np.clip(hr_base + hr_effect + np.random.normal(0, 5), 30, 220))
        
        sbp_base = 120.0
        sbp_effect = (L_card * 60 * np.random.choice([1, -1.5])) - (L_deh * 40) + (L_inf * -20)
        sbp = int(np.clip(sbp_base + sbp_effect + np.random.normal(0, 10), 50, 250))
        
        spo2_base = 99.0
        spo2_effect = (L_resp * 25) + (L_card * 10) + (smoking * 2)
        spo2 = int(np.clip(spo2_base - spo2_effect + np.random.normal(0, 1.5), 50, 100))
        
        temp_base = 37.0
        temp_effect = (L_inf * 3.5)
        temp = round(np.clip(temp_base + temp_effect + np.random.normal(0, 0.3), 34.0, 42.0), 1)
        
        glucose_base = 95.0
        glucose_effect = (L_met * 200) + (bmi * 1.5)
        glucose = int(np.clip(glucose_base + glucose_effect + np.random.normal(0, 15), 40, 600))
        
        # 4. SYMPTOMS & SEVERITY
        symps = set()
        if L_card > 0.4 and np.random.rand() < 0.8: symps.add("chest pain")
        if L_resp > 0.4 and np.random.rand() < 0.85: symps.add("shortness of breath")
        if L_inf > 0.4 and np.random.rand() < 0.8: symps.add("fever")
        if L_neuro > 0.5 and np.random.rand() < 0.7: symps.add("confusion")
        if L_neuro > 0.7 and np.random.rand() < 0.6: symps.add("unconscious")
        if L_deh > 0.5 and np.random.rand() < 0.8: symps.add("dizziness")
        
        if len(symps) == 0 or np.random.rand() < 0.5:
            symps.add(np.random.choice(["fatigue", "headache", "cough", "nausea"]))
            
        symps_list = list(symps)
        
        max_latent = max([L_inf, L_resp, L_card, L_neuro, L_deh, L_met])
        symptom_severity = int(np.clip(np.random.normal(max_latent * 10, 1.5), 1, 10))
        duration = np.random.randint(1, 14)
        
        # 5. CLINICAL OUTCOMES
        linear_risk = -4.0 + (L_inf * 3.5) + (L_resp * 4.0) + (L_card * 4.5) + (L_neuro * 4.0) + (L_deh * 2.5) + (L_met * 2.0)
        p_icu = 1.0 / (1.0 + np.exp(-linear_risk))
        
        icu_admitted = int(np.random.rand() < p_icu)
        intervention_needed = int(any(l > 0.75 for l in [L_inf, L_resp, L_card, L_neuro]))
        los = np.random.poisson(lam=(p_icu * 14) + 1)
        
        # 6. DERIVED TARGET (Severity Score)
        score = (p_icu * 50) + (min(los, 21) / 21.0 * 20) + (intervention_needed * 30)
        final_score = np.clip(score + np.random.normal(0, 3.0), 0, 100)
        
        row = {
            "age": age,
            "gender": gender,
            "bmi": bmi,
            "heart_rate": hr,
            "systolic_bp": sbp,
            "spO2": spo2,
            "temperature": temp,
            "blood_glucose": glucose,
            "symptom_severity": symptom_severity,
            "symptom_duration_days": duration,
            "smoking": smoking,
            "symptoms": ", ".join(symps_list),
            "severity_score": round(final_score, 2),
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {num_samples} latent-based triage records at {output_path}")
    return df

if __name__ == "__main__":
    generate_latent_dataset()
