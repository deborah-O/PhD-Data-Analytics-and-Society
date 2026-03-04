"""
Figure 6 – Sensitivity analysis

Source notebook:
notebooks/Sensitivity-Analysis.ipynb
"""
import random
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------
# Model (same logic as notebook)
# -----------------------------

class Agent:

    def __init__(self, model, beta, alpha=0.01, gamma=0.1):

        self.state = 0
        self.model = model
        self.beta = beta
        self.alpha = alpha
        self.gamma = gamma

    def step(self):

        if self.state == 0:
            self.infect()
        else:
            self.recover()

    def infect(self):

        other = random.choice(self.model.agents)

        if other.state == 1:
            likelihood = self.alpha + self.beta
        else:
            likelihood = self.alpha

        if random.random() < likelihood:
            self.state = 1

    def recover(self):

        if self.state == 1 and random.random() < self.gamma:
            self.state = 0


class Model:

    def __init__(self, n_agents, iterations, beta):

        self.n_agents = n_agents
        self.iterations = iterations
        self.beta = beta

        self.agents = [Agent(self, beta) for _ in range(n_agents)]
        self.history = []

    def get_infected(self):

        return sum(a.state for a in self.agents)

    def run(self):

        for t in range(self.iterations):

            if t > 0:
                for agent in self.agents:
                    agent.step()

            self.history.append(self.get_infected())

        return pd.DataFrame(
            {
                "iteration": range(self.iterations),
                "infected": self.history
            }
        )


# -----------------------------
# Sensitivity experiment
# -----------------------------

def run_experiment():

    beta_values = np.linspace(0.05, 0.6, 8)

    dfs = []

    for beta in beta_values:

        model = Model(1000, 1000, beta)
        df = model.run()
        df["beta"] = beta

        dfs.append(df)

    return pd.concat(dfs)


# -----------------------------
# Plot
# -----------------------------

def make_plot(df):

    sns.set(style="whitegrid")

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.lineplot(
        data=df,
        x="iteration",
        y="infected",
        hue="beta",
        palette="viridis",
        ax=ax
    )

    ax.set_xlabel("Iterations")
    ax.set_ylabel("Number of infected agents")

    plt.tight_layout()

    outdir = Path("figures/output")
    outdir.mkdir(parents=True, exist_ok=True)

    outfile = outdir / "fig6_sensitivity.png"

    plt.savefig(outfile, dpi=300)

    print("Saved:", outfile)


# -----------------------------
# Main
# -----------------------------

def main():

    random.seed(122)
    np.random.seed(122)

    df = run_experiment()

    make_plot(df)


if __name__ == "__main__":
    main()
