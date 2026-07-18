import os
import pandas as pd
import numpy as np
import random
from typing import List, Dict

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

ALL_SYMPTOMS = [
    "abdominal pain", "anxiety", "appetite loss", "back pain", "blurred vision",
    "chest pain", "cough", "depression", "diarrhea", "dizziness",
    "fatigue", "fever", "headache", "insomnia", "joint pain",
    "muscle pain", "nausea", "rash", "runny nose", "shortness of breath",
    "sneezing", "sore throat", "sweating", "swelling", "tremors",
    "vomiting", "weight gain", "weight loss"
]

def generate_patients(n_samples=30000):
    data = []
    
    for _ in range(n_samples):
        # 1. GENERATE LATENT VARIABLES (0.0 to 1.0)
        # We use beta distributions to keep them bounded and skewed low for mostly healthy
        latents = {
            "infection_severity": np.random.beta(1.5, 5),
            "cardiac_stress": np.random.beta(1.5, 6),
            "respiratory_failure": np.random.beta(1.2, 7),
            "neurological_dysfunction": np.random.beta(1.1, 8),
            "dehydration": np.random.beta(1.5, 4),
            "metabolic_dysfunction": np.random.beta(1.5, 5)
        }
        
        # Introduce critical spikes for some patients to ensure we hit the 10% critical bucket
        spike = np.random.rand()
        if spike < 0.15:  # 15% chance of major single-system failure
            sys = random.choice(list(latents.keys()))
            latents[sys] = min(1.0, latents[sys] + np.random.uniform(0.4, 0.8))
        elif spike < 0.25:  # 10% chance of multi-system failure
            for sys in random.sample(list(latents.keys()), 2):
                latents[sys] = min(1.0, latents[sys] + np.random.uniform(0.3, 0.7))
        
        # 2. DEMOGRAPHICS
        age = int(np.clip(np.random.normal(45, 18), 18, 100))
        gender = random.choice(["Male", "Female", "Other"])
        
        # Age adds biological frailty, boosting latent impacts
        frailty_modifier = 1.0 + max(0, (age - 60) / 40.0)
        for k in latents:
            latents[k] = min(1.0, latents[k] * (1.0 + (frailty_modifier - 1.0) * 0.5))

        bmi = round(np.clip(np.random.normal(26, 5), 16, 50), 1)
        smoking = bool(random.random() < 0.2)
        
        # 3. VITALS (Driven by Latents + Noise)
        
        # Heart Rate: Base (60-100) + Infection + Cardiac Stress + Dehydration
        hr_base = np.random.normal(75, 10)
        hr_elev = (latents["infection_severity"] * 35) + (latents["cardiac_stress"] * 45) + (latents["dehydration"] * 25)
        hr = int(np.clip(hr_base + hr_elev, 40, 200))
        
        # SBP: Base (100-130) + Cardiac Stress - Dehydration
        sbp_base = np.random.normal(120, 10)
        sbp_shift = (latents["cardiac_stress"] * 60) - (latents["dehydration"] * 40)
        # Age adds to SBP naturally
        sbp_age = (age - 40) * 0.4
        sbp = int(np.clip(sbp_base + sbp_shift + sbp_age, 60, 250))
        
        dbp = int(np.clip(sbp * random.uniform(0.5, 0.7), 40, 140))
        
        # Respiratory Rate: Base (12-20) + Respiratory + Infection
        rr_base = np.random.normal(16, 2)
        rr_elev = (latents["respiratory_failure"] * 20) + (latents["infection_severity"] * 8)
        rr = int(np.clip(rr_base + rr_elev, 8, 45))
        
        # SpO2: Base (97-100) - Respiratory
        spo2_base = np.random.normal(98, 1)
        spo2_drop = (latents["respiratory_failure"] * 25)
        if smoking:
            spo2_drop += random.uniform(1, 3)
        spo2 = round(np.clip(spo2_base - spo2_drop, 60, 100), 1)
        
        # Temperature: Base 36.5-37.5 + Infection
        temp_base = np.random.normal(37.0, 0.3)
        temp_elev = latents["infection_severity"] * 3.5
        temp = round(np.clip(temp_base + temp_elev, 35.0, 41.5), 1)
        
        # Blood Glucose: Base (70-110) + Metabolic
        glu_base = np.random.normal(95, 15)
        glu_elev = latents["metabolic_dysfunction"] * 250
        glu = round(np.clip(glu_base + glu_elev, 40, 600), 1)
        
        # 4. SYMPTOMS GENERATION
        symptoms = set()
        
        # Symptom mapping (Latent -> Trigger Prob -> Symptoms)
        # Infection
        if random.random() < latents["infection_severity"]: symptoms.add("fever")
        if random.random() < latents["infection_severity"] * 0.8: symptoms.add("fatigue")
        if random.random() < latents["infection_severity"] * 0.6: symptoms.add("muscle pain")
        if random.random() < latents["infection_severity"] * 0.5: symptoms.add("sweating")
        
        # Cardiac
        if random.random() < latents["cardiac_stress"] * 1.2: symptoms.add("chest pain")
        if random.random() < latents["cardiac_stress"]: symptoms.add("shortness of breath")
        if random.random() < latents["cardiac_stress"] * 0.7: symptoms.add("dizziness")
        if random.random() < latents["cardiac_stress"] * 0.6: symptoms.add("sweating")
        
        # Respiratory
        if random.random() < latents["respiratory_failure"] * 1.3: symptoms.add("shortness of breath")
        if random.random() < latents["respiratory_failure"] * 0.8: symptoms.add("cough")
        if random.random() < latents["respiratory_failure"] * 0.5: symptoms.add("chest pain")
        
        # Neurological
        if random.random() < latents["neurological_dysfunction"] * 1.2: symptoms.add("dizziness")
        if random.random() < latents["neurological_dysfunction"]: symptoms.add("blurred vision")
        if random.random() < latents["neurological_dysfunction"]: symptoms.add("headache")
        if random.random() < latents["neurological_dysfunction"] * 0.8: symptoms.add("tremors")
        
        # Dehydration
        if random.random() < latents["dehydration"] * 1.2: symptoms.add("dizziness")
        if random.random() < latents["dehydration"] * 0.9: symptoms.add("headache")
        if random.random() < latents["dehydration"] * 0.7: symptoms.add("fatigue")
        
        # Metabolic
        if random.random() < latents["metabolic_dysfunction"]: symptoms.add("vomiting")
        if random.random() < latents["metabolic_dysfunction"]: symptoms.add("nausea")
        if random.random() < latents["metabolic_dysfunction"] * 0.8: symptoms.add("fatigue")
        
        # Random noise symptoms (10% chance for healthy people to have minor symptoms)
        minor_symptoms = ["runny nose", "sneezing", "sore throat", "rash", "back pain", "joint pain", "insomnia", "anxiety", "depression", "weight gain", "weight loss", "abdominal pain", "diarrhea", "appetite loss", "swelling"]
        if random.random() < 0.4:
            symptoms.add(random.choice(minor_symptoms))
        if random.random() < 0.2:
            symptoms.add(random.choice(minor_symptoms))
            
        symp_list = list(symptoms)
        symptom_duration = int(np.clip(np.random.normal(4, 3), 1, 30))
        
        # 5. CLINICAL OUTCOMES
        # Probability of ICU
        icu_prob = (latents["cardiac_stress"] * 0.35 + 
                   latents["respiratory_failure"] * 0.35 + 
                   latents["neurological_dysfunction"] * 0.2 +
                   latents["metabolic_dysfunction"] * 0.1)
        need_icu = icu_prob > 0.65
        
        # Oxygen
        oxy_prob = latents["respiratory_failure"] * 0.8 + (1 if spo2 < 90 else 0) * 0.5
        need_oxygen = oxy_prob > 0.5
        
        # Emergency Procedure
        proc_prob = latents["cardiac_stress"] * 0.6 + latents["neurological_dysfunction"] * 0.4
        need_proc = proc_prob > 0.7
        
        # Admission
        adm_prob = max(icu_prob, latents["infection_severity"] * 0.6 + latents["dehydration"] * 0.5)
        need_admission = adm_prob > 0.5
        
        # 6. DERIVE SEVERITY SCORE (0-100) FROM OUTCOMES
        base_score = 10
        if need_icu: base_score += 40
        if need_proc: base_score += 30
        if need_oxygen: base_score += 15
        if need_admission: base_score += 15
        
        # Add continuous outcome risk to smooth out the steps
        outcome_risk = (icu_prob * 30) + (oxy_prob * 15) + (proc_prob * 20) + (adm_prob * 10)
        
        # Physiological extremes (objective markers that guarantee high severity)
        physio_risk = 0
        if hr > 130 or hr < 50: physio_risk += 15
        if sbp > 180 or sbp < 90: physio_risk += 15
        if spo2 < 92: physio_risk += 20
        if temp > 39.5: physio_risk += 10
        
        raw_severity = base_score + (outcome_risk * 0.6) + (physio_risk * 0.6)
        
        # Add some random clinical judgment noise (doctors rate differently)
        clinical_noise = np.random.normal(0, 5)
        final_severity = float(np.clip(raw_severity + clinical_noise, 0, 100))
        
        # For the ML Model to have an approximation of subjective "symptom severity" reported by patient
        # We will make this slightly correlated but NOT a perfect proxy, simulating a 1-10 pain/discomfort scale.
        subjective_severity = int(np.clip(np.random.normal(final_severity / 10, 2), 1, 10))

        patient = {
            "age": age,
            "gender": gender,
            "bmi": bmi,
            "smoking": int(smoking),
            "heart_rate": hr,
            "systolic_bp": sbp,
            "diastolic_bp": dbp,
            "respiratory_rate": rr,
            "spO2": spo2,
            "temperature": temp,
            "blood_glucose": glu,
            "symptom_duration_days": symptom_duration,
            "symptom_severity": subjective_severity,
            "symptoms_list": ",".join(symp_list),
            "severity_score": round(final_severity, 1)
        }
        
        # Extract individual symptoms for ML Training directly to bypass MLB if needed, 
        # but we'll include it for completeness so the pipeline works
        for s in ALL_SYMPTOMS:
            patient[f"symp_{s.replace(' ', '_')}"] = 1 if s in symptoms else 0
            
        data.append(patient)
        
    df = pd.DataFrame(data)
    
    # Stratify to hit target distribution exactly
    # Target: Low 35%, Med 35%, High 20%, Critical 10%
    q_low = df['severity_score'].quantile(0.35)
    q_med = df['severity_score'].quantile(0.70)
    q_high = df['severity_score'].quantile(0.90)
    
    def remap_severity(x):
        # We want to stretch/squash the distribution to fit the 0-30, 30-60, 60-85, 85-100 bands
        if x <= q_low:
            return (x / q_low) * 29.9
        elif x <= q_med:
            return 30.0 + ((x - q_low) / (q_med - q_low)) * 29.9
        elif x <= q_high:
            return 60.0 + ((x - q_med) / (q_high - q_med)) * 24.9
        else:
            return 85.0 + ((x - q_high) / (100 - q_high)) * 15.0
            
    df['severity_score'] = df['severity_score'].apply(remap_severity)
    df['severity_score'] = df['severity_score'].clip(0, 100).round(1)
    
    return df

def generate_report(df, filepath):
    # Calculate classes
    def get_class(s):
        if s >= 85: return "Critical"
        if s >= 60: return "High"
        if s >= 30: return "Medium"
        return "Low"
        
    df['class'] = df['severity_score'].apply(get_class)
    dist = df['class'].value_counts(normalize=True) * 100
    
    # Ensure all symptoms exist in the dataframe before checking sum
    symp_cols = [c for c in df.columns if c.startswith("symp_")]
    missing = sum(1 for c in df[symp_cols].sum() if c == 0)
    
    corr = df[['severity_score', 'heart_rate', 'spO2', 'systolic_bp', 'symptom_severity', 'age']].corr()
    
    report = f"""# Synthetic Triage Dataset v2 Generation Report

## Overview
- **Total Patients:** {len(df):,}
- **Objective:** Completely rebuilt dataset to eliminate label leakage. Severity scores are derived from simulated clinical outcomes driven by hidden latent physiological variables.

## Distribution
- **Low (0-29.9):** {dist.get('Low', 0):.1f}%
- **Medium (30-59.9):** {dist.get('Medium', 0):.1f}%
- **High (60-84.9):** {dist.get('High', 0):.1f}%
- **Critical (85-100):** {dist.get('Critical', 0):.1f}%

## Feature Correlations with Target (Severity Score)
```
{corr['severity_score'].round(3).to_string()}
```

## Missing Values
```
{df.isnull().sum().to_string()}
```

## Symptom Frequencies
The dataset includes instances of all {len(ALL_SYMPTOMS)} frontend symptoms.
({missing} symptoms were entirely missing in generation).
"""
    
    symp_freqs = df[symp_cols].sum().sort_values(ascending=False)
    
    report += "\n```\n" + symp_freqs.to_string() + "\n```\n"
    
    with open(filepath, "w") as f:
        f.write(report)
        
    # Drop the temporary class column
    df = df.drop(columns=['class'])
    return df

if __name__ == "__main__":
    print("Generating Latent-driven Dataset V2...")
    df = generate_patients(30000)
    
    # Save dataset
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../datasets/triage_dataset_v2.csv"))
    df.to_csv(dataset_path, index=False)
    print(f"Dataset saved to {dataset_path}")
    
    # Generate report
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../reports/dataset_generation_report.md"))
    generate_report(df, report_path)
    print(f"Report saved to {report_path}")
