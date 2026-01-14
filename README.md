NBA 3-Point Line Monte Carlo Simulator
--------------------------------------

This project analyzes how moving the NBA 3-point line back by small distances (in inches) would affect league-wide shooting efficiency. Using real NBA shot-location data, I fit a probabilistic shot-make model and ran Monte Carlo simulations to estimate expected changes and uncertainty.


📊 OVERVIEW
--------------------------------------------------------------------------------

Data: NBA shot-level data (2023–24 season)

Model: Logistic regression modeling make probability as a function of distance

Simulation: Monte Carlo simulation of hypothetical 3PT line shifts

Statistics:
  - Convergence diagnostics
  - Make distribution based on distance bins (22, 23, 24, 25, 26, 27 ft)
  - Make probability as a function of distance
  - Visualization of makes (green) and misses (red) using Streamlit


🧠 METHODOLOGY ----------------------------------------------------------------

Data Cleaning (SQL)
  - Imported raw shot data into SQLite
  - Filtered valid 3PT attempts
  - Engineered true shot distance using court geometry (2D distance formulae)

Shot Make Model
  - Fit a logistic regression: P(make | distance)
  - Used as the probability engine for simulations

Monte Carlo Simulation
  - Simulated thousands of shot attempts
  - Compared baseline vs shifted 3PT line scenarios
  - Computed expected deltas in 3PT%

Statistical Validation
  - Repeated simulations to test convergence
  - Computed 95% confidence intervals on deltas


🚀 STREAMLIT APP DETAILS ------------------------------------------------------

Interactive app allowing users to:
  - Adjust number of simulated shots
  - Move the 3PT line in inches
  - View shot charts, model curves, and simulated outcomes


🛠 TECH STACK ------------------------------------------------------------------

Python (NumPy, Pandas, scikit-learn)

SQLite (SQL views + feature engineering)

Streamlit

Plotly / Matplotlib


TO RUN LOCALLY: 
  % pip install -r requirements.txt
  % streamlit run app.py

FUTURE IMPROVEMENTS:
  - Player-specific shot models
  - Angle-dependent make probabilities
  - Bayesian uncertainty modeling