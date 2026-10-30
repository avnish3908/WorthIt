from flask import Flask, render_template, request, jsonify, g
import sqlite3
import os
import json
from utils.predictor import predict_price
from utils.recommender import get_alternatives
from utils.preprocessing import get_dynamic_maps

app = Flask(__name__)
app.config['DATABASE'] = 'worthit.db'
app.secret_key = 'worthit-secret-key-123'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        # Saved Phones table
        db.execute('''
            CREATE TABLE IF NOT EXISTS saved_phones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT,
                model TEXT,
                processor TEXT,
                ram INTEGER,
                storage INTEGER,
                predicted_price REAL,
                current_price REAL,
                savings REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Settings table (simple key-value for a single user context)
        db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        db.commit()

# Ensure DB is initialized
if not os.path.exists('worthit.db'):
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction')
def prediction():
    # Pass the full dynamic map to the frontend to handle smart autofill
    brands, full_map = get_dynamic_maps()
    return render_template('prediction.html', brands=brands, full_map=json.dumps(full_map))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # 1. Get prediction result
    try:
        prediction_result = predict_price(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
        
    # 2. Get alternatives based on predicted fair price or current price
    alternatives = get_alternatives(data, prediction_result['Current Price'], prediction_result['Predicted Fair Price'])
    
    # 3. Combine and return
    response_data = {
        'prediction': prediction_result,
        'alternatives': alternatives
    }
    return jsonify(response_data)

@app.route('/saved', methods=['GET', 'POST'])
def saved():
    if request.method == 'GET':
        db = get_db()
        cur = db.execute('SELECT * FROM saved_phones ORDER BY timestamp DESC')
        saved_items = [dict(row) for row in cur.fetchall()]
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(saved_items)
        return render_template('saved.html', saved_items=saved_items)
        
    elif request.method == 'POST':
        data = request.json
        db = get_db()
        db.execute('''
            INSERT INTO saved_phones (brand, model, processor, ram, storage, predicted_price, current_price, savings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('Brand', ''), data.get('Model', ''), data.get('Processor', ''), 
            data.get('RAM', 0), data.get('Storage', 0), data.get('Predicted_Price', 0), 
            data.get('Current_Price', 0), data.get('Savings', 0)
        ))
        db.commit()
        return jsonify({'status': 'success'})

@app.route('/saved/<int:item_id>', methods=['DELETE'])
def delete_saved(item_id):
    db = get_db()
    db.execute('DELETE FROM saved_phones WHERE id = ?', (item_id,))
    db.commit()
    return jsonify({'status': 'success'})

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        db = get_db()
        cur = db.execute('SELECT * FROM settings')
        settings_dict = {row['key']: row['value'] for row in cur.fetchall()}
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify(settings_dict)
        return render_template('settings.html', settings=settings_dict)
        
    elif request.method == 'POST':
        data = request.json
        db = get_db()
        for k, v in data.items():
            db.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (k, str(v)))
        db.commit()
        return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Initialize DB specifically on start if needed
    init_db()
    app.run(debug=True, port=5000)
