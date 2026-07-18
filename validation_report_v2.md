# Synthetic Patient Data Validation Report (v2)

**1. Number of patients generated:** 1000

**2. Missing values:** None

**3. Feature Distributions:**

```
|       |     age |     bmi |   smoking |   heart_rate |   systolic_bp |   diastolic_bp |   respiratory_rate |    spO2 |   temperature |   blood_glucose |   symptom_duration_days |   symptom_severity |   icu_admission_probability |   risk_of_deterioration |   emergency_intervention_probability |   expected_length_of_stay_days |   severity_score |
|:------|--------:|--------:|----------:|-------------:|--------------:|---------------:|-------------------:|--------:|--------------:|----------------:|------------------------:|-------------------:|----------------------------:|------------------------:|-------------------------------------:|-------------------------------:|-----------------:|
| count | 1000    | 1000    |   1000    |      1000    |       1000    |        1000    |            1000    | 1000    |       1000    |         1000    |                 1000    |            1000    |                     1000    |                 1000    |                              1000    |                        1000    |          1000    |
| mean  |   55.33 |   28.2  |      0.19 |        87.36 |        129.85 |          81.36 |              18.98 |   95.33 |         37.22 |          114.98 |                    3.03 |               3.47 |                        0.28 |                    0.26 |                                 0.34 |                           6.05 |            35.9  |
| std   |   17.17 |    5.55 |      0.39 |         9.7  |          9.35 |           5.24 |               3.28 |    1.91 |          0.46 |           13.65 |                    2.85 |               2.65 |                        0.19 |                    0.17 |                                 0.21 |                           3.46 |            24.26 |
| min   |   18    |   18.5  |      0    |        66    |        103    |          63    |              11    |   88    |         36.1  |           69    |                    1    |               1    |                        0.02 |                    0.02 |                                 0.04 |                           0    |             0.3  |
| 25%   |   43.38 |   24.18 |      0    |        80    |        123    |          78    |              17    |   94    |         36.9  |          106    |                    1    |               1    |                        0.14 |                    0.13 |                                 0.18 |                           3.5  |            16.64 |
| 50%   |   55.45 |   28    |      0    |        86    |        130    |          81    |              19    |   96    |         37.2  |          114    |                    2    |               3    |                        0.24 |                    0.22 |                                 0.28 |                           5.3  |            29.33 |
| 75%   |   66.7  |   32    |      0    |        93    |        136    |          85    |              21    |   97    |         37.5  |          123    |                    4    |               5    |                        0.38 |                    0.36 |                                 0.46 |                           8    |            52.09 |
| max   |   95    |   45    |      1    |       129    |        158    |          99    |              32    |  100    |         39.1  |          169    |                   24    |              10    |                        1    |                    0.93 |                                 1    |                          20.2  |           100    |
```

**4. Correlation Matrix (Selected Vitals & Outcomes):**

```
|                           |   heart_rate |   systolic_bp |   respiratory_rate |   spO2 |   temperature |   blood_glucose |   severity_score |   icu_admission_probability |
|:--------------------------|-------------:|--------------:|-------------------:|-------:|--------------:|----------------:|-----------------:|----------------------------:|
| heart_rate                |         1    |          0.26 |               0.6  |  -0.57 |          0.6  |            0.34 |             0.81 |                        0.81 |
| systolic_bp               |         0.26 |          1    |               0.19 |  -0.2  |          0.13 |            0.17 |             0.29 |                        0.3  |
| respiratory_rate          |         0.6  |          0.19 |               1    |  -0.65 |          0.51 |            0.27 |             0.75 |                        0.77 |
| spO2                      |        -0.57 |         -0.2  |              -0.65 |   1    |         -0.45 |           -0.32 |            -0.75 |                       -0.78 |
| temperature               |         0.6  |          0.13 |               0.51 |  -0.45 |          1    |            0.22 |             0.63 |                        0.64 |
| blood_glucose             |         0.34 |          0.17 |               0.27 |  -0.32 |          0.22 |            1    |             0.4  |                        0.4  |
| severity_score            |         0.81 |          0.29 |               0.75 |  -0.75 |          0.63 |            0.4  |             1    |                        0.97 |
| icu_admission_probability |         0.81 |          0.3  |               0.77 |  -0.78 |          0.64 |            0.4  |             0.97 |                        1    |
```

**Latent Variable Correlations:**

```
|             |   infection |   dehydration |   respiratory |   metabolic |   cardiac |   neuro |   base_latent |
|:------------|------------:|--------------:|--------------:|------------:|----------:|--------:|--------------:|
| infection   |        1    |          0.75 |          0.69 |        0.58 |      0.68 |    0.65 |          0.82 |
| dehydration |        0.75 |          1    |          0.66 |        0.57 |      0.61 |    0.56 |          0.82 |
| respiratory |        0.69 |          0.66 |          1    |        0.6  |      0.67 |    0.56 |          0.8  |
| metabolic   |        0.58 |          0.57 |          0.6  |        1    |      0.62 |    0.49 |          0.72 |
| cardiac     |        0.68 |          0.61 |          0.67 |        0.62 |      1    |    0.57 |          0.76 |
| neuro       |        0.65 |          0.56 |          0.56 |        0.49 |      0.57 |    1    |          0.67 |
| base_latent |        0.82 |          0.82 |          0.8  |        0.72 |      0.76 |    0.67 |          1    |
```

**5. Symptom Frequencies:**
- fatigue: 244 (24.4%)
- shortness of breath: 183 (18.3%)
- cough: 136 (13.6%)
- fever: 113 (11.3%)
- chest pain: 104 (10.4%)
- dizziness: 90 (9.0%)
- confusion: 74 (7.4%)
- headache: 66 (6.6%)
- vomiting: 57 (5.7%)
- abdominal pain: 28 (2.8%)


**6. Severity Score Distribution:**
- **Healthy (< 35):** 56.4%
- **Medium (35-65):** 29.0%
- **High (65-85):** 10.2%
- **Critical (>= 85):** 4.4%

Min: 0.3, 25th: 16.64, Median: 29.33, 75th: 52.09, Max: 100.0

**7. Outcome Distributions (Mean & Std):**
- icu_admission_probability: Mean=0.28, Std=0.19
- risk_of_deterioration: Mean=0.26, Std=0.17
- emergency_intervention_probability: Mean=0.34, Std=0.21
- expected_length_of_stay_days: Mean=6.05, Std=3.46


**8. Outlier Detection:**
- Extreme Tachycardia (HR > 150): 0
- Extreme Bradycardia (HR < 50): 0
- Severe Hypoxia (SpO2 < 85): 0
- Severe Fever (Temp > 40.0): 0
- Hyperglycemia (Glucose > 300): 0


**9. Clinical Sanity Checks:**
- Correlation between Severity Score and ICU Admission Prob: 0.97 (Expected high)
- Correlation between Heart Rate and SpO2: -0.57 (Expected negative)


**10. Five Example Patient Records with Explanations:**

### Example: High Respiratory Distress
**Age/Gender:** 45.5 Male
**Vitals:** HR: 117, BP: 125/83, RR: 27, SpO2: 90, Temp: 38.1, Glucose: 123
**Symptoms:** shortness of breath, fever, cough, vomiting, fatigue, headache (Severity: 10, Duration: 1 days)
**Latent Values (Hidden):** Respi=0.99, Infec=0.89, Card=0.29, Neuro=0.16, Metab=0.25
**Simulated Outcomes:** ICU Prob: 0.863, Severity Score: 100.0
**Explanation:** This patient shows high respiratory distress, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. shortness of breath, fever, cough, vomiting, fatigue, headache) and vitals. The resulting severity score of 100.0 correctly identifies the clinical state without directly looking at vitals.

### Example: Severe Infection/Sepsis
**Age/Gender:** 74.6 Male
**Vitals:** HR: 98, BP: 128/82, RR: 27, SpO2: 93, Temp: 39.0, Glucose: 132
**Symptoms:** fatigue, confusion (Severity: 10, Duration: 6 days)
**Latent Values (Hidden):** Respi=0.39, Infec=0.98, Card=0.19, Neuro=0.30, Metab=0.49
**Simulated Outcomes:** ICU Prob: 0.605, Severity Score: 87.99
**Explanation:** This patient shows severe infection/sepsis, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. fatigue, confusion) and vitals. The resulting severity score of 87.99 correctly identifies the clinical state without directly looking at vitals.

### Example: Acute Cardiac Event
**Age/Gender:** 74.9 Female
**Vitals:** HR: 117, BP: 142/94, RR: 25, SpO2: 92, Temp: 38.3, Glucose: 124
**Symptoms:** shortness of breath, fever, vomiting, fatigue (Severity: 8, Duration: 2 days)
**Latent Values (Hidden):** Respi=0.53, Infec=0.73, Card=0.81, Neuro=0.38, Metab=0.37
**Simulated Outcomes:** ICU Prob: 0.888, Severity Score: 100.0
**Explanation:** This patient shows acute cardiac event, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. shortness of breath, fever, vomiting, fatigue) and vitals. The resulting severity score of 100.0 correctly identifies the clinical state without directly looking at vitals.

### Example: Neurological Instability
**Age/Gender:** 52.9 Female
**Vitals:** HR: 102, BP: 136/83, RR: 22, SpO2: 92, Temp: 38.6, Glucose: 134
**Symptoms:** confusion (Severity: 8, Duration: 1 days)
**Latent Values (Hidden):** Respi=0.67, Infec=0.53, Card=0.35, Neuro=0.68, Metab=0.51
**Simulated Outcomes:** ICU Prob: 0.834, Severity Score: 92.27
**Explanation:** This patient shows neurological instability, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. confusion) and vitals. The resulting severity score of 92.27 correctly identifies the clinical state without directly looking at vitals.

### Example: Stable/Healthy Patient
**Age/Gender:** 36.9 Male
**Vitals:** HR: 77, BP: 131/81, RR: 18, SpO2: 99, Temp: 36.3, Glucose: 102
**Symptoms:**  (Severity: 1, Duration: 2 days)
**Latent Values (Hidden):** Respi=0.01, Infec=0.02, Card=0.04, Neuro=0.00, Metab=0.01
**Simulated Outcomes:** ICU Prob: 0.024, Severity Score: 0.3
**Explanation:** This patient shows stable/healthy patient, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. ) and vitals. The resulting severity score of 0.3 correctly identifies the clinical state without directly looking at vitals.
