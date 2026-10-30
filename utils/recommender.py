import pandas as pd
import os
from .preprocessing import load_data

def get_alternatives(input_specs, current_price, predicted_price, num_alternatives=10):
    """
    Finds cheaper phones with near-identical core specs.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'dataset', 'smartphones.csv')
    
    try:
        df = load_data(dataset_path)
    except Exception as e:
        print(f"Error loading dataset for alternatives: {e}")
        return []
        
    try:
        ram = float(input_specs.get('RAM', 0))
        storage = float(input_specs.get('Storage', 0))
    except ValueError:
        return []
    
    # Clean numeric columns to be safe
    df['RAM'] = pd.to_numeric(df['RAM'], errors='coerce').fillna(0)
    df['Storage'] = pd.to_numeric(df['Storage'], errors='coerce').fillna(0)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
    
    # Exclude the exact same phone they entered
    input_brand = input_specs.get('Brand', '')
    input_model = input_specs.get('Model', '')
    df = df[~((df['Brand'] == input_brand) & (df['Model'] == input_model))]
    
    lower_bound = min(predicted_price, current_price) * 0.9
    upper_bound = max(predicted_price, current_price) * 1.05
    
    # Filter 1: Price range and similar/better specs
    mask = (
        (df['Price'] >= lower_bound) & 
        (df['Price'] <= upper_bound) & 
        (df['RAM'] >= max(2, ram - 2)) & 
        (df['Storage'] >= max(16, storage / 2))
    )
    alternatives = df[mask].copy()
    
    if len(alternatives) == 0:
        return []
        
    # Scoring for best match:
    # We want price closest to predicted_price.
    # We want RAM and Storage to be closest to the requested ones (or slightly better).
    def calculate_penalty(row):
        price_penalty = abs(row['Price'] - predicted_price) / predicted_price
        
        # RAM penalty
        ram_diff = row['RAM'] - ram
        if ram_diff < 0:
            ram_penalty = abs(ram_diff) * 0.2
        else:
            ram_penalty = ram_diff * 0.05
            
        # Storage penalty
        storage_diff = row['Storage'] - storage
        if storage_diff < 0:
            storage_penalty = abs(storage_diff) / storage * 0.2
        else:
            storage_penalty = storage_diff / storage * 0.05
            
        return price_penalty + ram_penalty + storage_penalty

    alternatives['Penalty'] = alternatives.apply(calculate_penalty, axis=1)
    
    # Sort by Penalty
    alternatives = alternatives.sort_values(by='Penalty', ascending=True)
    
    # Deduplicate models
    alternatives = alternatives.drop_duplicates(subset=['Brand', 'Model'])
    
    top_alts = alternatives.head(num_alternatives)
    
    result = []
    for _, row in top_alts.iterrows():
        savings = current_price - row['Price']
        result.append({
            'Brand': row['Brand'],
            'Model': row['Model'],
            'Price': int(row['Price']),
            'Savings': int(savings) if savings > 0 else 0,
            'Pros': [
                f"{int(row['RAM'])}GB RAM, {int(row['Storage'])}GB Storage",
                f"{row['Processor']} Chipset",
                f"{int(row['Battery Capacity'])}mAh Battery"
            ],
            'ImagePlaceholder': f"{str(row['Brand']).lower()}-placeholder.png"
        })
        
    return result
