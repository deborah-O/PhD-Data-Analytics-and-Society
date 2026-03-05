import pandas as pd
from .agent import Agent


class Model:

    def __init__(self, num_of_agents, num_iterations, agent_groups):

        self.num_of_agents = num_of_agents
        self.num_iterations = num_iterations
        self.agent_groups = agent_groups

        self.time = 0

        # storing results
        self.num_infected_per_iteration = []
        self.num_infected_per_iteration_groups = []

        # create agents
        self.agents = []

        for key in self.agent_groups.keys():

            beta, alpha, proportion = self.agent_groups[key]

            for i in range(round(proportion * num_of_agents)):

                agent = Agent(self, key, beta=beta, alpha=alpha)

                self.agents.append(agent)

        self.infected_per_group = {}

        for g in self.agent_groups:
            self.infected_per_group[g] = []

    def get_num_infected(self):

        return len([a for a in self.agents if a.state == 1])

    def get_num_infected_iteration_groups(self, group_key):

        return len([a for a in self.agents if a.group == group_key and a.state == 1])

    def run(self):

        for t in range(self.num_iterations):

            for agent in self.agents:

                if t >= 1:
                    agent.step()

            for g in self.agent_groups:

                group_agents = [a for a in self.agents if a.group == g]

                num_infected = sum([a.state for a in group_agents])

                self.infected_per_group[g].append(num_infected)

            self.num_infected_per_iteration.append(self.get_num_infected())

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
