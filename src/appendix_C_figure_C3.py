# figure_C3_beta_posterior.py
# Appendix C – Figure C3

import os
import zipfile
import pyabc
import matplotlib.pyplot as plt

# -----------------------------
# FILE PATHS
# -----------------------------
ZIP_DB = "data/Appendix_C/Beta_05-06.db.zip"
DB_FILE = "data/Appendix_C/Beta_05-06.db"

RUN_ID = 1
OUTFILE = "beta_posterior.png"

# True parameter values
observation = {
    "Beta_One": [0.5],
    "Beta_Two": [0.6],
    "Alpha": [0.01],
}

PARAMS = ["Beta_One", "Beta_Two", "Alpha"]


# -----------------------------
# Unzip database if needed
# -----------------------------
if not os.path.exists(DB_FILE):
    with zipfile.ZipFile(ZIP_DB, "r") as zip_ref:
        zip_ref.extractall("data/Appendix_C")

DB_PATH = "sqlite:///" + DB_FILE


# -----------------------------
# Load ABC history
# -----------------------------
history = pyabc.History(DB_PATH)
history.id = RUN_ID
tmax = history.max_t


# -----------------------------
# Plot figure
# -----------------------------
plt.rcParams["font.size"] = 14
fig, axes = plt.subplots(3, 1, figsize=(10, 12))

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
            refval=observation,
            alpha=1.0 if t == 0 else float(t)/tmax,
            color="black" if t == tmax else None
        )

    ax.set_title(param)
    ax.set_ylabel("Posterior")
    ax.legend(fontsize="xx-small")

axes[-1].set_xlabel("Parameter value")

plt.tight_layout()

plt.savefig(OUTFILE, dpi=300, bbox_inches="tight")
plt.show()
