import os
import random
import numpy as np
import pandas as pd

def compute_triage_severity(row):
    """
    Computes a continuous severity score (0-100) using a modified NEWS2 approach.
    """
    score = 0.0
    
    # 1. SpO2 - Highly sensitive
    spo2 = row['spO2']
    if spo2 <= 88: score += 40
    elif spo2 <= 91: score += 25
    elif spo2 <= 93: score += 15
    elif spo2 <= 95: score += 5
    
    # 2. Heart Rate
    hr = row['heart_rate']
    if hr >= 140 or hr <= 40: score += 25
    elif hr >= 120 or hr <= 50: score += 15
    elif hr >= 100: score += 5
    
    # 3. Systolic BP
    sbp = row['systolic_bp']
    if sbp <= 90: score += 30
    elif sbp <= 100: score += 15
    elif sbp >= 180: score += 20
    elif sbp >= 160: score += 10
    
    # 4. Temperature
    temp = row['temperature']
    if temp >= 39.5 or temp <= 35.0: score += 15
    elif temp >= 38.5: score += 10
    
    # 5. Symptom Severity (Subjective 1-10)
    sev = row['symptom_severity']
    score += (sev * 1.5)
    
    # 6. Age Risk Multiplier
    age = row['age']
    if age > 75: score += 5
    elif age > 60: score += 3
    
    # 7. High Risk Symptoms
    symptoms = str(row.get('symptoms', ''))
    if any(s in symptoms for s in ['chest pain', 'shortness of breath', 'unconscious', 'seizure', 'stroke']):
        score += 25
    elif any(s in symptoms for s in ['dizziness', 'fainting', 'severe pain', 'vomiting blood']):
        score += 15
        
    # Cap at 100 and floor at 0
    # Add minor random noise for continuous distribution
    final_score = score + random.uniform(-2.0, 2.0)
    return max(0.0, min(100.0, round(final_score, 2)))

def generate_triage_dataset(num_samples=5000, output_path="backend/datasets/triage_dataset.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    data = []
    
    symptom_pool = [
        "chest pain", "shortness of breath", "fever", "cough", "headache",
        "dizziness", "nausea", "vomiting", "abdominal pain", "back pain",
        "fatigue", "weakness", "palpitations", "leg swelling", "sore throat",
        "confusion", "unconscious", "seizure", "stroke symptoms", "trauma"
    ]
    
    for _ in range(num_samples):
        age = random.randint(18, 95)
        gender = random.choice(["Male", "Female"])
        
        # Decide if this is a critical, sick, or healthy patient to ensure good distribution
        patient_type = random.choices(["Critical", "Sick", "Stable"], weights=[0.15, 0.40, 0.45])[0]
        
        if patient_type == "Critical":
            spO2 = random.randint(75, 93)
            hr = random.choice([random.randint(30, 50), random.randint(130, 180)])
            sbp = random.choice([random.randint(60, 90), random.randint(180, 220)])
            temp = random.uniform(34.5, 40.5)
            severity = random.randint(8, 10)
            symps = random.sample(["chest pain", "shortness of breath", "unconscious", "seizure", "stroke symptoms", "severe pain"], k=random.randint(1, 3))
        elif patient_type == "Sick":
            spO2 = random.randint(92, 96)
            hr = random.randint(90, 125)
            sbp = random.choice([random.randint(95, 110), random.randint(140, 160)])
            temp = random.uniform(37.5, 39.0)
            severity = random.randint(5, 8)
            symps = random.sample(["fever", "cough", "abdominal pain", "nausea", "dizziness", "headache"], k=random.randint(1, 3))
        else: # Stable
            spO2 = random.randint(96, 100)
            hr = random.randint(60, 95)
            sbp = random.randint(110, 135)
            temp = random.uniform(36.1, 37.4)
            severity = random.randint(1, 4)
            symps = random.sample(["fatigue", "sore throat", "back pain", "cough", "minor pain"], k=random.randint(1, 2))
            
        bmi = round(random.uniform(18.5, 40.0), 1)
        glucose = random.randint(70, 300)
        smoking = random.choice([0, 1])
        duration = random.randint(1, 30)
        
        row = {
            "age": age,
            "gender": gender,
            "bmi": bmi,
            "heart_rate": hr,
            "systolic_bp": sbp,
            "spO2": spO2,
            "temperature": round(temp, 1),
            "blood_glucose": glucose,
            "symptom_severity": severity,
            "symptom_duration_days": duration,
            "smoking": smoking,
            "symptoms": ", ".join(symps)
        }
        
        row["severity_score"] = compute_triage_severity(row)
        data.append(row)
        
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {num_samples} triage records at {output_path}")
    return df

if __name__ == "__main__":
    generate_triage_dataset()
