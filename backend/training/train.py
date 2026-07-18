import pandas as pd
import numpy as np
import os
import json
import uuid
import joblib
import warnings
from datetime import datetime
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor

warnings.filterwarnings('ignore')

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from preprocessing.pipeline import DataPreprocessor
from utils.triage_data_generator import generate_triage_dataset

def get_base_models(random_state=42):
    return {
        'Ridge': Ridge(random_state=random_state),
        'RandomForest': RandomForestRegressor(random_state=random_state),
        'ExtraTrees': ExtraTreesRegressor(random_state=random_state),
        'GradientBoosting': GradientBoostingRegressor(random_state=random_state),
        'XGBoost': xgb.XGBRegressor(random_state=random_state),
        'LightGBM': lgb.LGBMRegressor(random_state=random_state, verbose=-1),
        'CatBoost': CatBoostRegressor(random_state=random_state, verbose=0)
    }

def train_triage_pipeline():
    print("🚀 Starting Triage Auto-ML Pipeline (Regression)...")
    
    # 1. Load Data
    data_path = 'backend/datasets/triage_dataset.csv'
    if not os.path.exists(data_path):
        print("Data not found. Generating synthetic triage dataset...")
        df = generate_triage_dataset(num_samples=5000, output_path=data_path)
    else:
        df = pd.read_csv(data_path)
        
    # 2. Train/Test Split
    print("✂️ Splitting data...")
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

    # 3. Preprocessing
    print("⚙️ Running Preprocessing (Cleaning, Imputation, Scaling)...")
    preprocessor = DataPreprocessor()
    X_train, y_train, _ = preprocessor.fit_transform(df_train, target_col='severity_score')
    
    # 4. Model Arena
    print("⚔️ Entering Model Arena: Evaluating Regression Models...")
    models = get_base_models()
    results = {}
    
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    
    for name, model in models.items():
        print(f"Evaluating {name}...")
        
        metrics = []
        for train_idx, val_idx in cv.split(X_train):
            X_fold_train, X_fold_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
            y_fold_train, y_fold_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
            
            model.fit(X_fold_train, y_fold_train)
            y_pred = model.predict(X_fold_val)
            rmse = np.sqrt(mean_squared_error(y_fold_val, y_pred))
            r2 = r2_score(y_fold_val, y_pred)
            metrics.append((rmse, r2))
            
        avg_rmse = np.mean([m[0] for m in metrics])
        avg_r2 = np.mean([m[1] for m in metrics])
        
        # Train on full train set for final testing
        model.fit(X_train, y_train)
        
        results[name] = {
            'rmse': avg_rmse,
            'r2': avg_r2,
            'model_instance': model
        }

    # 5. Select Champion Model
    sorted_models = sorted(results.items(), key=lambda x: x[1]['rmse']) # Lower RMSE is better
    champion_name = sorted_models[0][0]
    champion_info = sorted_models[0][1]
    champion_model = champion_info['model_instance']
    
    print(f"👑 Champion Model Selected: {champion_name} (RMSE: {champion_info['rmse']:.4f}, R²: {champion_info['r2']:.4f})")
    
    # 6. Final Evaluation on Test Set
    print("📊 Evaluating Champion Model on Test Set...")
    X_test = preprocessor.transform(df_test)
    y_test = df_test['severity_score']
    
    y_pred = champion_model.predict(X_test)
    
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    test_mae = mean_absolute_error(y_test, y_pred)
    test_r2 = r2_score(y_test, y_pred)
    
    print(f"Test RMSE: {test_rmse:.4f}")
    print(f"Test MAE:  {test_mae:.4f}")
    print(f"Test R²:   {test_r2:.4f}")
    
    # 7. Save Model & Preprocessor
    version_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    version_dir = f"backend/models/versions/{version_id}"
    os.makedirs(version_dir, exist_ok=True)
    
    model_path = os.path.join(version_dir, "calibrated_model.joblib")
    joblib.dump(champion_model, model_path)
    
    preprocessor_path = os.path.join(version_dir, "preprocessor.joblib")
    preprocessor.save(preprocessor_path)
    
    report = {
        "version": version_id,
        "champion_model": champion_name,
        "arena_results": {k: {"rmse": v["rmse"], "r2": v["r2"]} for k, v in results.items()},
        "final_test_metrics": {
            "test_rmse": test_rmse,
            "test_mae": test_mae,
            "test_r2": test_r2
        }
    }
    
    os.makedirs("backend/reports", exist_ok=True)
    report_path = f"backend/reports/comparison_report_{version_id}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"✅ Pipeline Complete! Champion Model: {champion_name} (Version: {version_id})")
    print(f"📁 Artifacts: {version_dir}")
    print(f"📄 Report: {report_path}")

if __name__ == "__main__":
    train_triage_pipeline()
