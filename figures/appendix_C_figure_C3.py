# figure_C3_beta_posterior.py
# Appendix C – Figure C3: reproduce beta_posterior.png

import os
import pyabc
import matplotlib.pyplot as plt

# -----------------------------
# SETTINGS (edit if needed)
# -----------------------------
# Put your DB in your repo under data/Appendix_C/
DB_PATH = "sqlite:///data/Appendix_C/Beta_05-06.db"
RUN_ID = 1

OUTFILE = "beta_posterior.png"

# True values (this is your notebook "observation")
observation = {
    "Beta_One": [0.5],
    "Beta_Two": [0.6],
    "Alpha": [0.01],
}

# Order and names must match the DB column names
PARAMS = ["Beta_One", "Beta_Two", "Alpha"]


def main():
    # Load ABC history from sqlite DB
    history = pyabc.History(DB_PATH)
    history.id = RUN_ID
    tmax = history.max_t

    # Quick validation: ensure columns exist
    df_last, _w_last = history.get_distribution(m=0, t=tmax)
    missing = [p for p in PARAMS if p not in df_last.columns]
    if missing:
        raise KeyError(
            f"Missing columns in DB posterior: {missing}\n"
            f"Available columns: {sorted(df_last.columns)}"
        )

    # Create the same layout as the notebook (3 rows x 1 col)
    plt.rcParams["font.size"] = 14
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), dpi=100)

    for i, param in enumerate(PARAMS):
        ax = axes[i]

        for t in range(tmax + 1):
            df, w = history.get_distribution(m=0, t=t)

            pyabc.visualization.plot_kde_1d(
                df,
                w,
                x=param,
                ax=ax,
                label=f"PDF t={t}",
                refval=observation,  # draws the dotted orange reference line
                alpha=1.0 if t == 0 else float(t) / tmax,  # earlier populations more transparent
                color="black" if t == tmax else None,      # final population in black
            )

        ax.set_title(f"{param}")
        ax.set_ylabel("Posterior")
        ax.legend(fontsize="xx-small")

    axes[-1].set_xlabel("Parameter value")

    fig.tight_layout()
    fig.savefig(OUTFILE, bbox_inches="tight", dpi=300)
    plt.show()
    print(f"Saved: {os.path.abspath(OUTFILE)}")


if __name__ == "__main__":
    main()
