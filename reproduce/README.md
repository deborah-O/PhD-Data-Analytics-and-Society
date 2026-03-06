# Reproducing Manuscript Figures

This directory contains scripts used to **generate the figures included in the main paper**.

The scripts run the required analysis and produce the figures used in the manuscript.

## Requirements

Install the required Python dependencies from the project root:

```bash
pip install -r requirements.txt
```

## Generate All Figures 

To generate all figures used in the manuscript, run:
```bash
reproduce/make_all_figures.sh
```

The generated figures will be saved to the appropriate directories within the repository (typically `figures/`).

## Notes

- These scripts reproduce **figures used in the main paper only.**
- Additional exploratory figures and demonstrations can be found in the `notebooks/` directory.
- The full modelling and calibration workflow can be executed using:
```bash
scripts/run_pipeline.sh
```
