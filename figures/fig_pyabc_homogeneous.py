"""
pyABC calibration – homogeneous model

Source notebook:
Ch6_pyABC-Homogeneous.ipynb

Loads:
sqlite:///data/pyabc/homo_database_run7.db
run id = 7

Outputs (5 figures):
pyabc_homo_distance.png
homo-heatmap-pop.png
AppendixA_pyabc_output_homo.png
pyabc_alpha_beta_param.png
homo-heatmap-pop.png
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyabc
from pyabc.visualization import plot_kde_2d


OUTPUT = Path("figures/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

DB_PATH = "sqlite:///data/pyabc/homo_database.db"
RUN_ID = 7


def save(fig, name):
    path = OUTPUT / name
    fig.savefig(path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print("Saved:", path)


def plot_distance_over_time(history):

    populations = range(history.n_populations)

    median_distances = []
    q25 = []
    q75 = []

    for t in populations:
        pop = history.get_population(t)
        distances = np.array([p.distance for p in pop.particles])

        median_distances.append(np.median(distances))
        q25.append(np.percentile(distances, 25))
        q75.append(np.percentile(distances, 75))

    fig, ax = plt.subplots(figsize=(8,5))

    ax.plot(populations, median_distances, marker="o",
            color="#d62728", label="Median distance")

    ax.fill_between(populations, q25, q75,
                    alpha=0.3, color="#ff9896",
                    label="IQR (25–75%)")

    ax.set_xlabel("Population (t)")
    ax.set_ylabel("Distance (RMSE)")
    ax.set_title("Distance between Observed and Simulated Data")
    ax.legend(frameon=False)

    plt.tight_layout()

    return fig


def main():

    abc_continued = pyabc.ABCSMC(None, None)
    abc_continued.load(DB_PATH, RUN_ID)

    history = abc_continued.history

    # ---------------------------
    # Figure 1 – distance over time (Manuscript Figure 9)
    # ---------------------------
    fig = plot_distance_over_time(history)
    save(fig, "pyabc_homo_distance.png")

    # ---------------------------
    # Figure 2 – KDE evolution (Manuscript Figure 8)
    # ---------------------------
    params = ["Alpha", "Beta"]

    fig, axes = plt.subplots(1,2, figsize=(12,4))

    for i,param in enumerate(params):

        ax = axes[i]

        for t in range(history.max_t + 1):

            df, w = history.get_distribution(m=0, t=t)

            pyabc.visualization.plot_kde_1d(
                df, w,
                x=param,
                ax=ax,
                label=f"PDF t={t}",
                alpha=1.0 if t==0 else float(t)/history.max_t,
                color="black" if t==history.max_t else None
            )

        ax.set_title(param)

    axes[-1].legend(fontsize="xx-small")

    fig.tight_layout()
    save(fig, "homo-heatmap-pop.png")

    # ---------------------------
    # Figure 3 – ABC diagnostics (Appendix B Figure B.1)
    # ---------------------------
    fig, arr_ax = plt.subplots(3,1, figsize=(8,14))

    pyabc.visualization.plot_sample_numbers(history, ax=arr_ax[0])
    pyabc.visualization.plot_epsilons(history, ax=arr_ax[1])
    pyabc.visualization.plot_effective_sample_sizes(history, ax=arr_ax[2])

    fig.tight_layout()

    save(fig, "AppendixA_pyabc_output_homo.png")

    # ---------------------------
    # Figure 4 – alpha vs beta scatter (Manuscript Figure 11)
    # ---------------------------
    abc_output = history.get_population_extended()

    sns.set_style("whitegrid", {"axes.grid": False})

    g = sns.lmplot(
        y="par_Alpha",
        x="par_Beta",
        data=abc_output,
        scatter_kws={"s":80, "alpha":0.9},
        height=8,
        ci=None
    )

    g.set_axis_labels("Beta Parameter", "Alpha Parameter")
    g.fig.suptitle("pyABC: Alpha and Beta Parameters")

    g.savefig(OUTPUT / "pyabc_alpha_beta_param.png", dpi=300)
    plt.close(g.fig)

    print("Saved: pyabc_alpha_beta_param.png")

    # ---------------------------
    # Figure 5 – posterior heatmaps (Manuscript Figure 10)
    # ---------------------------
    fig = plt.figure(figsize=(20,8))

    for i,t in enumerate([0, history.max_t], start=1):

        ax = fig.add_subplot(1,2,i)

        kde_plot = plot_kde_2d(
            *history.get_distribution(m=0, t=t),
            "Beta",
            "Alpha",
            numx=200,
            numy=200,
            cmap="mako",
            colorbar=True,
            ax=ax
        )

        cb = kde_plot.collections[0].colorbar
        cb.set_label("Relative posterior density")

        ax.set_title(f"Posterior Distribution (Population {t})")
        ax.set_xlabel("Beta")
        ax.set_ylabel("Alpha")

    fig.tight_layout()

    save(fig, "homo-heatmap-pop.png")

    print("All homogeneous pyABC figures generated.")


if __name__ == "__main__":
    main()
