import numpy as np
import plotly.express as px

def plot_shot_chart(df, three_pt_line):
    df["result"] = df["made"].map({1: "Make", 0: "Miss"})

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="result",
        opacity=0.6,
        color_discrete_map={"Make": "green", "Miss": "red"}
    )

    theta = np.linspace(0, 2 * np.pi, 500)
    fig.add_scatter(
        x=three_pt_line * np.cos(theta),
        y=three_pt_line * np.sin(theta),
        mode="lines",
        name="3PT Line"
    )

    fig.update_layout(
        xaxis=dict(range=[-30, 30], scaleanchor="y"),
        yaxis=dict(range=[-5, 35]),
        plot_bgcolor="white"
    )

    return fig
