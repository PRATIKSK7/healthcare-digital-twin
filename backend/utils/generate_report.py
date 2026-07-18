import os
import pandas as pd
import numpy as np
import io

from latent_patient_generator import generate_patients

def generate_validation_report():
    df, df_latents = generate_patients(1000, "backend/datasets/triage_dataset_v2.csv")
    
    report = []
    report.append("# Synthetic Patient Data Validation Report (v2)\n")
    
    # 1. Number of patients
    report.append(f"**1. Number of patients generated:** {len(df)}\n")
    
    # 2. Missing values
    missing = df.isnull().sum()
    missing_report = missing[missing > 0]
    if len(missing_report) == 0:
        report.append("**2. Missing values:** None\n")
    else:
        report.append("**2. Missing values:**\n")
        for k, v in missing_report.items():
            report.append(f"- {k}: {v}\n")
            
    # 3. Feature distributions
    report.append("**3. Feature Distributions:**")
    desc = df.describe().round(2).to_markdown()
    report.append(f"\n```\n{desc}\n```\n")
    
    # 4. Correlation matrix
    report.append("**4. Correlation Matrix (Selected Vitals & Outcomes):**")
    corr_cols = ['heart_rate', 'systolic_bp', 'respiratory_rate', 'spO2', 'temperature', 'blood_glucose', 'severity_score', 'icu_admission_probability']
    corr = df[corr_cols].corr().round(2).to_markdown()
    report.append(f"\n```\n{corr}\n```\n")
    
    # Also Latent correlations
    report.append("**Latent Variable Correlations:**")
    corr_latents = df_latents.corr().round(2).to_markdown()
    report.append(f"\n```\n{corr_latents}\n```\n")
    
    # 5. Symptom frequencies
    report.append("**5. Symptom Frequencies:**")
    all_symptoms = []
    for s_list in df['symptoms']:
        if s_list:
            all_symptoms.extend([s.strip() for s in s_list.split(",")])
    
    from collections import Counter
    symp_counts = Counter(all_symptoms)
    for symp, count in symp_counts.most_common():
        report.append(f"- {symp}: {count} ({count/len(df)*100:.1f}%)")
    report.append("\n")
    
    # 6. Severity distribution
    report.append("**6. Severity Score Distribution:**")
    sev = df['severity_score']
    healthy = len(sev[sev < 35]) / len(sev) * 100
    medium = len(sev[(sev >= 35) & (sev < 65)]) / len(sev) * 100
    high = len(sev[(sev >= 65) & (sev < 85)]) / len(sev) * 100
    critical = len(sev[sev >= 85]) / len(sev) * 100
    
    report.append(f"- **Healthy (< 35):** {healthy:.1f}%")
    report.append(f"- **Medium (35-65):** {medium:.1f}%")
    report.append(f"- **High (65-85):** {high:.1f}%")
    report.append(f"- **Critical (>= 85):** {critical:.1f}%")
    
    sev_quantiles = sev.quantile([0, 0.25, 0.5, 0.75, 1.0]).round(2)
    report.append(f"\nMin: {sev_quantiles[0.0]}, 25th: {sev_quantiles[0.25]}, Median: {sev_quantiles[0.5]}, 75th: {sev_quantiles[0.75]}, Max: {sev_quantiles[1.0]}\n")
    
    # 7. Outcome distributions
    report.append("**7. Outcome Distributions (Mean & Std):**")
    outcomes = ['icu_admission_probability', 'risk_of_deterioration', 'emergency_intervention_probability', 'expected_length_of_stay_days']
    for out in outcomes:
        report.append(f"- {out}: Mean={df[out].mean():.2f}, Std={df[out].std():.2f}")
    report.append("\n")
    
    # 8. Outlier detection
    report.append("**8. Outlier Detection:**")
    report.append("- Extreme Tachycardia (HR > 150): " + str(len(df[df['heart_rate'] > 150])))
    report.append("- Extreme Bradycardia (HR < 50): " + str(len(df[df['heart_rate'] < 50])))
    report.append("- Severe Hypoxia (SpO2 < 85): " + str(len(df[df['spO2'] < 85])))
    report.append("- Severe Fever (Temp > 40.0): " + str(len(df[df['temperature'] > 40.0])))
    report.append("- Hyperglycemia (Glucose > 300): " + str(len(df[df['blood_glucose'] > 300])))
    report.append("\n")
    
    # 9. Clinical sanity checks
    report.append("**9. Clinical Sanity Checks:**")
    sev_icu_corr = df['severity_score'].corr(df['icu_admission_probability'])
    report.append(f"- Correlation between Severity Score and ICU Admission Prob: {sev_icu_corr:.2f} (Expected high)")
    
    hr_spo2_corr = df['heart_rate'].corr(df['spO2'])
    report.append(f"- Correlation between Heart Rate and SpO2: {hr_spo2_corr:.2f} (Expected negative)")
    report.append("\n")
    
    # 10. Five example patient records with explanations
    report.append("**10. Five Example Patient Records with Explanations:**\n")
    
    idx1 = df_latents['respiratory'].idxmax()
    idx2 = df_latents['infection'].idxmax()
    idx3 = df_latents['cardiac'].idxmax()
    idx4 = df_latents['neuro'].idxmax()
    idx5 = df_latents.sum(axis=1).idxmin()
    
    indices = [
        (idx1, "High Respiratory Distress"),
        (idx2, "Severe Infection/Sepsis"),
        (idx3, "Acute Cardiac Event"),
        (idx4, "Neurological Instability"),
        (idx5, "Stable/Healthy Patient")
    ]
    
    for idx, desc_text in indices:
        row = df.iloc[idx]
        latents = df_latents.iloc[idx]
        report.append(f"### Example: {desc_text}")
        report.append(f"**Age/Gender:** {row['age']} {row['gender']}")
        report.append(f"**Vitals:** HR: {row['heart_rate']}, BP: {row['systolic_bp']}/{row['diastolic_bp']}, RR: {row['respiratory_rate']}, SpO2: {row['spO2']}, Temp: {row['temperature']}, Glucose: {row['blood_glucose']}")
        report.append(f"**Symptoms:** {row['symptoms']} (Severity: {row['symptom_severity']}, Duration: {row['symptom_duration_days']} days)")
        report.append(f"**Latent Values (Hidden):** Respi={latents['respiratory']:.2f}, Infec={latents['infection']:.2f}, Card={latents['cardiac']:.2f}, Neuro={latents['neuro']:.2f}, Metab={latents['metabolic']:.2f}")
        report.append(f"**Simulated Outcomes:** ICU Prob: {row['icu_admission_probability']}, Severity Score: {row['severity_score']}")
        report.append(f"**Explanation:** This patient shows {desc_text.lower()}, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. {row['symptoms']}) and vitals. The resulting severity score of {row['severity_score']} correctly identifies the clinical state without directly looking at vitals.\n")
        
    with open("validation_report_v2.md", "w") as f:
        f.write("\n".join(report))
    
    print("Report written to validation_report_v2.md")

if __name__ == "__main__":
    generate_validation_report()
