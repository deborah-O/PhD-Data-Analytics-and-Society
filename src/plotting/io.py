import pandas as pd


def save_results_csv(df, path):

    df.to_csv(path, index=False)


def load_results_csv(path):

    return pd.read_csv(path)
