# -------------------------------
# APPENDIX A: FIGURE A.1
# -------------------------------
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -------------------------------
# Agent-Based Model
# -------------------------------
class Agent:
    def __init__(self, model, group, beta=0.0, alpha=0.0, gamma=0.0):
        self.model = model
        self.group = group
        self.beta = float(beta)
        self.alpha = float(alpha)
        self.gamma = float(gamma)
        self.state = 0  # 0 = susceptible, 1 = infected/panicked

    def step(self):
        if self.state == 0:
            self.become_infected()
        else:
            self.recover()

    def become_infected(self):
        # random mixing: sample another agent
        other = random.choice(self.model.agents)

        # infection likelihood: spontaneous alpha + (beta if contact infected)
        p = self.alpha + (self.beta if other.state == 1 else 0.0)

        if random.random() < p:
            self.state = 1

    def recover(self):
        if random.random() < self.gamma:
            self.state = 0


class Model:
    def __init__(self, num_of_agents, num_iterations, agent_groups):
        """
        agent_groups: dict like
          {'Group1': [beta, alpha, gamma, proportion]}
        """
        self.num_of_agents = int(num_of_agents)
        self.num_iterations = int(num_iterations)
        self.agent_groups = agent_groups

        self.agents = []
        self.num_infected_per_iteration = []
        self.infected_per_group = {g: [] for g in agent_groups.keys()}

        # build population
        for g, (beta, alpha, gamma, prop) in agent_groups.items():
            n_g = int(round(prop * self.num_of_agents))
            for _ in range(n_g):
                self.agents.append(Agent(self, g, beta=beta, alpha=alpha, gamma=gamma))

        # if rounding misses/overfills, trim/pad to exact size
        if len(self.agents) > self.num_of_agents:
            self.agents = self.agents[: self.num_of_agents]
        while len(self.agents) < self.num_of_agents:
            # pad with the first group’s params
            g0 = next(iter(agent_groups.keys()))
            beta, alpha, gamma, _ = agent_groups[g0]
            self.agents.append(Agent(self, g0, beta=beta, alpha=alpha, gamma=gamma))

    def get_num_infected(self):
        return sum(a.state for a in self.agents)

    def run(self):
        for t in range(self.num_iterations):
            # update agents (skip t=0 warm start if you want; here we update every step)
            for agent in self.agents:
                agent.step()

            # record totals + per-group
            self.num_infected_per_iteration.append(self.get_num_infected())
            for g in self.agent_groups.keys():
                group_agents = [a for a in self.agents if a.group == g]
                self.infected_per_group[g].append(sum(a.state for a in group_agents))


# -------------------------------
# 1) Sensitivity runner: sweep α
# -------------------------------
def run_sensitivity_alpha(beta_fixed, gamma_fixed, n_points=21, reps=100, n_agents=1000, T=100, seed=123):
    """
    Sweep α in [0, 0.1] for fixed (β, γ).
    For each α, run 'reps' simulations and record steady-state mean
    proportion infected (last 20% of iterations).
    """
    alpha_vals = np.linspace(0.0, 0.1, n_points)
    rows = []

    # optional reproducibility
    random.seed(seed)
    np.random.seed(seed)

    for alpha in alpha_vals:
        for rep in range(reps):
            agent_groups = {"Group1": [beta_fixed, float(alpha), gamma_fixed, 1.0]}
            model = Model(num_of_agents=n_agents, num_iterations=T, agent_groups=agent_groups)
            model.run()

            infected_frac = np.array(model.num_infected_per_iteration, dtype=float) / n_agents
            steady_mean = infected_frac[int(0.8 * T):].mean()  # last 20%

            rows.append(
                {
                    "Alpha": float(alpha),
                    "Infected": float(steady_mean),
                    "Replicate": rep,
                    "Beta": float(beta_fixed),
                    "Gamma": float(gamma_fixed),
                }
            )

    return pd.DataFrame(rows)


# -------------------------------
# 2) Build the 2×2 grid: four (β, γ) settings
# -------------------------------
def main():
    bg_conditions = [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)]

    df_alpha_all = pd.concat(
        [run_sensitivity_alpha(b, g, n_points=21, reps=100, n_agents=1000, T=100) for b, g in bg_conditions],
        ignore_index=True,
    )
    df_alpha_all["Condition"] = df_alpha_all.apply(
        lambda r: f"β={r['Beta']:.2f}, γ={r['Gamma']:.2f}", axis=1
    )

    # -------------------------------
    # 3) Plot: Mean bars + SD error bars
    # -------------------------------
    sns.set_style("white")
    sns.set_palette("gist_rainbow")

    g = sns.FacetGrid(df_alpha_all, col="Condition", col_wrap=2, sharey=True, height=4, aspect=1.2)
    g.map_dataframe(
        sns.barplot,
        x="Alpha",
        y="Infected",
        estimator=np.mean,
        errorbar="sd",
        edgecolor="black",
        linewidth=0.3,
        palette="gist_rainbow",
    )

    g.set_titles("{col_name}")
    g.set_axis_labels("α (Spontaneous Infection Rate)", "Mean Proportion Infected")

    # fix x ticks (5 evenly spaced labels)
    unique_alphas = np.sort(df_alpha_all["Alpha"].unique())
    n = len(unique_alphas)
    tick_idx = np.linspace(0, n - 1, 5).astype(int)
    tick_labels = [f"{unique_alphas[i]:.3f}" for i in tick_idx]

    for ax in g.axes.flat:
        ax.set_ylim(0, 1)
        ax.grid(False)
        ax.set_xticks(tick_idx)
        ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=8)

    g.fig.suptitle("Appendix A1. Alpha sensitivity", fontsize=14)
    plt.tight_layout()

    out = "appendix_A1_alpha_sensitivity.png"
    plt.savefig(out, bbox_inches="tight", dpi=300)
    plt.show()
    print(f"Saved figure to: {out}")


if __name__ == "__main__":
    main()
