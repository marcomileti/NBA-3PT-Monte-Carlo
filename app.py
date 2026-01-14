import streamlit as st
import matplotlib.pyplot as plt
from sim import run_sim, convergence_eval
from shotChart import plot_shot_chart
from pmake_and_others import plot_weightedBarChart
from model import plot_logistic

st.title("NBA 3PT Line Monte Carlo Simulator")

st.text("Although more accurate, the graph below becomes nonsensical after ~5,000 shots simulated")

n = st.slider("Shots simulated", 50, 50_000, 50, step=50)
inches = st.slider("Move 3PT line back (inches)", 0, 24, 0)

three_pt_line = 23.75 + inches / 12

df, delta = run_sim(n=n, shift=inches)
mean_delta = convergence_eval(shift=inches)

baseline = df["made"].mean()
adjusted = df[df["distance"] >= three_pt_line]["made"].mean()

st.metric("Baseline 3PT%", f"{baseline:.3%}")
st.metric("Adjusted 3PT%", f"{adjusted:.3%}")

fig = plot_shot_chart(df, three_pt_line)
st.plotly_chart(fig, use_container_width=True)

fig2 = plot_weightedBarChart()
st.plotly_chart(fig2, use_container_width=True)

fig3 = plot_logistic()
st.plotly_chart(fig3)

st.subheader("Monte Carlo Convergence")

st.text(
    "Shows how the estimated change in 3PT% (Δ) stabilizes "
    "as more Monte Carlo simulations are run"
)

running_mean = convergence_eval(
    shift=inches,
    n=min(n, 5000), # cap for performance
    reps=500
)

fig_conv, ax = plt.subplots()
ax.plot(running_mean)
ax.axhline(running_mean[-1], linestyle="--")
ax.set_xlabel("Monte Carlo Runs")
ax.set_ylabel("Estimated Δ")
ax.set_title("Convergence of Monte Carlo Estimate")

st.pyplot(fig_conv)
