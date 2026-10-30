import sys
import os
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import pandas as pd

# Add parent directory to path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import load_data, preprocess_and_encode

def train():
    print("Loading dataset...")
    try:
        df = load_data('../dataset/smartphones.csv')
    except FileNotFoundError:
        df = load_data('dataset/smartphones.csv') # Fallback if run from root
        
    print(f"Dataset loaded with {len(df)} rows.")
    
    # Separate features and target
    X = df.drop('Price', axis=1)
    y = df['Price']
    
    # Preprocess
    print("Encoding categorical features...")
    X_processed, encoders = preprocess_and_encode(X, train=True)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    
    # Train
    print("Training XGBoost Regressor...")
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Model trained! MAE: ${mae:.2f} | R2 Score: {r2:.4f}")
    
    # Save Model and Encoders
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/model.pkl')
    joblib.dump(encoders, 'model/encoder.pkl')
    print("Saved model.pkl and encoder.pkl to model/ directory.")
    
    # Feature Importance Plot (optional visualization)
    importance = model.feature_importances_
    features = X.columns
    feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    feature_importance_df.to_csv('model/feature_importance.csv', index=False)
    print("Saved feature_importance.csv")

if __name__ == "__main__":
    # Fix working directory if run from model folder
    if os.path.basename(os.getcwd()) == 'model':
        os.chdir('..')
    train()
