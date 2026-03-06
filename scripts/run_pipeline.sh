#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

NOTEBOOK_DIR="$ROOT_DIR/notebooks"
RESULTS_DIR="$ROOT_DIR/results"
FIGURES_DIR="$ROOT_DIR/figures/notebooks"
LOG_DIR="$ROOT_DIR/logs"

mkdir -p "$RESULTS_DIR"
mkdir -p "$FIGURES_DIR"
mkdir -p "$LOG_DIR"

export PYTHONPATH="$ROOT_DIR/src:${PYTHONPATH:-}"

echo "Figures will be saved to: $FIGURES_DIR"

run_notebook() {

    NOTEBOOK=$1

    python -m jupyter nbconvert \
        --to notebook \
        --execute "$NOTEBOOK_DIR/$NOTEBOOK" \
        --output "$NOTEBOOK" \
        --output-dir "$RESULTS_DIR" \
        --ExecutePreprocessor.timeout=1200

}

echo "Running pipeline..."

run_notebook Emotional_Contagion_ABM.ipynb
run_notebook pyABC-Homogeneous.ipynb
run_notebook pyABC-Heterogeneous.ipynb

echo "Pipeline complete."
