import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import balanced_accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from preprocessing import get_preprocessor

def plot_feature_importance(pipeline, numerical_cols, categorical_cols):
    """
    Extracts and visualizes the feature importance from the optimized pipeline.
    """
    print("\nExtracting Feature Importance...")
    
    # Extract the trained preprocessor and the classifier from the pipeline
    preprocessor = pipeline.named_steps['preprocessor']
    classifier = pipeline.named_steps['classifier']
    
    # Get the exact feature names after One-Hot Encoding
    try:
        # Scikit-Learn 1.0+ method
        feature_names = preprocessor.get_feature_names_out()
    except AttributeError:
        # Fallback for older versions
        cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
        cat_features = cat_encoder.get_feature_names(categorical_cols)
        feature_names = np.concatenate([numerical_cols, cat_features])
        
    # Clean up names for a professional plot (removing 'num__' or 'cat__' prefixes)
    clean_names = [name.split('__')[-1] for name in feature_names]
    
    # Extract importance weights
    importances = classifier.feature_importances_
    
    # Create a DataFrame for easy sorting
    importance_df = pd.DataFrame({
        'Feature': clean_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    # Plotting
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=importance_df.head(15), palette='viridis')
    plt.title('Top 15 Most Important Factors for Irrigation Need', fontsize=14, fontweight='bold')
    plt.xlabel('Relative Importance (XGBoost Weight)')
    plt.ylabel('Environmental Feature')
    plt.tight_layout()
    
    plt.savefig('feature_importance.png')
    print("Feature importance plot saved as 'feature_importance.png'")

def optimize_and_train():
    print("Loading data for optimization...")
    df = pd.read_csv('data/raw/train.csv')
    
    target_col = 'Irrigation_Need'
    X = df.drop(columns=[target_col, 'id'], errors='ignore')
    y = df[target_col].astype('category').cat.codes
    
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # 1. Setup the Base Pipeline for XGBoost
    # Tree models don't need highly correlated drops, so is_tree_model=True
    preprocessor = get_preprocessor(categorical_cols, numerical_cols, is_tree_model=True)
    
    # XGBoost configuration specifically tuned for imbalanced multiclass
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb)
    ])

    # 2. Define the Hyperparameter Grid to push past 90%
    # We use 'classifier__' prefix so RandomizedSearchCV knows these apply to the XGBoost step
    param_grid = {
        'classifier__n_estimators': [100, 300, 500],
        'classifier__max_depth': [3, 5, 7, 9],
        'classifier__learning_rate': [0.01, 0.05, 0.1, 0.2],
        'classifier__subsample': [0.7, 0.8, 1.0],
        'classifier__colsample_bytree': [0.7, 0.8, 1.0],
    }

    print("\nStarting Hyperparameter Tuning (This may take a few minutes)...")
    # RandomizedSearchCV tests random combinations, saving massive amounts of time compared to GridSearch
    search = RandomizedSearchCV(
        pipeline, 
        param_distributions=param_grid, 
        n_iter=15, # Tests 15 different parameter combinations
        scoring='balanced_accuracy', 
        cv=3,      # 3-fold cross-validation
        verbose=2, 
        n_jobs=-1, # Uses all CPU cores
        random_state=42
    )

    search.fit(X_train, y_train)

    # 3. Evaluate the Tuned Model
    best_model = search.best_estimator_
    print(f"\nBest Parameters Found: \n{search.best_params_}")
    
    y_pred = best_model.predict(X_test)
    final_score = balanced_accuracy_score(y_test, y_pred)
    
    print("\n=======================================================")
    print(f"OPTIMIZED XGBOOST BALANCED ACCURACY: {final_score:.4f}")
    print("=======================================================\n")
    print(classification_report(y_test, y_pred))

    # 4. Save the Final Model and Plot Features
    plot_feature_importance(best_model, numerical_cols, categorical_cols)
    
    joblib.dump(best_model, 'optimized_champion_model.pkl')
    print("\nOptimized pipeline successfully saved to 'optimized_champion_model.pkl'")

if __name__ == "__main__":
    optimize_and_train()