"""
Model implementation for the panic contagion ABM.
"""

import pandas as pd
from .agent import Agent


class Model:
    """
    Agent-Based Model of panic contagion.

    The model simulates behavioural contagion where agents can become
    panicked through social interaction.

    Parameters
    ----------
    num_of_agents : int
        Total population size.
    num_iterations : int
        Number of simulation time steps.
    agent_groups : dict
        Dictionary describing agent types.

        Format:
            {
                "GroupName": [beta, alpha, proportion]
            }
    """

    def __init__(self, num_of_agents, num_iterations, agent_groups):

        self.num_of_agents = num_of_agents
        self.num_iterations = num_iterations
        self.agent_groups = agent_groups

        # Model time counter
        self.time = 0

        # Store simulation results
        self.num_infected_per_iteration = []
        self.num_infected_per_iteration_groups = []

        # Create agent population
        self.agents = []

        for key in self.agent_groups.keys():

            beta, alpha, proportion = self.agent_groups[key]

            # Number of agents assigned to this group
            n_group = round(proportion * num_of_agents)

            for _ in range(n_group):

                agent = Agent(self, key, beta=beta, alpha=alpha)
                self.agents.append(agent)

        # Track infections per group
        self.infected_per_group = {g: [] for g in self.agent_groups}

    def get_num_infected(self):
        """
        Count total number of panicked agents.
        """

        return len([a for a in self.agents if a.state == 1])

    def get_num_infected_iteration_groups(self, group_key):
        """
        Count infected agents within a specific group.
        """

        return len([a for a in self.agents if a.group == group_key and a.state == 1])

    def run(self):
        """
        Execute the simulation.
        """

        for t in range(self.num_iterations):

            # Update agents after the first timestep
            for agent in self.agents:

                if t >= 1:
                    agent.step()

            # Record infections per group
            for g in self.agent_groups:

                group_agents = [a for a in self.agents if a.group == g]

                num_infected = sum([a.state for a in group_agents])

                self.infected_per_group[g].append(num_infected)

            # Record total infections
            self.num_infected_per_iteration.append(self.get_num_infected())

            # Build output datasets
            self.data = pd.DataFrame(self.infected_per_group)
            self.data.reset_index(inplace=True, drop=False)

            self.dataset = pd.DataFrame(self.num_infected_per_iteration)

            self.result = pd.merge(
                self.data,
                self.dataset,
                left_index=True,
                right_index=True
            )

            self.result.rename(
                columns={self.result.columns[-1]: "num_infected"},
                inplace=True
            )

            self.time += 1
