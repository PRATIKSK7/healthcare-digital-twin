# Synthetic Patient Data Validation Report

**1. Number of patients generated:** 1000

**2. Missing values:** None

**3. Feature Distributions:**

```
|       |     age |     bmi |   smoking |   heart_rate |   systolic_bp |   diastolic_bp |   respiratory_rate |    spO2 |   temperature |   blood_glucose |   symptom_duration_days |   symptom_severity |   icu_admission_probability |   risk_of_deterioration |   emergency_intervention_probability |   expected_length_of_stay_days |   severity_score |
|:------|--------:|--------:|----------:|-------------:|--------------:|---------------:|-------------------:|--------:|--------------:|----------------:|------------------------:|-------------------:|----------------------------:|------------------------:|-------------------------------------:|-------------------------------:|-----------------:|
| count | 1000    | 1000    |   1000    |      1000    |       1000    |        1000    |            1000    | 1000    |       1000    |         1000    |                 1000    |            1000    |                     1000    |                 1000    |                              1000    |                        1000    |          1000    |
| mean  |   55.33 |   28.2  |      0.19 |       125.4  |        150.44 |          84.74 |              25.74 |   88.96 |         37.94 |          189.8  |                    9.48 |               7.42 |                        0.76 |                    0.73 |                                 0.95 |                          22.42 |            80.9  |
| std   |   17.17 |    5.55 |      0.39 |        12.98 |         16.19 |           7.49 |               4.06 |    2.71 |          0.68 |           34.82 |                    8.62 |               1.74 |                        0.15 |                    0.14 |                                 0.09 |                           4.52 |            12.19 |
| min   |   18    |   18.5  |      0    |        89    |        105    |          61    |              15    |   80    |         36.3  |          105    |                    1    |               2    |                        0.29 |                    0.32 |                                 0.44 |                           9.7  |            35.57 |
| 25%   |   43.38 |   24.18 |      0    |       116    |        139    |          80    |              23    |   87    |         37.4  |          165    |                    2    |               6    |                        0.65 |                    0.64 |                                 0.95 |                          19.4  |            73.74 |
| 50%   |   55.45 |   28    |      0    |       126    |        150    |          85    |              26    |   89    |         37.9  |          188    |                    7    |               7    |                        0.76 |                    0.74 |                                 1    |                          22.3  |            82.3  |
| 75%   |   66.7  |   32    |      0    |       134.25 |        162    |          90    |              28    |   91    |         38.4  |          213    |                   14    |               9    |                        0.87 |                    0.84 |                                 1    |                          25.4  |            89.91 |
| max   |   95    |   45    |      1    |       167    |        202    |         108    |              40    |   96    |         40.2  |          297    |                   30    |              10    |                        1    |                    1    |                                 1    |                          36.5  |           100    |
```

**4. Correlation Matrix (Selected Vitals & Outcomes):**

```
|                           |   heart_rate |   systolic_bp |   respiratory_rate |   spO2 |   temperature |   blood_glucose |   severity_score |   icu_admission_probability |
|:--------------------------|-------------:|--------------:|-------------------:|-------:|--------------:|----------------:|-----------------:|----------------------------:|
| heart_rate                |         1    |          0.31 |               0.55 |  -0.51 |          0.5  |            0.27 |             0.77 |                        0.79 |
| systolic_bp               |         0.31 |          1    |               0.21 |  -0.25 |         -0.08 |            0.53 |             0.41 |                        0.4  |
| respiratory_rate          |         0.55 |          0.21 |               1    |  -0.78 |          0.4  |            0.14 |             0.69 |                        0.75 |
| spO2                      |        -0.51 |         -0.25 |              -0.78 |   1    |         -0.25 |           -0.12 |            -0.7  |                       -0.76 |
| temperature               |         0.5  |         -0.08 |               0.4  |  -0.25 |          1    |            0.03 |             0.38 |                        0.45 |
| blood_glucose             |         0.27 |          0.53 |               0.14 |  -0.12 |          0.03 |            1    |             0.36 |                        0.33 |
| severity_score            |         0.77 |          0.41 |               0.69 |  -0.7  |          0.38 |            0.36 |             1    |                        0.96 |
| icu_admission_probability |         0.79 |          0.4  |               0.75 |  -0.76 |          0.45 |            0.33 |             0.96 |                        1    |
```

**Latent Variable Correlations:**

```
|             |   infection |   dehydration |   respiratory |   metabolic |   cardiac |   neuro |
|:------------|------------:|--------------:|--------------:|------------:|----------:|--------:|
| infection   |        1    |          0.46 |          0.31 |        0.04 |      0.08 |    0.35 |
| dehydration |        0.46 |          1    |          0.17 |        0.05 |      0.13 |    0.42 |
| respiratory |        0.31 |          0.17 |          1    |        0.03 |      0.31 |    0.18 |
| metabolic   |        0.04 |          0.05 |          0.03 |        1    |      0.32 |    0.15 |
| cardiac     |        0.08 |          0.13 |          0.31 |        0.32 |      1    |    0.27 |
| neuro       |        0.35 |          0.42 |          0.18 |        0.15 |      0.27 |    1    |
```

**5. Symptom Frequencies:**
- dizziness: 744 (74.4%)
- fatigue: 689 (68.9%)
- shortness of breath: 658 (65.8%)
- chest pain: 592 (59.2%)
- headache: 571 (57.1%)
- confusion: 538 (53.8%)
- cough: 475 (47.5%)
- vomiting: 304 (30.4%)
- fever: 280 (28.0%)
- abdominal pain: 201 (20.1%)


**6. Severity Score Distribution:**
Min: 35.57, 25th: 73.74, Median: 82.3, 75th: 89.91, Max: 100.0

**7. Outcome Distributions (Mean & Std):**
- icu_admission_probability: Mean=0.76, Std=0.15
- risk_of_deterioration: Mean=0.73, Std=0.14
- emergency_intervention_probability: Mean=0.95, Std=0.09
- expected_length_of_stay_days: Mean=22.42, Std=4.52


**8. Outlier Detection:**
- Extreme Tachycardia (HR > 150): 22
- Extreme Bradycardia (HR < 50): 0
- Severe Hypoxia (SpO2 < 85): 61
- Severe Fever (Temp > 40.0): 1
- Hyperglycemia (Glucose > 300): 0


**9. Clinical Sanity Checks:**
- Correlation between Severity Score and ICU Admission Prob: 0.96 (Expected high)
- Correlation between Heart Rate and SpO2: -0.51 (Expected negative)


**10. Five Example Patient Records with Explanations:**

### Example: High Respiratory Distress
**Age/Gender:** 95.0 Male
**Vitals:** HR: 158, BP: 191/88, RR: 37, SpO2: 80, Temp: 39.4, Glucose: 248
**Symptoms:** chest pain, shortness of breath, fever, cough, dizziness, fatigue, confusion, headache, abdominal pain (Severity: 10, Duration: 5 days)
**Latent Values (Hidden):** Respi=1.00, Infec=0.66, Card=1.00, Neuro=0.94, Metab=0.92
**Simulated Outcomes:** ICU Prob: 1.0, Severity Score: 100.0
**Explanation:** This patient shows high respiratory distress, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. chest pain, shortness of breath, fever, cough, dizziness, fatigue, confusion, headache, abdominal pain) and vitals. The resulting severity score of 100.0 correctly identifies the clinical state without directly looking at vitals.

### Example: Severe Infection/Sepsis
**Age/Gender:** 81.9 Female
**Vitals:** HR: 143, BP: 133/87, RR: 31, SpO2: 87, Temp: 39.9, Glucose: 162
**Symptoms:** shortness of breath, cough, dizziness, vomiting, fatigue, headache, abdominal pain (Severity: 7, Duration: 8 days)
**Latent Values (Hidden):** Respi=0.61, Infec=0.86, Card=0.57, Neuro=0.71, Metab=0.43
**Simulated Outcomes:** ICU Prob: 0.903, Severity Score: 90.14
**Explanation:** This patient shows severe infection/sepsis, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. shortness of breath, cough, dizziness, vomiting, fatigue, headache, abdominal pain) and vitals. The resulting severity score of 90.14 correctly identifies the clinical state without directly looking at vitals.

### Example: Acute Cardiac Event
**Age/Gender:** 46.5 Male
**Vitals:** HR: 124, BP: 160/95, RR: 24, SpO2: 88, Temp: 37.5, Glucose: 244
**Symptoms:** vomiting, fatigue (Severity: 9, Duration: 14 days)
**Latent Values (Hidden):** Respi=0.51, Infec=0.11, Card=1.00, Neuro=0.44, Metab=0.96
**Simulated Outcomes:** ICU Prob: 0.856, Severity Score: 87.8
**Explanation:** This patient shows acute cardiac event, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. vomiting, fatigue) and vitals. The resulting severity score of 87.8 correctly identifies the clinical state without directly looking at vitals.

### Example: Neurological Instability
**Age/Gender:** 82.9 Male
**Vitals:** HR: 138, BP: 182/91, RR: 23, SpO2: 90, Temp: 38.1, Glucose: 198
**Symptoms:** chest pain, shortness of breath, dizziness, fatigue, confusion, abdominal pain (Severity: 10, Duration: 1 days)
**Latent Values (Hidden):** Respi=0.25, Infec=0.30, Card=1.00, Neuro=1.00, Metab=0.53
**Simulated Outcomes:** ICU Prob: 0.912, Severity Score: 93.5
**Explanation:** This patient shows neurological instability, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. chest pain, shortness of breath, dizziness, fatigue, confusion, abdominal pain) and vitals. The resulting severity score of 93.5 correctly identifies the clinical state without directly looking at vitals.

### Example: Stable/Healthy Patient
**Age/Gender:** 28.4 Male
**Vitals:** HR: 91, BP: 144/79, RR: 18, SpO2: 92, Temp: 37.5, Glucose: 121
**Symptoms:** dizziness, fatigue (Severity: 2, Duration: 1 days)
**Latent Values (Hidden):** Respi=0.35, Infec=0.06, Card=0.36, Neuro=0.11, Metab=0.28
**Simulated Outcomes:** ICU Prob: 0.359, Severity Score: 35.57
**Explanation:** This patient shows stable/healthy patient, reflected by the hidden latent variables. This causes the corresponding symptoms (e.g. dizziness, fatigue) and vitals. The resulting severity score of 35.57 correctly identifies the clinical state without directly looking at vitals.
