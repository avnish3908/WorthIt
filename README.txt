================================================================================
WorthIt - AI-Powered Smartphone Price Predictor
================================================================================

PROJECT OVERVIEW
----------------
WorthIt is an AI-powered web application that helps users determine the fair 
market value of a smartphone based on its specifications (Brand, RAM, Storage, 
Processor, Battery, etc.). It features a machine learning backend built with 
Flask and XGBoost, and a highly polished, interactive frontend using HTML, CSS, 
Vanilla JavaScript, GSAP animations, and Chart.js.

Key Aesthetics:
- Minimalist, editorial "Paper" theme (ivory background, terracotta/gold accents)
- Seamless Dark Mode toggle that persists across pages.
- Full-screen "pixel-sort" AI scanning animation during predictions.

--------------------------------------------------------------------------------
HOW TO START THE APPLICATION
--------------------------------------------------------------------------------
To run WorthIt locally on your machine, follow these steps:

1. Open your Terminal or Command Prompt.
2. Navigate to the project folder where `app.py` is located.
   (e.g., `cd path/to/WorthIt`)
3. Install the required Python packages if you haven't already:
   `pip install Flask pandas numpy scikit-learn xgboost joblib`
4. Start the Flask application by running:
   `python app.py`
5. Open your web browser and go to:
   http://127.0.0.1:5000/

--------------------------------------------------------------------------------
HOW TO PRESENT & DEMO THE PROJECT
--------------------------------------------------------------------------------
When presenting WorthIt to an audience or evaluator, follow this flow to 
highlight its best features:

1. THE LANDING PAGE (Home)
   - Start at the root URL (/).
   - Highlight the smooth GSAP scroll animations (text fading in, elements floating).
   - Point out the clean "editorial" aesthetic with the terracotta and gold colors.

2. THE PREDICTION ENGINE (Predict Price)
   - Click "Try it Now" or navigate to "Predict Price".
   - Demonstrate the smart form: Select a Brand (e.g., Apple) and show how the 
     Model and Processor fields automatically update based on your selection.
   - Fill out the specs (RAM, Storage, etc.).
   - Point out the "Live Preview" panel on the right: it updates in real-time as 
     you type, and the icon changes to match the selected brand.

3. THE AI SCANNING ANIMATION (The "Wow" Moment)
   - Type in a Current Market Price and click "Analyze Price".
   - Tell your audience to watch the screen: a full-screen, blurred overlay will 
     appear with a terracotta and gold "pixel-sort" scanning animation that sweeps 
     across the screen, giving a premium "AI is thinking" feel.

4. THE RESULTS DASHBOARD
   - Once the scan finishes, show the results grid.
   - Point out the dynamic Chart.js bar chart comparing the Current Price to the 
     Predicted Fair Price.
   - Highlight the "Recommendation Badge" (e.g., Good Deal in green, or 
     Overpriced in red) and the AI Confidence Score in gold.
   - Scroll down to the "Smarter Alternatives" section which suggests better phones.
   - Click the "Save" button at the top right to bookmark the result.

5. SETTINGS & DARK MODE (The Polish)
   - Navigate to the "Settings" page.
   - Click the "Dark Theme" option.
   - Show how the entire site instantly transitions to a deep charcoal/ivory theme 
     without reloading the page.
   - Navigate back to the "Predict Price" page to prove that the Dark Mode state 
     was saved and that even the Chart.js graphs updated their gridlines and colors 
     automatically to match the dark theme.

6. SAVED PHONES (Database Integration)
   - Navigate to the "Saved Phones" page.
   - Show that the phone you saved earlier is listed here.
   - Explain that this data (along with your theme preference) is saved persistently 
     (using SQLite and LocalStorage).

--------------------------------------------------------------------------------
TECHNICAL STACK SUMMARY
--------------------------------------------------------------------------------
- Backend: Python, Flask
- Machine Learning: XGBoost Regressor (trained on synthetic smartphones.csv), Scikit-Learn pipelines
- Database: SQLite (for saved predictions and settings)
- Frontend: HTML5, Vanilla CSS (CSS Variables for theming), Vanilla JavaScript
- Libraries: Chart.js (Data Visualization), GSAP (Animations), FontAwesome (Icons)
