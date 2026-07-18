import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

df = pd.read_csv('backend/datasets/synthetic_patient_data.csv')

report = {}
report['samples'] = len(df)
report['features'] = len(df.columns) - 1
report['diseases'] = df['disease'].nunique()
report['missing_values'] = int(df.isnull().sum().sum())
report['duplicate_rows'] = int(df.duplicated().sum())

class_dist = df['disease'].value_counts().to_dict()
report['class_imbalance'] = class_dist

# Feature importance using Random Forest
X = df.drop(columns=['disease'])
y = df['disease']

# Encode categorical variables for RF
X_encoded = pd.get_dummies(X)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

rf = RandomForestClassifier(random_state=42, n_estimators=50)
rf.fit(X_encoded, y_encoded)

importances = dict(zip(X_encoded.columns, rf.feature_importances_))
importances = {k: float(v) for k, v in sorted(importances.items(), key=lambda item: item[1], reverse=True)}

report['feature_importance'] = importances
report['strong_features'] = [k for k, v in importances.items() if v > 0.05]
report['weak_features'] = [k for k, v in importances.items() if v < 0.01]

# Save report
with open('backend/datasets/audit_report.json', 'w') as f:
    json.dump(report, f, indent=4)

print("Audit complete.")
