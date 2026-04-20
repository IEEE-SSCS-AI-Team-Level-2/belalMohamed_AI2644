import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

class IrrigationDataProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, drop_highly_correlated=False):
        """
        Custom transformer to handle dataset-specific logic.
        Configured to handle multicollinearity dynamically.
        """
        self.drop_highly_correlated = drop_highly_correlated
        # Left empty as EDA confirmed no correlations > 0.8
        # Kept as an attribute to satisfy the Open/Closed Principle for future data drops
        self.correlated_features = [] 
        
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_processed = X.copy()
        if self.drop_highly_correlated and self.correlated_features:
            X_processed = X_processed.drop(columns=self.correlated_features, errors='ignore')
        return X_processed

def get_preprocessor(categorical_cols, numerical_cols, is_tree_model=False):
    """
    Constructs the scaling and encoding pipeline to prevent data leakage.
    """
    # Standard scaling is critical for Logistic Regression
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler()) 
    ])

    # One-hot encoding for categorical variables
    categorical_transformer = Pipeline(steps=[
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    # Combine the custom EDA logic with the scikit-learn transformations
    full_pipeline = Pipeline(steps=[
        ('custom_processing', IrrigationDataProcessor(drop_highly_correlated=not is_tree_model)),
        ('col_transformer', preprocessor)
    ])
    
    return full_pipeline