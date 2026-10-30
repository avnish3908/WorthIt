import pandas as pd
import joblib
import os
from .preprocessing import preprocess_and_encode

def load_model_artifacts():
    # Adjust paths based on where the script is called from
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'model', 'model.pkl')
    encoder_path = os.path.join(base_dir, 'model', 'encoder.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        raise FileNotFoundError(f"Model or encoder missing at {model_path}. Train the model first.")
        
    model = joblib.load(model_path)
    encoders = joblib.load(encoder_path)
    return model, encoders

def get_recommendation(predicted, current):
    diff = current - predicted
    percent_diff = (diff / predicted) * 100
    
    if percent_diff < -15:
        return "Excellent Deal"
    elif percent_diff <= 0:
        return "Worth Buying"
    elif percent_diff < 10:
        return "Fair Price"
    elif percent_diff < 25:
        return "Slightly Overpriced"
    else:
        return "Highly Overpriced"

def calculate_confidence(input_data):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'dataset', 'smartphones.csv')
    try:
        from .preprocessing import load_data
        df = load_data(dataset_path)
    except Exception:
        return 80
        
    brand = input_data.get('Brand', '')
    processor = str(input_data.get('Processor', ''))
    try:
        ram = float(input_data.get('RAM', 0))
        storage = float(input_data.get('Storage', 0))
    except ValueError:
        ram = 0
        storage = 0
        
    df['RAM'] = pd.to_numeric(df['RAM'], errors='coerce').fillna(0)
    df['Storage'] = pd.to_numeric(df['Storage'], errors='coerce').fillna(0)
    
    brand_matches = (df['Brand'] == brand).sum()
    spec_matches = ((df['RAM'] == ram) & (df['Storage'] == storage)).sum()
    
    proc_words = processor.split()
    if len(proc_words) >= 2:
        proc_tier = f"{proc_words[0]} {proc_words[1]}"
    elif len(proc_words) == 1:
        proc_tier = proc_words[0]
    else:
        proc_tier = ""
        
    if proc_tier:
        proc_matches = df['Processor'].astype(str).str.contains(proc_tier, case=False, na=False, regex=False).sum()
    else:
        proc_matches = 0
        
    confidence = 65.0
    
    # 1. Brand representation
    confidence += min(10.0, (brand_matches / 40.0) * 10.0)
    
    # 2. Spec commonality
    confidence += min(10.0, (spec_matches / 60.0) * 10.0)
    
    # 3. Processor tier familiarity
    confidence += min(11.0, (proc_matches / 30.0) * 11.0)
    
    return max(65, min(96, int(round(confidence))))

def predict_price(input_data):
    """
    input_data: dict with features including 'Current Market Price'
    """
    model, encoders = load_model_artifacts()
    
    # Extract and remove 'Current Market Price' from features
    current_price = float(input_data.get('Current Market Price', 0))
    features = {k: v for k, v in input_data.items() if k != 'Current Market Price'}
    
    # Create DataFrame for a single row
    df = pd.DataFrame([features])
    
    # Ensure numerical columns are correctly typed
    num_cols = ['RAM', 'Storage', 'Battery Capacity', 'Fast Charging', 'Rear Camera']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    # Need to make sure columns match training exactly in name.
    # We will assume they do for now.
    
    # Preprocess
    df_processed = preprocess_and_encode(df, train=False, encoders=encoders)
    
    # Predict
    predicted_price = model.predict(df_processed)[0]
    predicted_price = round(float(predicted_price))
    
    diff = current_price - predicted_price
    overpriced_percentage = (diff / predicted_price) * 100 if predicted_price > 0 else 0
    
    confidence_score = calculate_confidence(input_data)
    
    return {
        'Predicted Fair Price': predicted_price,
        'Current Price': current_price,
        'Difference': diff,
        'Recommendation': get_recommendation(predicted_price, current_price),
        'Confidence': confidence_score,
        'Overpriced Percentage': round(overpriced_percentage, 1)
    }
