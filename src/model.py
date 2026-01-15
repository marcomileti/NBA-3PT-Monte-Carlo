import pandas as pd
import sqlite3
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt
from src.db import get_connection

# connect to SQLite
conn = get_connection()

# creates a two-column table of SHOT_MADE and self-computed distance 
# for shots between 23.75 (3pt_baseline) and 27 ft
df = pd.read_sql("""
SELECT
    true_distance,
    SHOT_MADE
FROM analysis_shots
WHERE is_3pt_baseline = 1
  AND true_distance BETWEEN 22 AND 27
""", conn)

# converts boolean strings to actual numerical values 
df['SHOT_MADE'] = df['SHOT_MADE'].map({
    'TRUE': 1,
    'FALSE': 0
})

# to compute distance bin weights (how many shots occured from x ft.)
bins_df = pd.read_sql("""
SELECT
    FLOOR(true_distance) AS distance_bin,
    COUNT(*) AS attempts
FROM analysis_shots
WHERE is_3pt_baseline = 1
  AND true_distance BETWEEN 22 AND 27
GROUP BY distance_bin
ORDER BY distance_bin
""", conn)

bin_distances = bins_df["distance_bin"].values # array 
bin_attempts = bins_df["attempts"].values # array 
bin_weights = bin_attempts / bin_attempts.sum()

# ----- LINEAR REGRESSION MODEL -----
X = df[['true_distance']]
y = df['SHOT_MADE']

model = LogisticRegression()
model.fit(X, y)

beta_0 = model.intercept_[0]
beta_1 = model.coef_[0][0]

# print(f"B0 = {beta_0:.3f}, B1 = {beta_1:.3f}")

d = np.linspace(22, 27, 300)
p = model.predict_proba(d.reshape(-1, 1))[:, 1]

def plot_logistic():
    fig, ax = plt.subplots()

    bin_means = (
        df.groupby(df.true_distance.astype(int))["SHOT_MADE"]
        .mean()
        .reset_index()
    )

    ax.scatter(
        bin_means.true_distance,
        bin_means.SHOT_MADE,
        label="Empirical Bin Avg"
    )

    ax.plot(d, p, label="Logistic Fit")

    ax.set_xlabel("Distance (ft)", color="white")
    ax.set_ylabel("P(Make)", color="white")
    ax.legend()
    ax.set_title("Shot Distance vs Shot Probabiltiy", color="white")
    
    # tick parameters
    ax.tick_params(colors="white")

    # key
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color("white")

    # borders
    for spine in ax.spines.values():
        spine.set_color("white")

    # bgs
    ax.set_facecolor("#111111")
    fig.patch.set_facecolor("#111111")
    return fig

#save weights from model 
np.savez(
    "logistic_3pt_model.npz",
    beta_0=beta_0,
    beta_1=beta_1, 
    bin_distances=bin_distances,
    bin_weights=bin_weights,
)

conn.close()
