# pyABC Experiment Data

This directory contains the **raw datasets generated during the Approximate Bayesian Computation (ABC) inference experiments** used in the manuscript. These databases store the results of model simulations and parameter inference runs performed using the **pyABC framework**.

The files are included to allow **full reproducibility of the inference analyses and figures reported in the manuscript**.

## Contents

| File name               | Description                                                                                                    | Model Type    |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- | ------------- |
| `homo_database_run7.db` | SQLite database containing results from the **homogeneous model inference experiment** performed with pyABC.   | Homogeneous   |
| `hete_database_run3.db` | SQLite database containing results from the **heterogeneous model inference experiment** performed with pyABC. | Heterogeneous |

Each database stores the full history of the ABC inference runs, including:

* sampled parameter values
* simulation outputs
* accepted particles
* distance metrics
* posterior distributions across generations

## Usage

These databases serve as the **primary data source for generating several figures in the manuscript**, including:

* posterior distributions of inferred parameters
* ABC distance convergence plots
* parameter exploration visualisations
* model comparison results

The analysis scripts in the repository query these databases to generate the corresponding figures.

## Reproducing Figures from the pyABC Experiments

To reproduce figures derived from these datasets:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the analysis pipeline:

```bash
bash scripts/run_pipeline.sh
```

or run the relevant scripts in the `src/analysis/` and `src/visualization/` directories.

These scripts will read the pyABC experiment databases and regenerate the figures used in the manuscript.

## Notes

* The `.db` files are **SQLite databases produced directly by pyABC runs**.
* They store the **complete inference history**, enabling detailed inspection of the ABC experiments.
* Including these files ensures that the reported inference results can be **replicated and validated without rerunning the full ABC simulations**, which can be computationally expensive.

For instructions on reproducing the full analysis workflow and manuscript results, see the **main repository `README.md`**.
