import random


class Agent:

    def __init__(self, model, group, beta=0, alpha=0, gamma=0.1):

        # initialising parameters
        self.state = 0

        self.alpha = alpha
        self.gamma = gamma
        self.beta = beta

        self.model = model
        self.group = group

        self.likelihood = 0

    def step(self):

        if self.state == 0:
            self.become_panicked()

        else:
            self.recover()

    def __repr__(self):

        return f"agent beta {self.beta}"

    def become_panicked(self):

        Agent_i = random.choice(self.model.agents)

        if Agent_i.state == 1:
            self.likelihood = self.alpha + self.beta

        else:
            self.likelihood = self.alpha

        r_v = random.random()

        if r_v < self.likelihood:
            self.state = 1

    def recover(self):

        r_v = random.random()

        if self.state == 1:
            if r_v < self.gamma:
                self.state = 0
