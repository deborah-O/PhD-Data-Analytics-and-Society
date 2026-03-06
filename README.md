# PhD Data Analytics and Society

This repository contains the **Agent-Based Model (ABM)**, calibration workflows, and analysis pipeline used in the research project on **emotional contagion dynamics and behavioural diffusion**.

The project combines:

- **Agent-Based Modelling (ABM)**
- **Approximate Bayesian Computation (ABC) using pyABC**
- **Computational experiments and sensitivity analysis**

The repository provides the **full modelling framework and reproducibility pipeline** used to generate the results presented in the associated research outputs.

---

# Repository Structure
.
├── data/              # Data files and ABC calibration databases
├── figures/           # Generated figures
│   └── appendix/      # Additional figures used in appendices
│
├── notebooks/         # Interactive notebooks demonstrating the model and calibration
│   ├── Emotional_Contagion_ABM.ipynb
│   ├── pyABC-Homogeneous.ipynb
│   └── pyABC-Heterogeneous.ipynb
│
├── scripts/           # Reproducibility and pipeline scripts
│   
│
├── src/               # Core model implementation
│   ├── abm/           # Agent-based model
│   └── plotting/      # Plotting utilities
│
├── results/           # Executed notebooks and intermediate results
│
├── reproduce/         # Scripts for generating figures used in the manuscript
│
├── logs              
│
├── requirements.txt   # Python dependencies
└── README.md
___

---

# Model Overview

The model simulates **emotional contagion processes within a population of agents**.

Agents interact and may transition between behavioural states according to probabilistic rules governing:

- baseline susceptibility  
- peer influence  
- recovery dynamics  

The model allows both:

- **Homogeneous populations** (single parameter set)
- **Heterogeneous populations** (multiple behavioural groups)

Calibration of model parameters is performed using **Approximate Bayesian Computation (ABC)** with the `pyABC` library.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/PhD-Data-Analytics-and-Society.git
cd PhD-Data-Analytics-and-Society
```
Install dependencies:
```bash
pip install -r requirements.txt
```
___

# Running the Full Analysis Pipeline

The complete modelling and analysis workflow can be reproduced using the pipeline script:
```bash scripts/run_pipeline.sh
```

This script will:
- Execute the modelling notebooks
- Run calibration experiments
- Generate figures and outputs
- Store results in the results/ and figures/ directories

