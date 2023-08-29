# %%
"""
<center> <h1> Agent-Based Model of Panic</h1> </center>
"""

# %%
"""
### Import Packages
"""

# %%
import random
import matplotlib.pyplot as plt
import pandas as pd
import statistics
import math
import numpy as np
import seaborn as sns

# %%
"""
### Figure Settings
"""

# %%
plt.rc('figure', figsize=(12, 8))
plt.rcParams['font.size'] = '14'
sns.set_style("ticks", {'font.family': 'Times New Roman'})
sns.set_palette("Paired")

# %%
"""
### Model Class
"""

# %%
class Model():
    '''
    Panic Model

    Description:
        An Agent-Based Model (ABM) that synchronously `steps`
        step()

    Params:
        num_of_agents 
        num_iterations
        agent_groups 
        
    Returns:
        get_num_infected()
    '''


    def __init__(self, num_of_agents, num_iterations, agent_groups): 
        '''
        Create a new model, reading parameters from a keyword argument
        dictionary.
        '''
        
        self.num_of_agents = num_of_agents #Number of Agent_Pop
        self.num_iterations = num_iterations #Number of Iterations
        self.agent_groups = agent_groups #Proportion of Agents in each group, between 0-1. 

        self.time = 0 #model time
        
        #creating lists
        self.num_infected_per_iteration = []
        
        #create the agents
        self.agents = []
        
        #create agent groups based on specified number of groups
        for key in self.agent_groups.keys():
#             print(key)
            for i in range(round(self.agent_groups[key][2] * num_of_agents)):
                agent = Agent(self, key, key[0], key[1])
                agent.beta = self.agent_groups[key][0]
                agent.alpha = self.agent_groups[key][1]
#                 print(agent)
                self.agents.append(agent)
        
        self.infected_per_group = {}
        
        for g in self.agent_groups:
            self.infected_per_group[g] = []
        

    def get_num_infected(self):
        '''
        Returns the number of infected agents.
        '''
        return len(([a for a in self.agents if a.state==1])) 
    
    def run(self):
        '''
        Iterate model forward one second.
        '''
        for t in range(self.num_iterations):
            for agent in self.agents:
                if t >=1:
                    agent.state = 0
           
            for g in self.agent_groups:
                group_agents = [a for a in self.agents if a.group == g]
                num_infected = sum([a.state for a in group_agents])
                self.infected_per_group[g].append(num_infected)
        
    
            self.num_infected_per_iteration.append(self.get_num_infected())
        
            #Prepares model output.
            self.data = pd.DataFrame(self.infected_per_group)
            self.data.reset_index(inplace = True, drop = False)
            self.dataset = pd.DataFrame(self.num_infected_per_iteration)
            self.result = pd.merge(self.data, self.dataset, left_index=True, right_index=True)
            self.result.rename(columns={self.result.columns[-1]: "num_infected" }, inplace = True)
        
    
            self.time += 1
        


# %%
"""
### Agent Class
"""

# %%
class Agent():
    '''
    A class representing a generic agent for the Panic ABM.
    '''
    
    def __init__(self, Model, group, beta, alpha, gamma= 0.1):
        '''
        Initialise a new agent.

        Desctiption:
            Creates a new agent and assigns it to the suspectible state.
            All agents are assigned rates for alpha, beta and gamma parameter values
            Agent likelihood are set to 0 to begin with

        Parameters:
            model - a pointer to the Model Class that is creating
            this agent
            group - a pointer to agent's the Agent Group
        '''
        # Required
        self.state = 0 # 0 Suspectible, 1 Infected
        
        self.alpha = alpha 
        self.gamma = gamma
        self.beta = beta 
        
        self.model = Model
        self.group = group
        
        self.likelihood = 0 # Updated once model begins

    def step(self):
        '''
        Iterate the agent.

        Description:
            If they are suspectible then they can become panicked, if they are infected they can recover.
        '''
        if self.state == 0:
            self.become_panicked()
            
        else:
            self.recover()
        
        
    def become_panicked(self):
        '''
        Process of infection. 
        The agent randomly chooses an agent from the population and observe their state. 
        If the comparative agent is infected, agent computes a likelihood with alpha and beta.
        If the comparative agent is suspectible, agent computes their likelihood with alpha.
        
        To switch states, the likelihood has to greater than a randomly generated number.
        '''
        
        Agent_i = random.choice(self.model.agents)
        
        if Agent_i.state == 1:
            self.likelihood = self.alpha + self.beta
        else:
            self.likelihood = self.alpha
        
        r_v = random.random()
        if r_v < self.likelihood: 
            self.state = 1
       
    def recover(self): 
        '''
        Process of recovery. 
        If the agent is infected, then given a randomly generated number, they can recover to a suspectible state.
        '''
        r_v = random.random()
        if self.state == 1:
            if r_v < self.gamma:
                self.state = 0

# %%
"""
### Run Model
"""

# %%
#Run model
agent_groups = {'Group1':[0.2, 0.01, 1.0]}
model = Model(num_of_agents=1000, num_iterations=1000, agent_groups=agent_groups)
model.run()