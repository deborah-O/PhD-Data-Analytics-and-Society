"""
Figure 5 – Rescaled gamma sensitivity analysis
Source notebook: notebooks/Ch5_Sensitivity-Analysis.ipynb
"""

import random
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------
# Model classes
# -----------------------

class Agent:

    def __init__(self, model, group, beta=0, alpha=0, gamma=0.1):

        self.state = 0
        self.alpha = alpha
        self.gamma = gamma
        self.beta = beta
        self.model = model
        self.group = group

    def step(self):

        if self.state == 0:
            self.become_panicked()
        else:
            self.recover()

    def become_panicked(self):

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

    def __init__(self, num_agents, num_iterations, beta):

        self.num_agents = num_agents
        self.num_iterations = num_iterations
        self.beta = beta

        self.agents = []
        self.history = []

        for i in range(num_agents):
            self.agents.append(Agent(self, "group", beta=beta, alpha=0.01))

    def get_num_infected(self):

        return sum(a.state for a in self.agents)

    def run(self):

        for t in range(self.num_iterations):

            if t >= 1:
                for a in self.agents:
                    a.step()

            self.history.append(self.get_num_infected())

        return pd.DataFrame({"iteration": range(self.num_iterations),
                             "infected": self.history})


# -----------------------
# Sensitivity analysis
# -----------------------

def run_sensitivity():

    beta_values = np.linspace(0.05, 0.6, 10)

    results = []

    for beta in beta_values:

        model = Model(1000, 1000, beta)
        df = model.run()

        df["beta"] = beta

        results.append(df)

    return pd.concat(results)


# -----------------------
# Plot
# -----------------------

def make_plot(data):

    sns.set(style="whitegrid")

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.lineplot(
        data=data,
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

    outfile = outdir / "fig5_rescaledgamma.png"

    plt.savefig(outfile, dpi=300)
    plt.close()

    print("Saved:", outfile)


# -----------------------
# Main
# -----------------------

def main():

    random.seed(122)
    np.random.seed(122)

    data = run_sensitivity()

    make_plot(data)


if __name__ == "__main__":
    main()
