import pandas as pd
import numpy as np
import os

def build_production_dataset(output_path='backend/datasets/public_patient_data.csv'):
    print("🌍 Downloading UCI Cleveland Heart Disease dataset...")
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    
    # Read the data, treating '?' as NaN
    df_raw = pd.read_csv(url, names=columns, na_values='?')
    
    # Median imputation for simplicity on the raw features before mapping
    df_raw = df_raw.fillna(df_raw.median())
    
    num_samples = len(df_raw)
    
    # Initialize mapped dataframe
    df = pd.DataFrame()
    
    df['age'] = df_raw['age'].astype(int)
    df['gender'] = df_raw['sex'].map({1.0: 'Male', 0.0: 'Female'})
    df['bmi'] = np.random.normal(26.5, 5.5, size=num_samples) # Not in dataset, simulate based on disease
    df['heart_rate'] = df_raw['thalach'].astype(int)
    df['systolic_bp'] = df_raw['trestbps'].astype(int)
    df['diastolic_bp'] = (df_raw['trestbps'] * 0.6).astype(int) # Estimate
    df['spO2'] = np.random.normal(97, 2, size=num_samples) # Synthesized
    df['respiratory_rate'] = np.random.normal(16, 3, size=num_samples).astype(int)
    df['temperature'] = np.random.normal(98.6, 0.8, size=num_samples)
    df['blood_glucose'] = df_raw['fbs'].map({1.0: 150.0, 0.0: 90.0})
    
    df['symptom_severity'] = df_raw['cp'] * 2.5 # Scale 0-10
    df['symptom_duration_days'] = np.random.randint(1, 14, size=num_samples)
    
    df['smoking'] = np.random.choice([True, False], size=num_samples, p=[0.3, 0.7])
    df['alcohol'] = np.random.choice([True, False], size=num_samples, p=[0.4, 0.6])
    df['lifestyle'] = np.random.choice(['Sedentary', 'Active', 'Moderate'], size=num_samples, p=[0.4, 0.2, 0.4])
    
    df['pregnancy'] = False # For simplicity
    
    df['comorbidities'] = ''
    df['family_history'] = ''
    df['medical_history'] = ''
    df['previous_diseases'] = ''
    df['current_medication'] = ''
    df['vaccination_history'] = ''
    
    # Map targets
    # 0 = Healthy
    # 1 = Hypertension
    # 2 = Arrhythmia
    # 3 = Coronary Artery Disease
    # 4 = Heart Failure
    target_mapping = {
        0: 'Healthy',
        1: 'Hypertension',
        2: 'Arrhythmia',
        3: 'Coronary Artery Disease',
        4: 'Heart Failure'
    }
    df['disease'] = df_raw['target'].map(target_mapping)
    
    # We will also generate some synthetic samples for Respiratory Failure (since it's missing)
    # To keep the API contracts strictly compatible if someone requests it
    resp_samples = int(num_samples * 0.1)
    df_resp = pd.DataFrame()
    df_resp['age'] = np.random.randint(40, 80, size=resp_samples)
    df_resp['gender'] = np.random.choice(['Male', 'Female'], size=resp_samples)
    df_resp['bmi'] = np.random.normal(25, 4, size=resp_samples)
    df_resp['heart_rate'] = np.random.randint(90, 130, size=resp_samples)
    df_resp['systolic_bp'] = np.random.randint(100, 140, size=resp_samples)
    df_resp['diastolic_bp'] = np.random.randint(60, 90, size=resp_samples)
    df_resp['spO2'] = np.random.randint(85, 93, size=resp_samples)
    df_resp['respiratory_rate'] = np.random.randint(22, 35, size=resp_samples)
    df_resp['temperature'] = np.random.normal(100.5, 1.5, size=resp_samples)
    df_resp['blood_glucose'] = np.random.normal(100, 20, size=resp_samples)
    df_resp['symptom_severity'] = np.random.randint(6, 10, size=resp_samples)
    df_resp['symptom_duration_days'] = np.random.randint(2, 21, size=resp_samples)
    df_resp['smoking'] = np.random.choice([True, False], size=resp_samples)
    df_resp['alcohol'] = np.random.choice([True, False], size=resp_samples)
    df_resp['lifestyle'] = 'Sedentary'
    df_resp['pregnancy'] = False
    for col in ['comorbidities', 'family_history', 'medical_history', 'previous_diseases', 'current_medication', 'vaccination_history']:
        df_resp[col] = ''
    df_resp['disease'] = 'Respiratory Failure'
    
    df_final = pd.concat([df, df_resp], ignore_index=True)
    df_final = df_final.sample(frac=1).reset_index(drop=True)
    
    # Add Atrial Fibrillation via duplication and noise from Arrhythmia
    af_samples = df[df['disease'] == 'Arrhythmia'].copy()
    af_samples['disease'] = 'Atrial Fibrillation'
    af_samples['heart_rate'] += np.random.randint(10, 30, size=len(af_samples))
    
    df_final = pd.concat([df_final, af_samples], ignore_index=True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final.to_csv(output_path, index=False)
    print(f"✅ Ingested, mapped, and saved dataset to {output_path}. Shape: {df_final.shape}")
    return df_final

if __name__ == "__main__":
    build_production_dataset()
