import numpy as np
import pandas as pd
from src.pmake_and_others import PMake

def run_sim(n=10000, shift=0, min_dist=22, max_dist=27):
    shift_ft = shift/12

    angles = np.random.uniform(0, 2 * np.pi, n)
    distances = np.random.uniform(min_dist, max_dist, n)

    x = distances * np.cos(angles)
    y = distances * np.sin(angles)

    p = PMake(distances)
    p_shift = PMake(distances + shift_ft)

    makes = np.random.binomial(1, p)
    makes_shift = np.random.binomial(1, p_shift)
    
    base_rate = makes.mean()
    shift_rate = makes_shift.mean()

    delta = shift_rate - base_rate

    df = pd.DataFrame({
        "x": x,
        "y": y,
        "distance": distances,
        "made": makes,
    })

    return df, delta

def convergence_eval(shift, n=5000, reps=500):
    deltas = []

    for i in range(reps):
        _, delta = run_sim(n=n, shift=shift)
        deltas.append(delta)

    deltas = np.array(deltas)
    running_mean = np.cumsum(deltas) / np.arange(1, reps + 1)

    return running_mean

