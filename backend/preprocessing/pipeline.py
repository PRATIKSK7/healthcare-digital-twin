import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import VarianceThreshold
from imblearn.over_sampling import SMOTE
import joblib
import os

class DataPreprocessor:
    def __init__(self):
        self.numerical_cols = [
            'age', 'bmi', 'heart_rate', 'systolic_bp', 
            'spO2', 'temperature', 'blood_glucose',
            'symptom_duration_days', 'symptom_severity'
        ]
        
        self.categorical_cols = ['gender']
        self.boolean_cols = ['smoking']
        self.list_cols = ['symptoms']
        
        self.numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', RobustScaler())
        ])
        
        self.categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        # Booleans just get imputed if missing, they remain 0/1
        self.boolean_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent'))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', self.numeric_transformer, self.numerical_cols),
                ('cat', self.categorical_transformer, self.categorical_cols),
                ('bool', self.boolean_transformer, self.boolean_cols)
            ])
            
        self.label_encoder = LabelEncoder()
        
    def _process_lists(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts comma-separated list columns into a simple integer count of items.
        (Advanced implementation could use MultiLabelBinarizer for specific diseases)
        """
        for col in self.list_cols:
            if col in df.columns:
                # Count the number of items in the list (or string representation of list in CSV)
                df[f'{col}_count'] = df[col].apply(lambda x: len(str(x).split(',')) if pd.notnull(x) and str(x).strip() != '' else 0)
                if f'{col}_count' not in self.numerical_cols:
                    self.numerical_cols.append(f'{col}_count')
        # Drop original list columns
        df = df.drop(columns=[col for col in self.list_cols if col in df.columns], errors='ignore')
        return df

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        initial_len = len(df)
        df = df.drop_duplicates()
        if initial_len - len(df) > 0:
            print(f"Removed {initial_len - len(df)} duplicate rows.")
        return df
        
    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in ['heart_rate', 'systolic_bp', 'diastolic_bp', 'spO2', 'temperature', 'blood_glucose']:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                df[col] = np.clip(df[col], Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
        return df

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'systolic_bp' in df.columns and 'diastolic_bp' in df.columns:
            df['pulse_pressure'] = df['systolic_bp'] - df['diastolic_bp']
            if 'pulse_pressure' not in self.numerical_cols:
                self.numerical_cols.append('pulse_pressure')
        
        # Convert booleans to int explicitly if they are bools
        for col in self.boolean_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)
                
        return df

    def fit_transform(self, df: pd.DataFrame, target_col: str):
        """
        Fits the preprocessor and transforms the data. Returns X (DataFrame), y (Series).
        Does NOT apply SMOTE because we are doing regression on severity_score.
        """
        # Feature Engineering: List to count
        df = self._process_lists(df)
        
        y = df[target_col]
        X = df.drop(columns=[target_col])
        
        # Ensure all expected columns are present (fill missing cols with 0 or NaN as appropriate before transform)
        for col in self.numerical_cols + self.categorical_cols + self.boolean_cols:
            if col not in X.columns:
                X[col] = np.nan
        
        # Fit and transform features
        X_processed = self.preprocessor.fit_transform(X)
        
        # Get feature names after one-hot encoding
        cat_feature_names = self.preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(self.categorical_cols).tolist()
        feature_names = self.numerical_cols + cat_feature_names + self.boolean_cols
        
        X_df = pd.DataFrame(X_processed, columns=feature_names)
        
        # Remove zero-variance features
        self.variance_selector = VarianceThreshold(threshold=0.0)
        X_selected = self.variance_selector.fit_transform(X_df)
        
        final_feature_names = X_df.columns[self.variance_selector.get_support()]
        X_final = pd.DataFrame(X_selected, columns=final_feature_names)
        
        self.feature_names = final_feature_names.tolist()
        
        return X_final, y, None

    def transform(self, df: pd.DataFrame):
        df = self._process_lists(df)
        df = self.engineer_features(df)
        
        # Ensure only known features are selected before preprocessing
        
        X_processed = self.preprocessor.transform(df)
        
        cat_feature_names = self.preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(self.categorical_cols).tolist()
        all_feature_names = self.numerical_cols + cat_feature_names + self.boolean_cols
        
        X_df = pd.DataFrame(X_processed, columns=all_feature_names)
        
        # Apply selector
        X_df = pd.DataFrame(self.variance_selector.transform(X_df), columns=self.feature_names)
        
        return X_df

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            'preprocessor': self.preprocessor,
            'selector': getattr(self, 'variance_selector', None),
            'feature_names': self.feature_names,
            'label_encoder': None
        }, filepath)
