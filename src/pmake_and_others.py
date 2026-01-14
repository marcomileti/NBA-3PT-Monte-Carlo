import numpy as np
import plotly.express as px
import pandas as pd


# load learned model + weights
data = np.load("logistic_3pt_model.npz")

# assign weights 
beta_0 = data["beta_0"]
beta_1 = data["beta_1"]
bin_distances = data["bin_distances"]
bin_weights = data["bin_weights"]


def PMake(d):
    return 1 / (1 + np.exp(-(beta_0 + beta_1 * d)))

def plot_weightedBarChart():
    df_contrib = pd.DataFrame({
        "Distance": bin_distances,
        "Contribution": bin_weights,
        "P_Make": PMake(bin_distances)
    })

    # Interactive bar chart
    fig = px.bar(
        df_contrib,
        x="Distance",
        y="Contribution",
        color="P_Make",
        color_continuous_scale="Viridis",
        hover_data={"Distance": True, "Contribution": True, "P_Make": True},
        title="Weighted Contribution by Distance (click and drag to resize, double click to reset)"
    )

    fig.update_layout(
        xaxis_title="Distance (ft)",
        yaxis_title="Contribution to 3PT%",
        plot_bgcolor="white"
    )


    return fig


