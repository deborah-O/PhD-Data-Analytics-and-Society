"""
Helper functions for saving and loading model outputs.
"""

import pandas as pd


def save_results_csv(df, path):
    """
    Save simulation results to CSV.
    """

    df.to_csv(path, index=False)


def load_results_csv(path):
    """
    Load simulation results from CSV.
    """

    return pd.read_csv(path)
