# CatBoost V2 Final Training Report

## Hyperparameters
**Search Strategy:** RandomizedSearchCV (10 iterations, 5-Fold CV)
**Best Parameters:**
```json
{
  "random_strength": 0.1,
  "learning_rate": 0.01,
  "l2_leaf_reg": 10,
  "iterations": 1500,
  "depth": 6,
  "bagging_temperature": 1.0
}
```

## Cross Validation Results
- **CV Mean R²:** 0.8482
- **CV Std R²:** 0.0033

## Final Test Set Metrics (80/20 Split)
- **RMSE:** 9.4646
- **MAE:** 7.1913
- **R² Score:** 0.8470

## Top 10 Feature Importances
```
                feature  importance
8                  spO2   46.004807
5            heart_rate   17.806886
38     symptom_severity   10.542102
40          temperature    9.762736
39          systolic_bp    6.491577
6      respiratory_rate    2.103967
18       symp_dizziness    1.719208
21        symp_headache    1.313820
0                   age    0.709951
13  symp_blurred_vision    0.706283
```
*(See `feature_importance_v2.png` and `shap_summary_v2.png` for visualizations)*

## Clinical Validation Scenarios
| Scenario | Predicted Severity (0-100) |
| :--- | :--- |
| Healthy Adult | 24.04 |
| Moderate Infection | 34.72 |
| Hypertension | 44.29 |
| Respiratory Distress | 82.80 |
| Acute Cardiac Emergency | 88.90 |
| Elderly Frail | 41.10 |

## Sensitivity Tests (Isolated Feature Changes)
| Scenario | Predicted Severity |
| :--- | :--- |
| Base Patient | 24.04 |
| HR 70 -> 170 | 52.84 |
| SpO2 98 -> 82 | 74.19 |
| SBP 120 -> 220 | 41.62 |
| Shortness of Breath (On) | 24.73 |

## Final Recommendation
**READY FOR PRODUCTION.** 
The model successfully learned the latent physiological relationships from the V2 dataset without exploiting artificial label leakage. Vitals and symptoms independently drive realistic clinical outcomes. The `.cbm`, `.json`, and `.joblib` artifacts are safely stored in `backend/models/`.
