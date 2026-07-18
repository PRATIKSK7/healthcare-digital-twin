import os
import random
import numpy as np
import pandas as pd

def generate_patients(num_samples=1000, output_csv="backend/datasets/triage_dataset_v2.csv"):
    np.random.seed(42)
    random.seed(42)
    
    # ---------------------------------------------------------
    # 1. Base Demographics
    # ---------------------------------------------------------
    age = np.random.normal(55, 18, num_samples).clip(18, 95)
    gender_prob = np.random.rand(num_samples)
    gender = np.where(gender_prob > 0.5, "Male", "Female")
    bmi = np.random.normal(28, 6, num_samples).clip(18.5, 45.0)
    smoking = np.random.choice([0, 1], size=num_samples, p=[0.8, 0.2])
    
    age_norm = (age - 18) / (95 - 18)
    bmi_norm = (bmi - 18.5) / (45.0 - 18.5)
    
    # ---------------------------------------------------------
    # 2. Skewed Base Severity & Latent Variables (0 to 1)
    # Using explicit categories to hit target distributions:
    # 45-55% healthy, 25-35% medium, 10-20% high, 5-10% critical
    # ---------------------------------------------------------
    base_illness = np.random.choice([0, 1, 2, 3], size=num_samples, p=[0.45, 0.30, 0.17, 0.08])
    base_latent = np.zeros(num_samples)
    base_latent[base_illness == 0] = np.random.uniform(0.0, 0.25, np.sum(base_illness == 0))
    base_latent[base_illness == 1] = np.random.uniform(0.25, 0.55, np.sum(base_illness == 1))
    base_latent[base_illness == 2] = np.random.uniform(0.55, 0.85, np.sum(base_illness == 2))
    base_latent[base_illness == 3] = np.random.uniform(0.85, 1.0, np.sum(base_illness == 3))
    
    # Specific latents are driven by the base latent but vary
    infection = np.clip(base_latent * np.random.beta(2, 2, num_samples) + age_norm * 0.05, 0, 1)
    dehydration = np.clip(base_latent * np.random.beta(2, 5, num_samples) + infection * 0.2, 0, 1)
    respiratory = np.clip(base_latent * np.random.beta(2, 2, num_samples) + smoking * 0.1 + infection * 0.1, 0, 1)
    metabolic = np.clip(base_latent * np.random.beta(2, 5, num_samples) + bmi_norm * 0.1, 0, 1)
    cardiac = np.clip(base_latent * np.random.beta(2, 4, num_samples) + age_norm * 0.1 + bmi_norm * 0.1 + respiratory * 0.1, 0, 1)
    neuro = np.clip(base_latent * np.random.beta(1, 5, num_samples) + infection * 0.1, 0, 1)
    
    # ---------------------------------------------------------
    # 3. Observable Vitals
    # Scaled down to clinically realistic ED averages
    # ---------------------------------------------------------
    heart_rate = 75 + cardiac * 30 + infection * 20 + dehydration * 10 + np.random.normal(0, 5, num_samples)
    heart_rate = np.clip(heart_rate, 40, 200).astype(int)
    
    systolic_bp = 120 + cardiac * 25 - dehydration * 15 + metabolic * 15 + age_norm * 10 + np.random.normal(0, 8, num_samples)
    systolic_bp = np.clip(systolic_bp, 70, 220).astype(int)
    
    diastolic_bp = 80 + cardiac * 10 - dehydration * 10 + metabolic * 10 + np.random.normal(0, 5, num_samples)
    diastolic_bp = np.clip(diastolic_bp, 40, 120).astype(int)
    
    respiratory_rate = 16 + respiratory * 10 + infection * 4 + cardiac * 2 + np.random.normal(0, 2, num_samples)
    respiratory_rate = np.clip(respiratory_rate, 10, 40).astype(int)
    
    spo2 = 98 - respiratory * 8 - cardiac * 2 + np.random.normal(0, 1, num_samples)
    spo2 = np.clip(spo2, 70, 100).astype(int)
    
    temperature = 36.8 + infection * 2.0 + np.random.normal(0, 0.3, num_samples)
    temperature = np.clip(temperature, 35.5, 41.5).round(1)
    
    blood_glucose = 100 + metabolic * 60 + bmi_norm * 20 + np.random.normal(0, 10, num_samples)
    blood_glucose = np.clip(blood_glucose, 60, 400).astype(int)
    
    # ---------------------------------------------------------
    # 4. Symptoms
    # Reduced frequencies
    # ---------------------------------------------------------
    def sample_symptom(prob):
        return (np.random.rand(num_samples) < prob).astype(int)
    
    chest_pain = sample_symptom(cardiac * 0.4 + respiratory * 0.1)
    sob = sample_symptom(respiratory * 0.5 + cardiac * 0.2)
    fever = sample_symptom(infection * 0.5)
    cough = sample_symptom(respiratory * 0.4 + infection * 0.2)
    dizziness = sample_symptom(dehydration * 0.3 + neuro * 0.2 + cardiac * 0.1)
    vomiting = sample_symptom(infection * 0.2 + metabolic * 0.1)
    fatigue = sample_symptom(base_latent * 0.5 + infection * 0.2)
    confusion = sample_symptom(neuro * 0.5 + infection * 0.1)
    headache = sample_symptom(infection * 0.2 + dehydration * 0.2)
    abdominal_pain = sample_symptom(infection * 0.1 + metabolic * 0.1)
    
    symptom_lists = []
    for i in range(num_samples):
        symps = []
        if chest_pain[i]: symps.append("chest pain")
        if sob[i]: symps.append("shortness of breath")
        if fever[i]: symps.append("fever")
        if cough[i]: symps.append("cough")
        if dizziness[i]: symps.append("dizziness")
        if vomiting[i]: symps.append("vomiting")
        if fatigue[i]: symps.append("fatigue")
        if confusion[i]: symps.append("confusion")
        if headache[i]: symps.append("headache")
        if abdominal_pain[i]: symps.append("abdominal pain")
        symptom_lists.append(", ".join(symps))
        
    symptom_duration = np.clip(np.random.exponential(scale=2 + infection*3 + metabolic*5, size=num_samples), 1, 30).astype(int)
    symptom_severity = np.clip((base_latent * 10 + np.random.normal(0, 1, num_samples)), 1, 10).astype(int)

    # ---------------------------------------------------------
    # 5. Simulated Clinical Outcomes (ONLY from latents)
    # ---------------------------------------------------------
    icu_prob = np.clip((respiratory * 0.5 + cardiac * 0.4 + neuro * 0.3 + infection * 0.2 + metabolic * 0.1), 0, 1)
    risk_of_deterioration = np.clip((cardiac * 0.4 + respiratory * 0.4 + neuro * 0.3 + metabolic * 0.2 + dehydration * 0.2), 0, 1)
    emergency_intervention = np.clip(np.maximum.reduce([respiratory*1.2, cardiac*1.2, neuro*1.2, infection*1.0]), 0, 1)
    
    expected_los = 1 + infection * 5 + respiratory * 7 + cardiac * 7 + neuro * 5 + metabolic * 3
    expected_los = np.clip(expected_los + np.random.normal(0, 1, num_samples), 0, 45).round(1)
    
    # ---------------------------------------------------------
    # 6. Continuous Severity Score (0 - 100)
    # Adjusted to ensure realistic distribution
    # ---------------------------------------------------------
    severity_score = (icu_prob * 30) + (risk_of_deterioration * 30) + (emergency_intervention * 20)
    # Shift base_latent impact to directly shape the final score bounds
    severity_score = np.clip(severity_score + base_latent*35 + np.random.normal(0, 2, num_samples), 0, 100).round(2)

    # Compile DataFrame
    df = pd.DataFrame({
        "age": np.round(age, 1),
        "gender": gender,
        "bmi": np.round(bmi, 1),
        "smoking": smoking,
        "heart_rate": heart_rate,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "respiratory_rate": respiratory_rate,
        "spO2": spo2,
        "temperature": temperature,
        "blood_glucose": blood_glucose,
        "symptoms": symptom_lists,
        "symptom_duration_days": symptom_duration,
        "symptom_severity": symptom_severity,
        
        "icu_admission_probability": np.round(icu_prob, 3),
        "risk_of_deterioration": np.round(risk_of_deterioration, 3),
        "emergency_intervention_probability": np.round(emergency_intervention, 3),
        "expected_length_of_stay_days": expected_los,
        "severity_score": severity_score
    })
    
    df_latents = pd.DataFrame({
        "infection": infection,
        "dehydration": dehydration,
        "respiratory": respiratory,
        "metabolic": metabolic,
        "cardiac": cardiac,
        "neuro": neuro,
        "base_latent": base_latent
    })
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    return df, df_latents

if __name__ == "__main__":
    df, df_latents = generate_patients()
    print("Dataset generated.")
