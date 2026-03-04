#!/bin/bash

pip install -r requirements.txt

# Appendix figures
python src/appendix_A_figure_A1.py
python src/appendix_B_figure_B3.py
python src/appendix_C_figure_C1.py
python src/appendix_C_figure_C2.py
python src/appendix_C_figure_C3.py

# Main figures
python src/fig4_infected_agents_comparison.py
python src/fig5_rescaledgamma.py
python src/fig6_sensitivity.py
python src/fig_pyabc_heterogeneous.py
python src/fig_pyabc_homogeneous.py
