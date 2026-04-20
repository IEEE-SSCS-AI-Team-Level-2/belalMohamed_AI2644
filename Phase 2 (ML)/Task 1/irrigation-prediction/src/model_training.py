import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import seaborn as sns
import matplotlib.pyplot as plt
from preprocessing import get_preprocessor

class ModelEvaluator:
    @staticmethod
    def evaluate(y_true, y_pred, model_name):
        # Using Balanced Accuracy to account for the 3.33% 'High' class minority
        b_acc = balanced_accuracy_score(y_true, y_pred)
        print(f"\n--- {model_name} ---")
        print(f"Balanced Accuracy: {b_acc:.4f}")
        print(classification_report(y_true, y_pred))
        return b_acc

    @staticmethod
    def plot_confusion_matrix(y_true, y_pred, model_name, class_names):
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=class_names, yticklabels=class_names)
        plt.title(f'{model_name} Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        
        # Save the plot professionally for the portfolio/README
        plt.savefig(f'{model_name.replace(" ", "_")}_confusion_matrix.png')
        print(f"Saved confusion matrix plot for {model_name}.")

def run_pipeline():
    print("Loading data...")
    df = pd.read_csv('data/raw/train.csv')
    
    target_col = 'Irrigation_Need'
    X = df.drop(columns=[target_col, 'id'], errors='ignore')
    y = df[target_col]
    
    # Extract unique class names for the confusion matrix labels before encoding
    class_names = y.unique().tolist()
    
    # Map string target classes to integers for XGBoost compatibility
    y = y.astype('category').cat.codes
    
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # Stratify is crucial here to ensure the 3.33% class is equally represented in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # Define architectures. Notice class_weight='balanced' to fight the severe imbalance
    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, class_weight='balanced', random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    }

    best_score = 0
    best_model_name = ""
    best_y_pred = None

    print("\nBeginning model training and evaluation...")
    for name, model in models.items():
        is_tree = name in ["Random Forest", "XGBoost"]
        preprocessor = get_preprocessor(categorical_cols, numerical_cols, is_tree_model=is_tree)
        
        clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        score = ModelEvaluator.evaluate(y_test, y_pred, name)
        
        if score > best_score:
            best_score = score
            best_model_name = name
            best_y_pred = y_pred

    print(f"\n=======================================================")
    print(f"CHAMPION MODEL: {best_model_name} (Balanced Accuracy: {best_score:.4f})")
    print(f"=======================================================")
    
    ModelEvaluator.plot_confusion_matrix(y_test, best_y_pred, best_model_name, class_names)
    
    # Save the champion model for deployment
    import joblib
    joblib.dump(clf, 'champion_model.pkl')
    print("Champion model saved to champion_model.pkl")

if __name__ == "__main__":
    run_pipeline()