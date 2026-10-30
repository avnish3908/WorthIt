# ITR VIVA QUESTION BANK: 50+ EVIDENCE-ANCHORED QUESTIONS
**Project:** WorthIt — AI-Powered Smartphone Price Intelligence and Fair Valuation System  
**Alignment:** MSBTE Diploma in Computer Engineering (K-Scheme) Industrial Training Report  

---

## CATEGORY A: PROJECT INTRODUCTION & MOTIVATION

#### Q1: What is the title and core objective of your industrial training project?
- **Short Spoken Answer:** My project is titled **WorthIt: AI-Powered Smartphone Price Intelligence and Fair Valuation System**. Its objective is to determine the mathematically fair market price of any smartphone based on hardware specifications, evaluate deal quality, and suggest better-value alternatives.
- **Deeper Answer:** Consumers frequently encounter erratic pricing on retail sites where markups do not reflect actual silicon and component value. WorthIt removes this information asymmetry by using a trained regression model to evaluate fair pricing and surface superior specs within the same budget.
- **Code Evidence:** `templates/index.html` (Lines 8–13), `README.txt` (Lines 5–11).

#### Q2: Who is the intended end user of this system?
- **Short Spoken Answer:** Retail smartphone buyers, e-commerce shoppers, and second-hand/refurbished electronics buyers who need an objective evaluation before purchasing a phone.
- **Deeper Answer:** It serves both non-technical consumers who simply want to know if a deal is good, and power users who want to compare hardware specifications and discover superior silicon alternatives.
- **Code Evidence:** `templates/prediction.html`, `templates/saved.html`.

---

## CATEGORY B: MACHINE LEARNING & ALGORITHMIC FOUNDATIONS

#### Q3: Which machine learning algorithm did you use and why?
- **Short Spoken Answer:** We used **XGBoost Regressor (`XGBRegressor`)**, an ensemble method of Gradient Boosted Decision Trees. It was chosen because it delivers state-of-the-art accuracy on structured tabular datasets, captures non-linear price jumps, and includes built-in regularization.
- **Deeper Answer:** Simple Linear Regression assumes independent, linear contributions which fails when modeling hardware combinations—for example, doubling storage from 64GB to 128GB has a different price slope than moving from 512GB to 1TB. Deep neural networks, on the other hand, are prone to overfitting on small tabular datasets. XGBoost builds trees sequentially to correct prior residual errors with low inference latency.
- **Code Evidence:** `model/train_model.py` (Line 36: `XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)`).

#### Q4: How is categorical data encoded before feeding it to XGBoost?
- **Short Spoken Answer:** We use Scikit-Learn's **`LabelEncoder`** across the categorical features: `Brand`, `Model`, `Processor`, `Display Type`, and `Network`.
- **Deeper Answer:** Tree-based algorithms can handle label-encoded integer features effectively because decision trees split on threshold values along feature dimensions without imposing a continuous linear weight. The fitted encoders are serialized into `model/encoder.pkl` to transform user inputs during inference.
- **Code Evidence:** `utils/preprocessing.py` (Lines 63–89: `preprocess_and_encode()`).

#### Q5: What evaluation metrics did you use to evaluate model performance?
- **Short Spoken Answer:** We evaluated our model using **Mean Absolute Error (MAE)** and the **Coefficient of Determination ($R^2$ Score)**.
- **Deeper Answer:** MAE measures the average absolute difference between predicted and actual prices in Indian Rupees, providing an intuitive measure of accuracy. $R^2$ measures the proportion of variance in price explained by the hardware features, achieving over 0.93 on the test set.
- **Code Evidence:** `model/train_model.py` (Lines 41–43: `mean_absolute_error(y_test, predictions)`, `r2_score(y_test, predictions)`).

#### Q6: What were the most important features determining smartphone price?
- **Short Spoken Answer:** According to our exported feature importance rankings, **Internal Storage** is the single most important factor at **39.6%**, followed by **Brand** at **18.8%**, and **Display Type** at **13.4%**.
- **Deeper Answer:** Silicon and storage markups drive retail mobile margins. Interestingly, raw battery capacity and camera megapixels contributed less than 3% each, reflecting that high-megapixel sensors and large batteries are now common across budget devices, whereas storage capacity and brand positioning remain premium differentiators.
- **Code Evidence:** `model/feature_importance.csv` (Lines 1–11).

---

## CATEGORY C: RECOMMENDER ENGINE & HEURISTIC LOGIC

#### Q7: How does your Smarter Alternatives recommender select phones?
- **Short Spoken Answer:** It filters phones within a strict price window between the predicted fair price and listing price with comparable or superior RAM and storage, then ranks them using a multi-criteria penalty function.
- **Deeper Answer:** In `utils/recommender.py`, we define an empirical window: `[min(pred, curr) * 0.9, max(pred, curr) * 1.05]`. We enforce $RAM \ge \max(2, RAM_{\text{req}} - 2)$ and $Storage \ge \max(16, Storage_{\text{req}} / 2)$. The penalty score combines the relative price distance from fair value with spec differences, prioritizing phones closest to fair value with superior specs.
- **Code Evidence:** `utils/recommender.py` (Lines 34–71: `calculate_penalty()`).

#### Q8: Why are the top 3 alternative cards styled differently in the UI?
- **Short Spoken Answer:** To provide visual hierarchy and draw the user's attention to the best-value options, the top 1–3 alternatives receive a distinct terracotta/gold accent border and a 'Top Pick' star badge.
- **Deeper Answer:** In `static/js/prediction.js`, we check `index < 3`. If true, the card receives a 2px solid terracotta border, subtle box shadow glow, and a styled pill badge indicating it is a top recommendation. Rank 4 and above remain in standard card styling.
- **Code Evidence:** `static/js/prediction.js` (Lines 265–276).

#### Q9: How is the Model Confidence score calculated?
- **Short Spoken Answer:** It is calculated dynamically based on dataset density—evaluating how many rows in the training data match the user's brand, RAM/storage combination, and processor tier—bounded strictly between 65% and 96%.
- **Deeper Answer:** Rather than displaying an arbitrary static percentage (such as 80%), `calculate_confidence()` starts at a baseline of 65.0%, adds up to 10 points for brand frequency, 10 points for exact RAM/Storage commonality, and 11 points for processor family representation. This provides an empirical indicator of statistical support.
- **Code Evidence:** `utils/predictor.py` (Lines 34–83: `calculate_confidence()`), verified in `test_conf.py`.

#### Q10: How are deal recommendations categorized?
- **Short Spoken Answer:** By calculating the percentage difference between the current listing price and predicted fair price into 5 discrete tiers: Excellent Deal, Worth Buying, Fair Price, Slightly Overpriced, or Highly Overpriced.
- **Deeper Answer:** In `utils/predictor.py`, `(current - predicted) / predicted * 100` determines the category. If under -15%, it's an "Excellent Deal"; if under 0%, "Worth Buying"; under 10%, "Fair Price"; under 25%, "Slightly Overpriced"; and 25% or higher, "Highly Overpriced".
- **Code Evidence:** `utils/predictor.py` (Lines 19–32: `get_recommendation()`).

---

## CATEGORY D: DATASET & PREPROCESSING

#### Q11: Describe your dataset. Where did it come from and what is its shape?
- **Short Spoken Answer:** The dataset is `smartphones.csv` located in `dataset/`. It contains **2,983 rows** and **11 columns**, covering 27 smartphone manufacturers with cleaned specification values.
- **Deeper Answer:** The 11 feature columns are: `Brand`, `Model`, `Processor`, `RAM`, `Storage`, `Display Type`, `Battery Capacity`, `Fast Charging`, `Rear Camera`, `Network`, and `Price`. All storage suffixes have been decoupled from model names to allow clean variant mapping.
- **Code Evidence:** `dataset/smartphones.csv` (Header line 1, total lines 2,984).

#### Q12: How do your dynamic dropdowns prevent users from selecting invalid phone configurations?
- **Short Spoken Answer:** On application load, `get_dynamic_maps()` parses the dataset and creates a nested hierarchy of Brand $\rightarrow$ Model $\rightarrow$ valid Variants. This map is passed to the browser as `window.FULL_MAP` to dynamically filter child dropdowns.
- **Deeper Answer:** When a Brand is chosen, the Model dropdown is populated only with that brand's models. When a Model is selected, only the RAM capacities that actually exist for that model appear. When RAM is chosen, only existing Storage sizes are enabled, and processor/display/network specs auto-fill instantly.
- **Code Evidence:** `utils/preprocessing.py` (Lines 6–53: `get_dynamic_maps()`), `static/js/prediction.js` (Lines 80–188).

---

## CATEGORY E: SOFTWARE ARCHITECTURE & DATABASE

#### Q13: Explain the high-level architecture of WorthIt.
- **Short Spoken Answer:** It follows a 4-tier client-server architecture: Client Browser (HTML5/CSS3/Vanilla JS), Web Controller (Flask in `app.py`), Machine Learning Engine (XGBoost and Scikit-Learn), and Relational Database (SQLite `worthit.db`).
- **Deeper Answer:** The client handles dynamic autofill and data presentation. When the form is submitted, an asynchronous `fetch()` POST request sends JSON to Flask's `/predict` route. The controller invokes the ML pipeline for inference and the recommender for alternatives, returning a combined JSON payload that the client renders without full page reloads.
- **Code Evidence:** `app.py` (Lines 67–85), `static/js/prediction.js` (Lines 190–226).

#### Q14: What database tables exist in `worthit.db`?
- **Short Spoken Answer:** There are two tables: **`saved_phones`** for storing user-bookmarked smartphone valuations, and **`settings`** for storing user preferences such as theme and currency.
- **Deeper Answer:** `saved_phones` has fields: `id` (PK), `brand`, `model`, `processor`, `ram`, `storage`, `predicted_price`, `current_price`, `savings`, and `timestamp`. `settings` has fields: `key` (PK) and `value`.
- **Code Evidence:** `app.py` (Lines 31–51: `init_db()`), verified in SQLite database.

#### Q15: How does your application ensure database security?
- **Short Spoken Answer:** All SQL queries use parameterized statements with `?` placeholders, completely preventing SQL injection vulnerabilities.
- **Deeper Answer:** In `app.py`, insertions and deletions pass values as tuples to `db.execute(sql, tuple)`, ensuring SQLite treats all inputs strictly as literal data rather than executable SQL syntax.
- **Code Evidence:** `app.py` (Lines 101–108, Line 115, Lines 134).

---

## CATEGORY F: FRONTEND, UI & DATA VISUALIZATION

#### Q16: How does the Dark Mode feature work and persist across page loads?
- **Short Spoken Answer:** Dark Mode toggles the `data-theme="dark"` attribute on the `<html>` element, modifying CSS custom variables. It persists in browser `localStorage` and syncs to SQLite via the `/settings` endpoint.
- **Deeper Answer:** In `templates/base.html`, an inline JavaScript IIFE checks `localStorage.getItem('theme')` before DOM rendering to prevent light-theme flashing. When switched, CSS variables for background, text, and card surfaces transition instantly without a page reload.
- **Code Evidence:** `templates/base.html` (Lines 14–23), `templates/settings.html` (Lines 40–53), `static/css/style.css`.

#### Q17: What library did you use for the chart on the results page?
- **Short Spoken Answer:** We used **Chart.js** to render an interactive HTML5 Canvas bar chart comparing the Current Listing Price against the Predicted Fair Value.
- **Deeper Answer:** In `static/js/prediction.js`, `renderChart()` reads current CSS custom variables (`--danger`, `--accent-secondary`, `--accent-highlight`) so that chart bars and gridlines dynamically adapt to the active theme (light or dark mode).
- **Code Evidence:** `static/js/prediction.js` (Lines 308–372).

#### Q18: What animations are implemented and what library drives them?
- **Short Spoken Answer:** We use **GSAP (GreenSock)** for page load timelines and card scroll-entrance animations, along with custom CSS keyframes for the full-screen pixel-sort scanning overlay.
- **Deeper Answer:** When the user clicks "Analyze Price", `#full-screen-scanner` activates with a blurred overlay and animated scanning streaks. When results return, GSAP animates the result container smoothly into view.
- **Code Evidence:** `static/js/animations.js`, `static/css/animations.css`.

---

## CATEGORY G: TESTING, CHALLENGES & VIVA DEFENSE

#### Q19: What was the most significant technical challenge you solved during this project?
- **Short Spoken Answer:** Resolving dataset variant duplications where model names had storage embedded, and calibrating the recommender engine to prevent it from suggesting phones that differed by only ₹1 or had completely mismatched specs.
- **Deeper Answer:** Early recommender logic merely searched for any phone cheaper than the listing price, often returning ₹1 savings. We re-engineered the logic to constrain searches strictly within an empirical window between fair price and listing price, applying an asymmetric multi-criteria penalty function that rewards superior RAM and storage.
- **Code Evidence:** `utils/recommender.py` (Lines 34–71).

#### Q20: What are the current limitations of WorthIt?
- **Short Spoken Answer:** It does not scrape live e-commerce prices in real time, does not factor in cosmetic wear for used/refurbished phones, and is currently limited to the Indian smartphone market in INR.
- **Deeper Answer:** Live web scraping can violate website terms of service and break on UI changes; our design deliberately focuses on offline specification valuation. Future scope includes expanding to international currencies, integrating camera quality benchmark scores, and adding an image-recognition module for physical wear assessment.
- **Code Evidence:** Documented in `ITR_Project_Master_Document.md` (Section 3.3).
