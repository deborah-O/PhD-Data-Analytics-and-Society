# Notebooks

This directory contains **interactive notebooks documenting the core modelling and calibration components used in the manuscript**. The notebooks provide reference implementations of the **Agent-Based Model (ABM)** and the **Approximate Bayesian Computation (ABC) calibration procedures implemented with pyABC**.

These notebooks are intended to help readers understand the **model structure, experimental setup, and calibration methodology** used in the study.

## Contents

| Notebook                    | Description                                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `Emotional_Contagion.ipynb` | Implementation of the core **Agent-Based Model (ABM)** used to simulate emotional contagion dynamics among agents. |
| `pyABC-Homogeneous.ipynb`   | Notebook demonstrating the **pyABC calibration workflow for the homogeneous model configuration**.                 |
| `pyABC-Heterogeneous.ipynb` | Notebook demonstrating the **pyABC calibration workflow for the heterogeneous model configuration**.               |

## Purpose

The notebooks serve as:

* **Interactive documentation** of the modelling framework
* Demonstrations of the **core ABM model structure**
* Examples of how **pyABC calibration experiments are configured**
* Reference material for researchers wishing to inspect or extend the model

They provide a clear overview of how the model and calibration procedures are constructed.

## Important Notes

* These notebooks **do not contain stored experimental results or manuscript figures**.
* All figures, tables, and final outputs used in the manuscript are generated through the **analysis pipeline and scripts located elsewhere in the repository**.
* The notebooks are intentionally kept **lightweight** to facilitate exploration and understanding of the model.

## Running the Notebooks

To run the notebooks interactively:

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Launch Jupyter:

```bash
jupyter notebook
```

3. Open the desired notebook from this directory.

## Reproducing Manuscript Results

The notebooks demonstrate the model and calibration setup but are **not required to reproduce the manuscript results**.

To reproduce the full analysis pipeline and generate all figures and outputs, run:

```bash
bash scripts/run_pipeline.sh
```

For full reproduction instructions and repository structure, see the **main repository `README.md`**.
