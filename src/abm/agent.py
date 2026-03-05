"""
Agent definition for the panic / emotional contagion ABM.
"""

import random


class Agent:
    """
    Represents an individual agent in the model.

    Agents can be in one of two states:
        0 : susceptible
        1 : panicked / infected

    Each agent has behavioural parameters controlling their probability
    of becoming panicked when interacting with other agents.
    """

    def __init__(self, model, group, beta=0, alpha=0, gamma=0.1):
        """
        Initialise a new agent.

        Parameters
        ----------
        model : Model
            Reference to the model containing the agent population.
        group : str
            Identifier for the agent's behavioural group.
        beta : float
            Additional probability of panic when interacting with
            an already panicked agent.
        alpha : float
            Baseline probability of panic.
        gamma : float
            Probability of recovery.
        """

        # Current agent state (0 = susceptible, 1 = panicked)
        self.state = 0

        # Behavioural parameters
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        # Reference to model and group membership
        self.model = model
        self.group = group

        # Temporary likelihood value calculated during interactions
        self.likelihood = 0

    def step(self):
        """
        Execute one behavioural update for the agent.

        Susceptible agents may become panicked.
        Panicked agents may recover.
        """

        if self.state == 0:
            self.become_panicked()
        else:
            self.recover()

    def __repr__(self):
        """Readable representation for debugging."""
        return f"Agent(beta={self.beta})"

    def become_panicked(self):
        """
        Infection / contagion process.

        The agent randomly selects another agent in the population and
        observes their state. If the observed agent is panicked, the
        probability of panic increases by beta.
        """

        # Randomly select another agent in the population
        agent_i = random.choice(self.model.agents)

        # Calculate panic likelihood
        if agent_i.state == 1:
            self.likelihood = self.alpha + self.beta
        else:
            self.likelihood = self.alpha

        # Random draw to determine state transition
        r_v = random.random()

        if r_v < self.likelihood:
            self.state = 1

    def recover(self):
        """
        Recovery process.

        Panicked agents return to a susceptible state with
        probability gamma.
        """

        r_v = random.random()

        if self.state == 1 and r_v < self.gamma:
            self.state = 0
