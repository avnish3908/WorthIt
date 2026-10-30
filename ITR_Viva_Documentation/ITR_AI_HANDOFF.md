# ITR AI HANDOFF: ORIENTATION FOR SUCCESSOR AI ASSISTANT
**Project:** WorthIt — AI-Powered Smartphone Price Intelligence and Fair Valuation System  
**Purpose:** Standalone orientation document for the next AI agent preparing the student for the MSBTE ITR Viva  
**Target Student:** Final Year Diploma in Computer Engineering (MSBTE K-Scheme)  
**Host Organization:** InfoStack Software Development, Training and Research Center, Solapur  

---

## 1. PROJECT ESSENTIALS AT A GLANCE
- **Project Name:** `WorthIt`
- **Core Domain:** Supervised Machine Learning, Applied Data Science, Web Application Engineering.
- **Problem Solved:** Resolves price inflation, asymmetric retail markups, and consumer confusion in smartphone purchases by predicting intrinsic fair market value based on hardware specifications.
- **Core Technology Stack:**
  - **Backend:** Python 3.10+, Flask (RESTful routing, Jinja2).
  - **Machine Learning:** Extreme Gradient Boosting (`XGBRegressor`), Scikit-Learn (`LabelEncoder`, `train_test_split`, `metrics`), Joblib serialization.
  - **Data Processing:** Pandas, NumPy.
  - **Database:** SQLite3 (`worthit.db`) with tables `saved_phones` and `settings`.
  - **Frontend:** HTML5, Modern CSS3 (Glassmorphism, custom CSS variables), Vanilla JavaScript (ES6+ Fetch API, DOM manipulation).
  - **Libraries:** Chart.js (bar chart visualizations), GSAP (entrance & scroll animations), FontAwesome (icons).
- **Dataset:** `dataset/smartphones.csv` (2,983 cleaned rows, 11 features, 27 brands).

---

## 2. VERIFIED CODE PATHS & KEY ALGORITHMS

1. **Dynamic Cascading Dropdowns (`utils/preprocessing.py` -> `get_dynamic_maps()`):**
   - Ingests dataset, groups by Brand and Model, extracts valid RAM/Storage variants.
   - Injected into frontend as `window.FULL_MAP`.
   - Client JS dynamically disables and populates child dropdowns to prevent invalid combinations.
2. **ML Valuation Model (`model/train_model.py` & `utils/predictor.py`):**
   - Model: `XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)`.
   - Artifacts: `model/model.pkl` (233 KB) and `model/encoder.pkl` (37 KB).
   - Top Features: Storage (39.57%), Brand (18.80%), Display Type (13.36%), RAM (9.62%), Processor (5.20%).
3. **5-Tier Deal Quality Evaluator (`utils/predictor.py` -> `get_recommendation()`):**
   - Calculates percentage difference: $\Delta_{\%} = ((P_{\text{curr}} - P_{\text{pred}}) / P_{\text{pred}}) \times 100$.
   - Categories: Excellent Deal ($<-15\%$), Worth Buying ($\le 0\%$), Fair Price ($<10\%$), Slightly Overpriced ($<25\%$), Highly Overpriced ($\ge 25\%$).
4. **Heuristic Confidence Scorer (`utils/predictor.py` -> `calculate_confidence()`):**
   - Formula: $\text{Confidence} = 65.0 + \text{BrandPts} + \text{SpecPts} + \text{ProcPts}$.
   - Strictly bounded between **65% and 96%**; based on dataset row density.
5. **Smarter Alternatives Recommender (`utils/recommender.py` -> `get_alternatives()`):**
   - Filters candidate phones in range: $[\min(P_{\text{pred}}, P_{\text{curr}}) \times 0.9, \max(P_{\text{pred}}, P_{\text{curr}}) \times 1.05]$.
   - Requires $RAM \ge \max(2, RAM - 2)$ and $Storage \ge \max(16, Storage / 2)$.
   - Ranks by asymmetric penalty function combining price distance and spec bonuses.
   - Top 1–3 results receive distinct terracotta/gold borders and "Top Pick" star badges.
6. **SQLite Relational Persistence (`app.py` & `worthit.db`):**
   - Tables: `saved_phones` (id, brand, model, processor, ram, storage, predicted_price, current_price, savings, timestamp) and `settings` (key, value).
   - All queries strictly parameterized using `?` placeholders.

---

## 3. WHAT THE NEXT AI MUST NOT ASSUME (CRITICAL GUARDRAILS)

- **DO NOT assume live web-scraping exists:** The app does NOT scrape Amazon or Flipkart. The user enters the `Current Market Price` manually in the UI.
- **DO NOT assume live online learning exists:** The model is trained offline via `train_model.py`. Saving a phone does not retrain `model.pkl`.
- **DO NOT assume currency conversion is operational:** The UI shows an INR option only; no real-time currency conversion logic exists.
- **DO NOT assume a pytest/unittest test suite exists:** Testing was performed through standalone verification scripts (`test_conf.py`) and manual functional test matrices.
- **DO NOT claim synthetic datasets are in use:** The codebase was verified to use only the cleaned 2,983-row production dataset `smartphones.csv`. All synthetic scripts have been deleted.

---

## 4. RECOMMENDED STRUCTURE FOR MOCK VIVA SESSIONS

When preparing the student, the successor AI should conduct the mock viva in the following sequence:
1. **Round 1 — Project Overview & Pitch (5 mins):** Practice the 30-second and 60-second elevator pitches. Check clarity and confidence.
2. **Round 2 — Machine Learning Deep Dive (10 mins):** Drill on why XGBoost was chosen, feature importance percentages, LabelEncoder mechanics, and evaluation metrics ($R^2$ and MAE).
3. **Round 3 — Architecture & Web Implementation (10 mins):** Drill on the 4-tier architecture, `/predict` REST route, cascading dropdown logic (`get_dynamic_maps`), and SQLite parameterized queries.
4. **Round 4 — Recommender Engine & Formulas (10 mins):** Quiz on the deal rating thresholds, the bounded confidence formula (65%–96%), and the Smarter Alternatives price window and penalty function.
5. **Round 5 — Difficult Examiner Cross-Questions & Trap Defense (10 mins):** Use the 15 examiner traps in `ITR_Viva_Quick_Revision.md` to train the student in avoiding unverified claims and giving honest, technically rigorous responses.
6. **Round 6 — Live Demonstration Walkthrough (5 mins):** Rehearse the 5-step UI demo flow from index page to smart form, pixel scanner, results card, saved phones, and dark mode toggling.
