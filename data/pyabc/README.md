# pyABC Experiment Data

This directory contains the **pyABC calibration databases used for the inference experiments** reported in the manuscript.

Because the full SQLite databases exceed GitHub’s file size limits, they are archived on **Zenodo**.

## Data Availability

The complete calibration databases can be downloaded from:

**Zenodo DOI:** https://doi.org/10.5281/zenodo.18879832

After downloading, place the database files in this directory: data/pyabc

---

## Expected filenames

The following files should be placed in this directory:

- `homo_database.db` — homogeneous model calibration database  
- `hete_database.db` — heterogeneous model calibration database  

These SQLite databases contain the full pyABC inference history, including:

- sampled parameter values  
- accepted particles  
- particle weights  
- simulation outputs  
- distance metrics  
- posterior distributions across populations  

---

## Used run IDs

The analysis scripts load specific runs from the calibration databases:

- **Homogeneous model:** run id = `7`  
- **Heterogeneous model:** run id = `3`

---
## Reproducing pyABC Figures

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Download the calibration databases from Zenodo: https://doi.org/10.5281/zenodo.18879832

3.	Place the .db files in: data/pyabc

4. Run all the figure scripts:
```
python src/fig_pyabc_homogeneous.py
python src/fig_pyabc_heterogeneous.py
```
Generated figures will be saved to: figures/output

## Notes
- The .db files are SQLite databases generated directly by pyABC calibration runs.
- They contain the complete ABC inference history required to reproduce the calibration figures.
- Providing these databases allows reproduction of the calibration analysis without rerunning the full ABC simulations, which can be computationally intensive.

For instructions on reproducing the full analysis workflow and manuscript results, see the main repository README.md.
