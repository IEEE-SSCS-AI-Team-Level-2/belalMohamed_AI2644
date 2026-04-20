import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from preprocessing import get_preprocessor

def plot_feature_importance(pipeline):
    print("\nExtracting Feature Importance...")
    
    # Point exactly to the column transformer, bypassing the custom processor
    col_transformer = pipeline.named_steps['preprocessor'].named_steps['col_transformer']
    classifier = pipeline.named_steps['classifier']
    
    # Extract the names directly
    feature_names = col_transformer.get_feature_names_out()
    clean_names = [name.split('__')[-1] for name in feature_names]
    importances = classifier.feature_importances_
    
    importance_df = pd.DataFrame({
        'Feature': clean_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=importance_df.head(15), palette='viridis')
    plt.title('Top 15 Most Important Factors for Irrigation Need', fontsize=14, fontweight='bold')
    plt.xlabel('Relative Importance (XGBoost Weight)')
    plt.ylabel('Environmental Feature')
    plt.tight_layout()
    
    plt.savefig('feature_importance.png')
    print("Feature importance plot saved as 'feature_importance.png'")

def main():
    print("Loading data for final Champion Model...")
    df = pd.read_csv('data/raw/train.csv')
    
    target_col = 'Irrigation_Need'
    X = df.drop(columns=[target_col, 'id'], errors='ignore')
    y = df[target_col].astype('category').cat.codes
    
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    preprocessor = get_preprocessor(categorical_cols, numerical_cols, is_tree_model=True)
    
    # We plug the winning parameters directly in here
    print("Training Optimized XGBoost Model...")
    xgb = XGBClassifier(
        use_label_encoder=False, 
        eval_metric='mlogloss', 
        random_state=42,
        subsample=0.7,
        n_estimators=100,
        max_depth=7,
        learning_rate=0.2,
        colsample_bytree=1.0
    )
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', xgb)])
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    final_score = balanced_accuracy_score(y_test, y_pred)
    
    print("\n=======================================================")
    print(f"FINAL CHAMPION BALANCED ACCURACY: {final_score:.4f}")
    print("=======================================================\n")
    
    plot_feature_importance(pipeline)
    
    joblib.dump(pipeline, 'optimized_champion_model.pkl')
    print("\nProduction pipeline successfully saved to 'optimized_champion_model.pkl'")

if __name__ == "__main__":
    main()