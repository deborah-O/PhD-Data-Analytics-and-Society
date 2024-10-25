# Heterogeneity in Agent-based models 
This repository contains research and scripts for the PhD thesis, focusing on Agent-Based Models (ABM) and model calibration techniques. This work explores how heterogeneity among agents affects model calibration and parameter identification using Bayesian computation and emotional contagion modeling.

## Research Highlights
Examines how agent heterogeneity affects calibration accuracy.
Discusses implications of parameter non-identification on policy decisions.

## Contents
[Emotional_Contagion.ipynb]([https://www.example.com](https://github.com/deborah-O/PhD-Data-Analytics-and-Society/blob/main/Emotional_Contagion.ipynb)): Jupyter Notebook on emotional contagion in heterogeneous vs. homogeneous agent models.
[pyABC-Heterogeneous.ipynb](https://github.com/deborah-O/PhD-Data-Analytics-and-Society/blob/main/pyABC-Heterogeneous.ipynb) and [pyABC-Homogeneous.ipynb](https://github.com/deborah-O/PhD-Data-Analytics-and-Society/blob/main/pyABC-Homogeneous.ipynb): Notebooks for Bayesian calibration in heterogeneous and homogeneous scenarios.

## Project Summary
Agent-based models are an incredibly flexible tool that among other things, allow modellers to capture heterogeneity in agent attributes, characteristics, and behaviours. This study defines heterogeneity in agent-based models as agent granularity: the level of description used to define the agent population. Consequently, this increased complexity can make the already challenging tasks of calibration and parameter identification, even more difficult. Although modellers recognise the significance of model calibration, the process of uniquely determining model input from any given model output is overlooked. This thesis proposes an impact of heterogeneity in agent-based models is parameter non-identification.
 
To this end, this research conducts a thorough examination of agent heterogeneity by the comparative study of homogeneous and heterogeneous scenarios in agent-based models. Using an emotional contagion case study model and approximate Bayesian computation calibration, it finds that the introduction of heterogeneity results in inaccurate parameter calibration compared to the homogeneous case. This study proposes the inaccurate results as the consequence of a failure to uniquely distinguish the effect of additional parameters in the model. Furthermore, failing to identify model parameters limits the predictive or forecasting power of the agent-based model. A simple case study is used to demonstrate that the use of unidentifiable models to inform real-world governmental and social policies can lead to erroneous conclusions and potentially unsound interventions.
 
## License
This project is licensed under the MIT License.
