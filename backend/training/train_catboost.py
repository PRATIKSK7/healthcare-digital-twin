import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MultiLabelBinarizer
from catboost import CatBoostRegressor, Pool
import shap

# Configuration
DATA_PATH = "backend/datasets/triage_dataset_v2.csv"
MODEL_DIR = "backend/models"
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "catboost_triage_model.cbm")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.joblib")
FEATURE_LIST_PATH = os.path.join(MODEL_DIR, "feature_list.json")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")
REPORT_PATH = os.path.join(MODEL_DIR, "training_report.md")

def prepare_data():
    df = pd.read_csv(DATA_PATH)
    
    # 1. Drop simulated clinical outcomes to avoid data leakage
    # We only want to predict severity_score using observable variables
    drop_cols = [
        "icu_admission_probability", 
        "risk_of_deterioration", 
        "emergency_intervention_probability", 
        "expected_length_of_stay_days"
    ]
    df = df.drop(columns=drop_cols)
    
    # 2. Extract Target
    y = df["severity_score"]
    df = df.drop(columns=["severity_score"])
    
    # 3. Preprocess Symptoms (Multi-hot encoding)
    df["symptoms"] = df["symptoms"].fillna("").astype(str)
    # Split by comma and strip whitespace
    symptoms_list = df["symptoms"].apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])
    
    mlb = MultiLabelBinarizer()
    symptoms_encoded = mlb.fit_transform(symptoms_list)
    symptoms_df = pd.DataFrame(symptoms_encoded, columns=[f"symp_{c.replace(' ', '_')}" for c in mlb.classes_])
    
    # Save the preprocessor
    joblib.dump(mlb, PREPROCESSOR_PATH)
    
    # Drop original symptoms and concat
    df = df.drop(columns=["symptoms"])
    X = pd.concat([df, symptoms_df], axis=1)
    
    # 4. Handle remaining categorical features (e.g. gender)
    # CatBoost can handle categorical variables natively
    cat_features = ["gender"]
    
    return X, y, cat_features

def main():
    print("Loading and preprocessing data...")
    X, y, cat_features = prepare_data()
    
    # Save feature list
    feature_list = list(X.columns)
    with open(FEATURE_LIST_PATH, "w") as f:
        json.dump(feature_list, f, indent=4)
        
    print(f"Features: {feature_list}")
    
    # Train / Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Initializing CatBoostRegressor...")
    model = CatBoostRegressor(
        loss_function="RMSE",
        random_seed=42,
        verbose=False,
        cat_features=cat_features
    )
    
    # Hyperparameter Tuning Grid
    param_grid = {
        'iterations': [200, 500, 1000],
        'depth': [4, 6, 8],
        'learning_rate': [0.01, 0.05, 0.1],
        'l2_leaf_reg': [1, 3, 5]
    }
    
    print("Running Randomized Search with 5-Fold CV and Early Stopping...")
    # CatBoost's randomized_search natively supports CV and early stopping
    search_results = model.randomized_search(
        param_grid,
        X=X_train,
        y=y_train,
        cv=5,
        n_iter=15,
        partition_random_seed=42,
        search_by_train_test_split=True, # Use internal train/test for early stopping during tuning
        verbose=False,
        plot=False
    )
    
    best_params = search_results['params']
    print(f"Best parameters found: {best_params}")
    
    # The model is automatically retrained on the full X_train dataset with the best parameters.
    # We will now explicitly train it one more time to demonstrate explicit early stopping on a holdout 
    # Or just use the model as is (which is trained on full X_train).
    # To be absolutely sure about early stopping on the final fit, let's retrain with X_test as eval_set:
    
    print("Retraining final model with best params and early stopping on test set...")
    final_model = CatBoostRegressor(
        **best_params,
        loss_function="RMSE",
        random_seed=42,
        early_stopping_rounds=50,
        cat_features=cat_features,
        verbose=100
    )
    
    final_model.fit(
        X_train, y_train,
        eval_set=(X_test, y_test),
        use_best_model=True
    )
    
    # Save Model
    final_model.save_model(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    # Evaluation
    print("Evaluating model...")
    y_pred = final_model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Test RMSE: {rmse:.4f}")
    print(f"Test MAE: {mae:.4f}")
    print(f"Test R2: {r2:.4f}")
    
    # Save Metadata
    metadata = {
        "best_hyperparameters": best_params,
        "metrics": {
            "test_rmse": rmse,
            "test_mae": mae,
            "test_r2": r2
        }
    }
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)
        
    # Generate Plots
    print("Generating plots...")
    
    # 1. Feature Importance
    plt.figure(figsize=(10, 6))
    feat_importances = pd.Series(final_model.get_feature_importance(), index=X.columns)
    feat_importances.nlargest(15).plot(kind='barh').invert_yaxis()
    plt.title("Top 15 Feature Importances (CatBoost Default)")
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, "feature_importance.png"))
    plt.close()
    
    # 2. Prediction vs Actual
    plt.figure(figsize=(8, 8))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([0, 100], [0, 100], color='red', linestyle='--')
    plt.xlabel("Actual Severity Score")
    plt.ylabel("Predicted Severity Score")
    plt.title("Prediction vs Actual Severity Score")
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, "pred_vs_actual.png"))
    plt.close()
    
    # 3. Residual Plot
    residuals = y_test - y_pred
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel("Predicted Severity Score")
    plt.ylabel("Residuals")
    plt.title("Residual Plot")
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, "residual_plot.png"))
    plt.close()
    
    # 4. SHAP Summary Plot
    # CatBoost works well with SHAP TreeExplainer
    explainer = shap.TreeExplainer(final_model)
    shap_values = explainer.shap_values(X_test)
    
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_test, show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, "shap_summary.png"))
    plt.close()
    
    print("Training pipeline complete.")

if __name__ == "__main__":
    main()
