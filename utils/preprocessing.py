import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def get_dynamic_maps():
    csv_path = os.path.join(os.path.dirname(__file__), '../dataset/smartphones.csv')
    if not os.path.exists(csv_path):
        return [], {}
        
    df = pd.read_csv(csv_path)
    df = df.fillna({'RAM': 0, 'Storage': 0, 'Fast Charging': 0})
    df = df.fillna('Unknown')
    
    brands = sorted([str(b) for b in df['Brand'].unique()])
    full_map = {}
    
    grouped = df.groupby(['Brand', 'Model'])
    for (brand, model), group in grouped:
        brand = str(brand)
        model = str(model)
        if brand not in full_map:
            full_map[brand] = {}
            
        variants = []
        for _, row in group.iterrows():
            variants.append({
                'RAM': float(row['RAM']),
                'Storage': float(row['Storage']),
                'Processor': str(row['Processor']),
                'Display Type': str(row['Display Type']),
                'Network': str(row['Network']),
                'Battery Capacity': float(row['Battery Capacity']),
                'Fast Charging': float(row['Fast Charging']),
                'Rear Camera': float(row['Rear Camera'])
            })
            
        # Deduplicate variants if there are multiple rows with exact same specs
        # We can just keep the unique combinations
        unique_variants = []
        seen = set()
        for v in variants:
            key = (v['RAM'], v['Storage'], v['Processor'])
            if key not in seen:
                seen.add(key)
                unique_variants.append(v)
                
        # Sort variants primarily by RAM then Storage
        unique_variants.sort(key=lambda x: (x['RAM'], x['Storage']))
        
        full_map[brand][model] = unique_variants
        
    return brands, full_map

def load_data(filepath='dataset/smartphones.csv'):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    df = pd.read_csv(filepath)
    # Handle missing values by dropping rows (simple approach for this project)
    df = df.dropna()
    return df

def preprocess_and_encode(df, train=True, encoders=None):
    """
    Preprocess data. 
    If train=True, fits new LabelEncoders and returns the processed df + the encoders.
    If train=False, transforms data using the provided encoders.
    """
    df_processed = df.copy()
    categorical_cols = ['Brand', 'Model', 'Processor', 'Display Type', 'Network']
    
    if train:
        encoders = {}
        for col in categorical_cols:
            if col in df_processed.columns:
                le = LabelEncoder()
                df_processed[col] = le.fit_transform(df_processed[col].astype(str))
                encoders[col] = le
        return df_processed, encoders
    else:
        if not encoders:
            raise ValueError("Encoders must be provided for inference")
        for col in categorical_cols:
            if col in df_processed.columns:
                le = encoders[col]
                # Handle unseen labels by defaulting to the first seen label
                df_processed[col] = df_processed[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                df_processed[col] = le.transform(df_processed[col].astype(str))
        return df_processed
