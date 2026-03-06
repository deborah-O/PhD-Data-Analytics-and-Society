# Notebooks

This directory contains **interactive notebooks documenting the core modelling and calibration components used in the manuscript**. The notebooks provide reference implementations of the **Agent-Based Model (ABM)** and the **Approximate Bayesian Computation (ABC) calibration procedures implemented with pyABC**.

These notebooks are intended to help readers understand the **model structure, experimental setup, and calibration methodology** used in the study.

---

## Contents

| Notebook | Description |
|--------|--------|
| `Emotional_Contagion_ABM.ipynb` | Implementation and demonstration of the **Agent-Based Model (ABM)** used to simulate emotional contagion dynamics among agents. |
| `pyABC-Homogeneous.ipynb` | Demonstrates the **pyABC calibration workflow for the homogeneous model configuration**. |
| `pyABC-Heterogeneous.ipynb` | Demonstrates the **pyABC calibration workflow for the heterogeneous model configuration**. |

---

## Purpose

The notebooks serve as:

- **Interactive documentation** of the modelling framework  
- Demonstrations of the **core ABM model structure**  
- Examples of how **pyABC calibration experiments are configured**  
- Reference material for researchers wishing to inspect or extend the model  

They provide a transparent overview of how the model and calibration procedures are constructed.

---

## Important Notes

- These notebooks **do not contain stored experimental results or manuscript figures**.
- All figures, tables, and final outputs used in the manuscript are generated through the **analysis pipeline and scripts located elsewhere in the repository**.
- The notebooks are intentionally kept **lightweight** to facilitate exploration and understanding of the model.

---

## Running the Notebooks

To run the notebooks interactively:

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

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

## Importing the Model Code

The notebooks import the core model implementation from the 

```bash 
src/
```
directory.

If running notebooks from this directory, you may need to ensure the src folder is available in the Python path. This is handled in the notebooks using:
```bash
import sys
from pathlib import Path
sys.path.append(str(Path("../src").resolve()))
```
## Reproducing Manuscript Results

The notebooks demonstrate the model and calibration setup but are **not required to reproduce the manuscript results**.

To reproduce the full analysis pipeline and generate all figures and outputs, run:

```bash
bash scripts/run_pipeline.sh
```
