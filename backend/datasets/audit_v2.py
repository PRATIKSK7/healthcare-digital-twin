import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('backend/datasets/triage_dataset_v2.csv')

print("=== PHASE 1: Dataset Integrity ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print(f"Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"Duplicate rows: {df.duplicated().sum()}")

invalid_vitals = {
    'spO2 > 100': (df['spO2'] > 100).sum(),
    'HR < 20': (df['heart_rate'] < 20).sum(),
    'Temp > 45': (df['temperature'] > 45).sum(),
    'Temp < 32': (df['temperature'] < 32).sum(),
    'SBP < 0': (df['systolic_bp'] < 0).sum(),
    'DBP < 0': (df['diastolic_bp'] < 0).sum(),
    'SBP < DBP': (df['systolic_bp'] < df['diastolic_bp']).sum()
}
print(f"Invalid values: {invalid_vitals}")

print("\n=== PHASE 2: Distribution Analysis ===")
cols_to_analyze = ['age', 'heart_rate', 'systolic_bp', 'diastolic_bp', 'respiratory_rate', 'temperature', 'spO2', 'blood_glucose', 'bmi', 'severity_score']
print(df[cols_to_analyze].describe().T[['mean', '50%', 'std', 'min', 'max']].to_string())

print("\n=== PHASE 3: Symptom Analysis ===")
symp_cols = [c for c in df.columns if c.startswith('symp_')]
symp_freq = df[symp_cols].sum().sort_values(ascending=False)
print("Symptom Frequencies:")
print(symp_freq.to_string())
print(f"Never occurring: {(symp_freq == 0).sum()}")

print("\n=== PHASE 4 & 5: Correlation Analysis & Leakage ===")
numeric_cols = df.select_dtypes(include=[np.number]).columns
pearson_corr = df[numeric_cols].corr(method='pearson')['severity_score'].sort_values(ascending=False)
spearman_corr = df[numeric_cols].corr(method='spearman')['severity_score'].sort_values(ascending=False)
print("Top 10 Pearson Correlates with Severity:")
print(pearson_corr.head(10).to_string())
print("\nBottom 5 Pearson Correlates with Severity:")
print(pearson_corr.tail(5).to_string())

print("\nTop 10 Spearman Correlates with Severity:")
print(spearman_corr.head(10).to_string())

print("\n=== PHASE 6: Clinical Relationship Audit ===")
# Define some clinical groups and get mean severity
high_hr = df[df['heart_rate'] > 120]['severity_score'].mean()
low_spo2 = df[df['spO2'] < 92]['severity_score'].mean()
high_rr = df[df['respiratory_rate'] > 24]['severity_score'].mean()
chest_pain = df[df['symp_chest_pain'] == 1]['severity_score'].mean()
sob = df[df['symp_shortness_of_breath'] == 1]['severity_score'].mean()
fever = df[df['symp_fever'] == 1]['severity_score'].mean()
smoking = df[df['smoking'] == 1]['severity_score'].mean()
non_smoking = df[df['smoking'] == 0]['severity_score'].mean()

base_severity = df['severity_score'].mean()
print(f"Base Severity: {base_severity:.2f}")
print(f"High HR (>120) Severity: {high_hr:.2f}")
print(f"Low SpO2 (<92) Severity: {low_spo2:.2f}")
print(f"High RR (>24) Severity: {high_rr:.2f}")
print(f"Chest Pain Severity: {chest_pain:.2f}")
print(f"Shortness of Breath Severity: {sob:.2f}")
print(f"Fever Severity: {fever:.2f}")
print(f"Smoking Severity: {smoking:.2f} vs Non-smoking: {non_smoking:.2f}")

print("\n=== PHASE 7: Severity Distribution ===")
def get_class(s):
    if s >= 85: return "Critical"
    if s >= 60: return "High"
    if s >= 30: return "Medium"
    return "Low"
df['class'] = df['severity_score'].apply(get_class)
dist = df['class'].value_counts(normalize=True) * 100
print(dist.to_string())
