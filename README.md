# Heterogeneity in Agent-Based Models

This repository contains the **Emotional Contagion Agent-Based Model (ABM)**, calibration workflows, and analysis pipeline used in the research project titled Heterogeneity in Agent-Based Models.

The project combines:

- **Agent-Based Modelling (ABM)**
- **Approximate Bayesian Computation (ABC) using pyABC**
- **Computational experiments and sensitivity analysis**

The repository provides the **full modelling framework and reproducibility pipeline** used to generate the results presented in the associated research outputs.

---
# Repository Structure
```
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
```
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
```bash
scripts/run_pipeline.sh
```

This script will:
1. Execute the modelling notebooks
2. Run calibration experiments
3. Generate figures and outputs
4. Store executed notebooks in `results/executed_notebooks` and notebook figures in `figures/notebooks` directories
___

# Data
The `data/` directory contains:
- experimental databases generated during ABC calibration
- auxiliary datasets used for analysis
Large calibration databases may be excluded or truncated to keep the repository lightweight.
___
# Figures
Generated figures are stored in:

`figures/`

Appendix figures and additional visualisations are located in:

`figures/appendix/`

Main Paper figures are located in:

`figures/output`
___
# Reproducibility
The repository is designed to support **transparent and reproducible computational research.**

Reproducibility is supported through:
- modular model implementation `(src/)`
- documented notebooks `(notebooks/)`
- automated pipeline `(scripts/run_pipeline.sh)`
- version-controlled figures and outputs
___
# Dependencies 
All dependencies are listed in: 

`requirements.txt`
___
# License
This project is distributed under the terms specified in the `LICENSE` file.
___
# Citation
If you use this repository or build upon this work, please cite the associated research output.

`
`
