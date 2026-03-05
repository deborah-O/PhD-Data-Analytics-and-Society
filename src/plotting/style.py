"""
Plotting configuration for figures used in the project.
"""

import matplotlib.pyplot as plt
import seaborn as sns


def apply_style():
    """
    Apply consistent plotting style across all figures.
    """

    plt.rc("figure", figsize=(12, 8))
    plt.rcParams["font.size"] = 24

    sns.set_style("ticks")
