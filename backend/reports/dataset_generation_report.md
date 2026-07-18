# Synthetic Triage Dataset v2 Generation Report

## Overview
- **Total Patients:** 30,000
- **Objective:** Completely rebuilt dataset to eliminate label leakage. Severity scores are derived from simulated clinical outcomes driven by hidden latent physiological variables.

## Distribution
- **Low (0-29.9):** 35.0%
- **Medium (30-59.9):** 35.1%
- **High (60-84.9):** 20.0%
- **Critical (85-100):** 9.9%

## Feature Correlations with Target (Severity Score)
```
severity_score      1.000
heart_rate          0.355
spO2               -0.695
systolic_bp         0.061
symptom_severity    0.670
age                 0.061
```

## Missing Values
```
age                         0
gender                      0
bmi                         0
smoking                     0
heart_rate                  0
systolic_bp                 0
diastolic_bp                0
respiratory_rate            0
spO2                        0
temperature                 0
blood_glucose               0
symptom_duration_days       0
symptom_severity            0
symptoms_list               0
severity_score              0
symp_abdominal_pain         0
symp_anxiety                0
symp_appetite_loss          0
symp_back_pain              0
symp_blurred_vision         0
symp_chest_pain             0
symp_cough                  0
symp_depression             0
symp_diarrhea               0
symp_dizziness              0
symp_fatigue                0
symp_fever                  0
symp_headache               0
symp_insomnia               0
symp_joint_pain             0
symp_muscle_pain            0
symp_nausea                 0
symp_rash                   0
symp_runny_nose             0
symp_shortness_of_breath    0
symp_sneezing               0
symp_sore_throat            0
symp_sweating               0
symp_swelling               0
symp_tremors                0
symp_vomiting               0
symp_weight_gain            0
symp_weight_loss            0
class                       0
```

## Symptom Frequencies
The dataset includes instances of all 28 frontend symptoms.
(0 symptoms were entirely missing in generation).

```
symp_dizziness              16939
symp_fatigue                15324
symp_shortness_of_breath    12283
symp_headache               11587
symp_chest_pain             10415
symp_fever                   8015
symp_nausea                  7995
symp_vomiting                7950
symp_sweating                7601
symp_muscle_pain             4880
symp_blurred_vision          4568
symp_cough                   4485
symp_tremors                 3797
symp_runny_nose              1251
symp_insomnia                1229
symp_weight_gain             1220
symp_abdominal_pain          1217
symp_depression              1208
symp_appetite_loss           1203
symp_joint_pain              1200
symp_diarrhea                1191
symp_back_pain               1189
symp_sneezing                1187
symp_anxiety                 1186
symp_weight_loss             1173
symp_swelling                1164
symp_sore_throat             1137
symp_rash                    1130
```
