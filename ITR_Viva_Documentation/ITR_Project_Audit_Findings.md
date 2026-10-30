# ITR PROJECT AUDIT FINDINGS: FORENSIC CODEBASE VERIFICATION
**Project:** WorthIt — AI-Powered Smartphone Price Intelligence and Fair Valuation System  
**Audit Conducted:** 2026-10-29  
**Auditor Role:** Senior Software Engineer, Code Auditor, and MSBTE Viva Preparation Specialist  

---

## 1. VERIFIED FACTS (EVIDENCE-BACKED)

1. **Dataset Integrity:** Verified file `dataset/smartphones.csv` exists, contains **2,983 records** (2,984 lines including header), 11 columns, and 27 unique brands. Column names match code expectations: `Brand, Model, Processor, RAM, Storage, Display Type, Battery Capacity, Fast Charging, Rear Camera, Network, Price`.
2. **Model Serialization:** Verified files `model/model.pkl` (233 KB) and `model/encoder.pkl` (37 KB) exist and are loaded successfully via Joblib during inference.
3. **Database Existence & Integrity:** Verified file `worthit.db` exists. Inspected tables:
   - `saved_phones`: Verified schema with 10 fields and 3 actual saved records (Nothing Phone 1, Samsung Galaxy Z Fold6, Apple iPhone 17 Pro Max).
   - `settings`: Verified schema with 2 fields and 2 records (`currency=INR`, `theme=light`).
4. **Dynamic Mapping Engine:** `get_dynamic_maps()` in `utils/preprocessing.py` successfully reads `dataset/smartphones.csv`, groups by `['Brand', 'Model']`, deduplicates identical variants, and constructs a nested hierarchy.
5. **Inference Pipeline:** `predict_price()` in `utils/predictor.py` processes specification dictionaries, encodes categorical labels with `encoder.pkl`, and invokes `model.predict()`.
6. **Deal Classification Logic:** Implemented in `utils/predictor.py` across 5 defined tiers using percentage difference.
7. **Heuristic Confidence Formula:** Verified in `utils/predictor.py` and independently validated in `test_conf.py`. Bounded strictly between 65% and 96%.
8. **Smarter Alternatives Engine:** Implemented in `utils/recommender.py`. Enforces the empirical price-band filter and asymmetric 3-factor penalty scoring function.
9. **UI & Card Hierarchy:** `static/js/prediction.js` contains the rank-based check (`index < 3`) rendering a distinct terracotta/gold accent border and "Top Pick" star badge on the top 3 cards.
10. **Theming & Persistence:** Dark mode is implemented via CSS variables (`data-theme="dark"`), synchronized in browser `localStorage`, and persisted via SQLite `/settings`.

---

## 2. DISCREPANCIES BETWEEN DOCUMENTATION & CODE

1. **Feature Importance Ranking in Reference Report vs. Reality:**
   - In earlier report drafts, generic regression weights were mentioned.
   - *Actual Code Finding:* `model/feature_importance.csv` contains the true empirical tree-split importance from the trained XGBoost model: **Storage (39.57%)**, **Brand (18.80%)**, **Display Type (13.36%)**, **RAM (9.62%)**, **Processor (5.20%)**. The viva defense must cite these exact verified percentages.
2. **Synthetic Dataset Claims in Older Readmes:**
   - Earlier commit notes mentioned synthetic smartphone datasets.
   - *Actual Code Finding:* Confirmed all synthetic dataset generation scripts have been purged. The system operates entirely on the cleaned 2,983-row production dataset `smartphones.csv`.
3. **Currency Conversion Claim:**
   - The settings UI presents a Currency dropdown, but only `INR (₹)` is populated, and no conversion math exists in the backend.
   - *Action for Viva:* Acknowledge honestly that multi-currency support is scoped as a future enhancement and current processing is strictly in INR.

---

## 3. SECURITY & RELIABILITY AUDIT

| Component | Security / Reliability Finding | Risk Level | Evidence in Code | Mitigation / Viva Answer |
| :--- | :--- | :--- | :--- | :--- |
| **SQL Injection** | Parameterized queries (`?`) used throughout `app.py`. | **PASS / Secure** | `app.py` lines 101–108, 115, 134. | Complies with database security standards. |
| **Secret Key Management** | Hardcoded secret key string in `app.py`. | **LOW (Dev Risk)** | `app.py` line 11: `'worthit-secret-key-123'`. | In production, this should be an environment variable (`os.environ`). |
| **Unseen Label Handling** | Fallback to `classes_[0]` in LabelEncoder. | **PASS / Safe** | `utils/preprocessing.py` line 87. | Prevents unhandled exceptions when unseen strings are processed. |
| **Numeric Coercion** | Numeric fields coerced via `pd.to_numeric(..., errors='coerce').fillna(0)`. | **PASS / Safe** | `utils/predictor.py` line 101, `utils/recommender.py` lines 25–27. | Robust defense against malformed or non-numeric form inputs. |
| **Automated Test Coverage** | No automated `pytest` or `unittest` suite found in workspace. | **MODERATE (QA Gap)** | Only `test_conf.py` exists. | Frame validation around functional test case matrices and standalone testing scripts. |

---

## 4. INCOMPLETE OR UNVERIFIED CLAIMS

1. **Live E-Commerce Scraping:** No web-scraping logic (BeautifulSoup, Selenium, Scrapy) exists in the repository. The listing price must be provided by the user. Do not claim automated live scraping in the viva.
2. **Real-time Model Retraining:** The application does not retrain `model.pkl` when users save phones. Training is strictly an offline batch process via `train_model.py`.
3. **Refurbished Phone Wear Factor:** No computer vision or cosmetic grading logic exists. Valuations assume a functioning device matching the stated hardware specs.

---

## 5. RANKED VIVA PREPARATION PRIORITIES

1. **Priority 1 (Must Master):** The 4-tier system architecture and the complete request-response flow from `/prediction` form submission to JSON response and Chart.js rendering.
2. **Priority 2 (Must Master):** Why XGBoost was selected over Linear Regression, its key hyperparameters (`n_estimators=100`, `max_depth=5`), and the top feature importances (Storage 39.6%, Brand 18.8%).
3. **Priority 3 (Must Master):** The exact formulas for the 5 deal tiers, the bounded confidence score (65%–96%), and the Smarter Alternatives price window and penalty function.
4. **Priority 4 (Must Master):** The SQLite schema (`saved_phones`, `settings`) and how parameterized queries prevent SQL injection.
5. **Priority 5 (Must Master):** Live demonstration flow: smart cascading dropdowns, pixel scanner animation, results card, bookmarking, and theme toggling.
