import random
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------
# Agent-based model
# -----------------------
class Agent:
    def __init__(self, model, group, beta=0.0, alpha=0.0, gamma=0.1):
        self.state = 0
        self.alpha = alpha
        self.gamma = gamma
        self.beta = beta
        self.model = model
        self.group = group
        self.likelihood = 0.0

    def step(self):
        if self.state == 0:
            self.become_panicked()
        else:
            self.recover()

    def become_panicked(self):
        other = random.choice(self.model.agents)
        self.likelihood = self.alpha + self.beta if other.state == 1 else self.alpha
        if random.random() < self.likelihood:
            self.state = 1

    def recover(self):
        if self.state == 1 and random.random() < self.gamma:
            self.state = 0


class Model:
    def __init__(self, num_of_agents: int, num_iterations: int, agent_groups: dict):
        """
        agent_groups format:
          { 'Group1': [beta, alpha, proportion], ... }
        """
        self.num_of_agents = num_of_agents
        self.num_iterations = num_iterations
        self.agent_groups = agent_groups

        self.time = 0
        self.num_infected_per_iteration = []
        self.infected_per_group = {g: [] for g in agent_groups}

        self.agents = []
        for group_name, (beta, alpha, proportion) in self.agent_groups.items():
            n = round(proportion * num_of_agents)
            for _ in range(n):
                a = Agent(self, group_name, beta=beta, alpha=alpha)
                self.agents.append(a)

        self.data = None
        self.result = None

    def get_num_infected(self) -> int:
        return sum(1 for a in self.agents if a.state == 1)

    def run(self):
        for t in range(self.num_iterations):
            if t >= 1:
                for agent in self.agents:
                    agent.step()

            # Track infected counts per group
            for g in self.agent_groups:
                group_agents = [a for a in self.agents if a.group == g]
                self.infected_per_group[g].append(sum(a.state for a in group_agents))

            # Track total infected
            self.num_infected_per_iteration.append(self.get_num_infected())

            # Build outputs similar to the notebook
            self.data = pd.DataFrame(self.infected_per_group)
            self.data.reset_index(inplace=True, drop=False)

            totals = pd.DataFrame(self.num_infected_per_iteration)
            self.result = pd.merge(self.data, totals, left_index=True, right_index=True)
            self.result.rename(columns={self.result.columns[-1]: "num_infected"}, inplace=True)

            self.time += 1


# -----------------------
# Figure 4
# -----------------------
def main():
    # Reproducibility
    random.seed(122)

    # Models
    homo_groups = {"Group1": [0.2, 0.01, 1.0]}
    hete_groups = {
        "Group1": [0.2, 0.01, 0.5],
        "Group2": [0.6, 0.01, 0.5],
    }

    homo_model = Model(num_of_agents=1000, num_iterations=1000, agent_groups=homo_groups)
    homo_model.run()

    hete_model = Model(num_of_agents=1000, num_iterations=1000, agent_groups=hete_groups)
    hete_model.run()

    # Merge data exactly like the notebook
    homo_df = homo_model.data.copy().rename(columns={"Group1": "homo_total"})
    hete_df = hete_model.result.copy()

    merged = pd.merge(
        homo_df[["index", "homo_total"]],
        hete_df[["index", "num_infected", "Group1", "Group2"]],
        on="index",
        how="inner",
    )

    # Plot styling
    palette = sns.color_palette("Paired", 10)

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_ylim(0, len(hete_model.agents))

    sns.lineplot(
        data=merged,
        x="index",
        y="homo_total",
        label=r"Homogeneous: Total Infected ($\beta$ = 0.2)",
        linewidth=3.2,
        color="orange",
        ax=ax,
    )

    sns.lineplot(
        data=merged,
        x="index",
        y="num_infected",
        label="Heterogeneous: Total Infected",
        linewidth=3,
        color=palette[5],
        ax=ax,
    )

    sns.lineplot(
        data=merged,
        x="index",
        y="Group1",
        label=r"Heterogeneous: Group 1 ($\beta$ = 0.2)",
        linewidth=1.5,
        color=palette[1],
        ax=ax,
    )

    sns.lineplot(
        data=merged,
        x="index",
        y="Group2",
        label=r"Heterogeneous: Group 2 ($\beta$ = 0.6)",
        linewidth=1.5,
        color=palette[2],
        ax=ax,
    )

    ax.set_title("Comparison: Number of Infected Agents Over 1000 Iterations", pad=10)
    ax.set_xlabel("Iterations (Time)", fontsize=24)
    ax.set_ylabel("Number of Infected Agents", fontsize=24)
    ax.legend(loc="upper right", fontsize=18)
    ax.grid(False)
    plt.tight_layout()

    # Save
    outdir = Path("figures/output")
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "fig4_infected_agents_comparison.png"
    plt.savefig(outfile, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {outfile}")


if __name__ == "__main__":
    main()
