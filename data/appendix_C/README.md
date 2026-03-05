# Appendix C Data

This directory contains the **data files used to reproduce the analyses and figures presented in Appendix C of the manuscript**. The datasets are outputs from the model experiments and inference procedures and are provided to ensure that the Appendix C results are **fully reproducible**.

These files allow the figures in Appendix C to be regenerated without rerunning the full set of simulations.

## Contents

| File name             | Description                                                                                                   | Associated Figure               |
| --------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `ABM_Experiment.db`   | Database containing results from the main agent-based model (ABM) experiment used in the Appendix C analysis. | Used across Appendix C analyses |
| `Alpha_Experiment.db` | Database containing inference outputs for the **alpha parameter experiment**.                                 | Appendix C — Figure C.2         |
| `Beta_05-06.db.zip`   | Archived database containing posterior samples for the **beta parameter experiment**.                         | Appendix C — Figure C.3         |
| `test.pkl.zip`        | Processed data used to generate the **agent grouping structure** used in the Appendix analysis.               | Appendix C — Figure C.1         |

## Associated Figures

The data in this directory is used to generate the following figures in the manuscript:

* **Appendix C — Figure C.1:** Agent grouping structure used in the model.
* **Appendix C — Figure C.2:** Posterior distribution for the alpha parameter.
* **Appendix C — Figure C.3:** Posterior distribution for the beta parameter.

The corresponding figure images are located in the repository's **appendix figures directory**.

## Reproducing the Figures

To reproduce the Appendix C figures:

1. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

2. Run the analysis scripts provided in the repository:

```bash
bash scripts/run_pipeline.sh
```

or run the relevant analysis modules directly from the `src/` directory.

These scripts will read the database files in this directory and regenerate the figures used in Appendix C.

## Notes

* The `.db` files contain **SQLite databases** with simulation and inference outputs.
* Some files are provided in **compressed `.zip` format** to reduce repository size.
* The datasets are included to support **reproducibility and verification of the Appendix C results**.

For full instructions on reproducing the complete analysis and manuscript figures, see the **main repository `README.md`**.
