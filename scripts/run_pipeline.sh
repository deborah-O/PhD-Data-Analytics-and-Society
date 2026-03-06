#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NOTEBOOK_DIR="$ROOT_DIR/notebooks"
RESULTS_DIR="$ROOT_DIR/results/executed_notebooks"
FIGURES_DIR="$ROOT_DIR/figures/notebooks"
LOG_DIR="$ROOT_DIR/logs"

mkdir -p "$RESULTS_DIR" "$FIGURES_DIR" "$LOG_DIR"

export PYTHONPATH="$ROOT_DIR/src:${PYTHONPATH:-}"

run_notebook() {
    local notebook_name="$1"
    local notebook_path="$NOTEBOOK_DIR/$notebook_name"
    local log_file="$LOG_DIR/${notebook_name%.ipynb}.log"

    echo "Running notebook: $notebook_name"

    python -m jupyter nbconvert \
        --to notebook \
        --execute "$notebook_path" \
        --output "$notebook_name" \
        --output-dir "$RESULTS_DIR" \
        --ExecutePreprocessor.timeout=1200 \
        >"$log_file" 2>&1

    echo "Finished: $notebook_name"
}

move_generated_figures() {
    echo "Collecting generated figures..."

    find "$ROOT_DIR" -maxdepth 3 -type f \( \
        -iname "*.png" -o \
        -iname "*.pdf" -o \
        -iname "*.svg" -o \
        -iname "*.jpg" -o \
        -iname "*.jpeg" \
    \) ! -path "$FIGURES_DIR/*" ! -path "$RESULTS_DIR/*" | while read -r file; do
        filename="$(basename "$file")"
        mv "$file" "$FIGURES_DIR/$filename"
        echo "Moved: $file -> $FIGURES_DIR/$filename"
    done
}

echo "Starting pipeline..."

run_notebook "Emotional_Contagion_ABM.ipynb"
run_notebook "pyABC-Homogeneous.ipynb"
run_notebook "pyABC-Heterogeneous.ipynb"

move_generated_figures

echo "Pipeline completed successfully."
