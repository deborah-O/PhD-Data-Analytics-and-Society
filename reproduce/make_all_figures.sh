#!/usr/bin/env bash
set -euo pipefail

# Make output directory
mkdir -p figures/output

echo "Generating all paper figures..."

python figures/fig1.py
python figures/fig2.py
python figures/fig3.py
python figures/figA1.py
python figures/figA2.py

echo "Done. Figures saved to figures/output/"
