# figure_C2_alpha_posterior.py
# Appendix C – Figure C.2: alpha_posterior.png

import os
import numpy as np
import matplotlib.pyplot as plt
import pyabc


# -----------------------------
# USER SETTINGS
# -----------------------------
# Put your DB in your GitHub repo under data/appendix_C/ (recommended)
DB_PATH = "sqlite:///data/Appendix_C/Alpha_Experiment.db"  # <-- change if your filename differs
RUN_ID = 1                                                 # <-- change if needed

# Save to Path
FIG_DIR = os.path.join("figures", "appendix")
os.makedirs(FIG_DIR, exist_ok=True)

# Output (exact filename requested)
OUTFILE = "alpha_posterior.png"

# Parameters to plot (must match names stored in the DB)
PARAMS = ["Alpha_One", "Alpha_Two", "Beta"]

# Axis ranges (optional; set to None to let pyabc choose)
XRANGES = {
    "Alpha_One": (0.0, 1.0),
    "Alpha_Two": (0.0, 1.0),
    "Beta": (0.0, 0.1),
}


def main():
    # Load history from DB
    history = pyabc.History(DB_PATH)
    history.id = RUN_ID
    tmax = history.max_t

    # Basic validation: ensure params exist in the posterior dataframe
    df_last, w_last = history.get_distribution(m=0, t=tmax)
    missing = [p for p in PARAMS if p not in df_last.columns]
    if missing:
        raise KeyError(
            f"These parameters were not found in the DB posterior columns: {missing}\n"
            f"Available columns: {sorted(df_last.columns)}"
        )

    # Plot (matches notebook intent: overlay KDEs for each population)
    plt.rcParams["font.size"] = 14
    fig, axes = plt.subplots(len(PARAMS), 1, figsize=(10, 12), dpi=100)

    if len(PARAMS) == 1:
        axes = [axes]

    for i, param in enumerate(PARAMS):
        ax = axes[i]

        # Overlay populations from t=0..tmax
        for t in range(tmax + 1):
            df_t, w_t = history.get_distribution(m=0, t=t)

            # Notebook styling: earlier populations more transparent; last one black
            alpha = 1.0 if t == 0 else float(t) / max(1, tmax)
            color = "black" if t == tmax else None

            # x-range control
            xmin, xmax = (None, None)
            if param in XRANGES and XRANGES[param] is not None:
                xmin, xmax = XRANGES[param]

            pyabc.visualization.plot_kde_1d(
                df_t,
                w_t,
                x=param,
                ax=ax,
                label=f"PDF t={t}",
                alpha=alpha,
                color=color,
                xmin=xmin,
                xmax=xmax,
            )

        ax.set_title(f"{param}")
        ax.legend(fontsize="xx-small")

    fig.tight_layout()

    # Save exactly as requested
    OUTFILE = os.path.join(FIG_DIR, "alpha_posterior.png")

    fig.savefig(OUTFILE, bbox_inches="tight")
    plt.show()

    print(f"Saved: {os.path.abspath(OUTFILE)}")


if __name__ == "__main__":
    main()
