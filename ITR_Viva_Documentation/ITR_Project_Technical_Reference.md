# ITR PROJECT TECHNICAL REFERENCE
**Project:** WorthIt — AI-Powered Smartphone Price Intelligence and Fair Valuation System  
**Scope:** File Responsibilities, Function Signatures, Schemas, Dependencies & API Reference  

---

## 1. FILE & COMPONENT MAP

| File Path | Component Type | Primary Responsibility | Key External Dependencies |
| :--- | :--- | :--- | :--- |
| `app.py` | Web Controller | Flask HTTP route handlers, request dispatching, SQLite DB lifecycle (`get_db`, `init_db`). | `flask`, `sqlite3`, `utils.predictor`, `utils.recommender`, `utils.preprocessing` |
| `utils/preprocessing.py` | ETL / Preprocessor | Ingests `smartphones.csv`, extracts nested variant maps (`get_dynamic_maps`), fits/transforms `LabelEncoder`. | `pandas`, `sklearn.preprocessing.LabelEncoder`, `os` |
| `utils/predictor.py` | ML Inference | Loads `.pkl` artifacts, coordinates `XGBRegressor.predict()`, evaluates deal quality, computes confidence score. | `joblib`, `pandas`, `sklearn`, `utils.preprocessing` |
| `utils/recommender.py` | Recommendation | Filters alternative smartphones within price band, computes penalty scores, deduplicates models. | `pandas`, `os`, `utils.preprocessing` |
| `model/train_model.py` | Training Pipeline | Standalone script: splits data (80/20), trains `XGBRegressor`, serializes `model.pkl` and `encoder.pkl`, exports `feature_importance.csv`. | `xgboost.XGBRegressor`, `sklearn.model_selection`, `joblib` |
| `test_conf.py` | Standalone Test | Standalone script validating the dynamic confidence formula against edge-case inputs. | `pandas` |
| `static/js/prediction.js` | Frontend Controller | Manages cascading dropdowns, live preview silhouette, full-screen scanner, Chart.js bar chart, and AJAX POST `/predict`. | `Chart.js`, Native DOM API |
| `static/js/animations.js` | Motion Controller | Configures GSAP timelines, navbar entry, scroll triggers for `.card` elements, and result entrance. | `gsap`, `ScrollTrigger` |
| `static/js/main.js` | UI Enhancements | Controls navbar shrink-on-scroll and toggles the advanced specs section. | Native DOM API |
| `templates/base.html` | Master Template | HTML skeleton, navigation bar, flash messages, theme initializer script, FontAwesome, Chart.js. | Jinja2 |
| `templates/prediction.html` | Prediction View | Form fields, live preview card, scanner overlay, result dashboard, canvas for Chart.js. | Jinja2 |
| `templates/saved.html` | Saved View | Card grid displaying bookmarked valuations from SQLite with delete handlers. | Jinja2 |
| `templates/settings.html` | Settings View | Preference controls for currency (INR) and theme toggle (light/dark mode). | Jinja2 |

---

## 2. FUNCTION & CLASS SIGNATURE SPECIFICATION

### `utils/preprocessing.py`
```python
def get_dynamic_maps() -> tuple[list[str], dict]:
    """
    Reads dataset/smartphones.csv and constructs:
    - brands: list of unique sorted brand names.
    - full_map: nested dict of structure:
        {
            brand_name: {
                model_name: [
                    {
                        'RAM': float, 'Storage': float, 'Processor': str,
                        'Display Type': str, 'Network': str,
                        'Battery Capacity': float, 'Fast Charging': float,
                        'Rear Camera': float
                    }, ...
                ]
            }
        }
    """

def load_data(filepath: str = 'dataset/smartphones.csv') -> pd.DataFrame:
    """Loads CSV dataset and drops rows with missing values."""

def preprocess_and_encode(
    df: pd.DataFrame, 
    train: bool = True, 
    encoders: dict[str, LabelEncoder] = None
) -> tuple[pd.DataFrame, dict[str, LabelEncoder]] | pd.DataFrame:
    """
    Applies Scikit-Learn LabelEncoder to categorical columns:
    ['Brand', 'Model', 'Processor', 'Display Type', 'Network'].
    If train=True, fits new encoders.
    If train=False, transforms using existing encoders, falling back to class 0 for unseen labels.
    """
```

### `utils/predictor.py`
```python
def load_model_artifacts() -> tuple[XGBRegressor, dict[str, LabelEncoder]]:
    """Loads model.pkl and encoder.pkl via joblib. Raises FileNotFoundError if missing."""

def get_recommendation(predicted: float, current: float) -> str:
    """
    Calculates percentage diff: ((current - predicted) / predicted) * 100
    Returns:
        < -15%: 'Excellent Deal'
        <= 0%: 'Worth Buying'
        < 10%: 'Fair Price'
        < 25%: 'Slightly Overpriced'
        >= 25%: 'Highly Overpriced'
    """

def calculate_confidence(input_data: dict) -> int:
    """
    Calculates dynamic confidence based on dataset row density:
    Confidence = 65.0 + min(10.0, brand_matches/40 * 10)
                       + min(10.0, spec_matches/60 * 10)
                       + min(11.0, proc_matches/30 * 11)
    Bounded strictly between [65, 96].
    """

def predict_price(input_data: dict) -> dict:
    """
    Orchestrates full inference pipeline:
    - Separates 'Current Market Price' from features
    - Encodes categorical features via encoder.pkl
    - Invokes model.predict()
    - Returns dictionary with Predicted Fair Price, Current Price, Difference,
      Recommendation, Confidence, and Overpriced Percentage.
    """
```

### `utils/recommender.py`
```python
def get_alternatives(
    input_specs: dict, 
    current_price: float, 
    predicted_price: float, 
    num_alternatives: int = 10
) -> list[dict]:
    """
    Finds cheaper smartphones with near-identical or better specifications:
    1. Excludes current Brand + Model.
    2. Filters within price window: [min(pred, curr)*0.9, max(pred, curr)*1.05].
    3. Requires RAM >= max(2, ram - 2) and Storage >= max(16, storage / 2).
    4. Computes composite penalty:
       Penalty = |Price - pred|/pred + RAM_penalty + Storage_penalty.
    5. Deduplicates by model and returns top N alternatives.
    """
```

---

## 3. DATABASE SCHEMA & TABLE DEFINITIONS

### Database File: `worthit.db` (SQLite 3)

```sql
-- 1. Saved Phone Bookmarks Table
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
);

-- 2. System Settings Table
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

---

## 4. RESTful API REFERENCE

### 1. `POST /predict`
- **Purpose:** Executes fair price estimation and surfaces smarter alternatives.
- **Payload:**
  ```json
  {
    "Brand": "string",
    "Model": "string",
    "Processor": "string",
    "RAM": "number",
    "Storage": "number",
    "Display Type": "string",
    "Battery Capacity": "number",
    "Fast Charging": "number",
    "Rear Camera": "number",
    "Network": "string",
    "Current Market Price": "number"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "prediction": {
      "Predicted Fair Price": 42150,
      "Current Price": 48900,
      "Difference": 6750,
      "Recommendation": "Slightly Overpriced",
      "Confidence": 93,
      "Overpriced Percentage": 16.0
    },
    "alternatives": [
      {
        "Brand": "OnePlus",
        "Model": "Nord 3 5G",
        "Price": 33999,
        "Savings": 14901,
        "Pros": ["16GB RAM, 256GB Storage", "Dimensity 9000 Chipset", "5000mAh Battery"],
        "ImagePlaceholder": "oneplus-placeholder.png"
      }
    ]
  }
  ```

### 2. `POST /saved`
- **Purpose:** Persists a valuation bookmark into SQLite.
- **Payload:**
  ```json
  {
    "Brand": "Apple",
    "Model": "iPhone 11",
    "Processor": "Apple A13 Bionic Hexa Core",
    "RAM": 4,
    "Storage": 128,
    "Predicted_Price": 42150.0,
    "Current_Price": 48900.0,
    "Savings": 6750.0
  }
  ```
- **Success Response (200 OK):** `{"status": "success"}`

### 3. `DELETE /saved/<int:item_id>`
- **Purpose:** Removes a bookmarked valuation from SQLite.
- **Success Response (200 OK):** `{"status": "success"}`

### 4. `POST /settings`
- **Purpose:** Saves user preferences (e.g. `{"theme": "dark", "currency": "INR"}`).
- **Success Response (200 OK):** `{"status": "success"}`

---

## 5. COMPLETE DEPENDENCY SPECIFICATION

From `requirements.txt`:
```
Flask
pandas
numpy
scikit-learn
xgboost
matplotlib
joblib
```
*(All components verified compatible with standard Python 3.10+ environments).*
