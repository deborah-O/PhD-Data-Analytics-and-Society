"""
pyABC calibration – heterogeneous model

Source notebook:
pyABC-Heterogeneous.ipynb

Notebook load logic (exactly):
db_path = ("sqlite:///" + "hete_database.db")
abc_continued.load(db_path, 3)

Repo expectation:
- Put your reduced DB here (recommended):
  data/pyabc/hete_database.db

Outputs (5 figures):
pyabc_hete_distance.png
ch6_pyabc_posterior.png
Appendix_B_pyabc_hete_output.png
pyabc_beta_beta_param.png
hetero-heatmap-pop.png
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyabc
import pyabc.visualization
from pyabc.visualization import plot_kde_2d
from matplotlib.lines import Line2D


# -------------------------
# Config
# -------------------------
OUTPUT = Path("figures/output")
OUTPUT.mkdir(parents=True, exist_ok=True)
from pathlib import Path

db_file = Path("data/pyabc/hete_database.db")  # adjust name
if not db_file.exists():
    raise FileNotFoundError(
        "Missing pyABC database.\n"
        "Download it from Zenodo: https://doi.org/10.5281/zenodo.18879832\n"
        "and place it at: data/pyabc/hete_database.db"
    )

DB_PATH = f"sqlite:///{db_file.resolve()}"
RUN_ID = 3

# True parameters (exactly as in notebook)
Group1_Beta_PARAM = 0.2
Group2_Beta_PARAM = 0.6
Alpha_PARAM = 0.01

# Observation dict (exactly as in notebook)
observation = {
    "Beta_One": [0.2],
    "Beta_Two": [0.6],
    "Alpha": [0.01],
}


def save_fig(fig, filename: str, dpi: int = 300):
    out = OUTPUT / filename
    fig.savefig(out, bbox_inches="tight", dpi=dpi)
    plt.close(fig)
    print("Saved:", out)


def save_grid(grid, filename: str, dpi: int = 300):
    out = OUTPUT / filename
    grid.savefig(out, bbox_inches="tight", dpi=dpi)
    plt.close(grid.fig)
    print("Saved:", out)


# -------------------------
# Figure 1: distance over time (Manuscript Figure 15)
# -------------------------
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

    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
    ax.plot(populations, median_distances, marker="o", color="#1f77b4", label="Median distance")
    ax.fill_between(populations, q25, q75, alpha=0.3, color="#aec7e8", label="IQR (25–75%)")

    ax.set_xlabel("Population (t)")
    ax.set_ylabel("Distance (RMSE)")
    ax.set_title("Distance between Observed and Simulated Data (Over 12 Populations)")
    ax.legend(frameon=False)

    plt.tight_layout()
    return fig


def main():
    # -------------------------
    # Load stored run (exactly like notebook)
    # -------------------------
    abc_continued = pyabc.ABCSMC(None, None)
    abc_continued.load(DB_PATH, RUN_ID)
    history = abc_continued.history

    # -------------------------
    # posterior_df (derived exactly from your notebook intent)
    # (your notebook sorts by Alpha; keep that behavior)
    # -------------------------
    _df, _w = history.get_distribution(m=0, t=history.max_t)
    _df = _df.copy()
    _df["weight"] = _w
    posterior_df = _df.sort_values("Alpha", ascending=False).reset_index()

    # -------------------------
    # FIG 1: distance plot (Manuscript Figure 13)
    # -------------------------
    fig = plot_distance_over_time(history)
    save_fig(fig, "pyabc_hete_distance.png", dpi=300)

    # -------------------------
    # FIG 2: Posterior KDE 1D (Manuscript Figure 12)
    # -------------------------
    fig, axes = plt.subplots(1, 3, figsize=(22, 8), dpi=100)

    Tmax = history.max_t
    label_ts = sorted(set([0, Tmax // 2, Tmax]))

    panel_titles = [
        "Alpha",
        "Group 1: Beta Parameter",
        "Group 2: Beta Parameter",
    ]
    panel_xlabels = [
        "Alpha",
        "Group 1: Beta Parameter",
        "Group 2: Beta Parameter",
    ]

    params_in_order = ["Alpha", "Beta_One", "Beta_Two"]

    for i, param in enumerate(params_in_order):
        ax = axes[i]

        for t in range(Tmax + 1):
            df, w = history.get_distribution(m=0, t=t)

            pop_label = f"Population t={t}" if t in label_ts else None

            pyabc.visualization.plot_kde_1d(
                df,
                w,
                x=param,
                ax=ax,
                label=pop_label,
                refval=None,  # we add our own reference lines below
                alpha=0.15 if t < Tmax else 1.0,
                color="black" if t == Tmax else None,
            )

        ax.set_title(panel_titles[i], fontsize=14)
        ax.set_xlabel(panel_xlabels[i], fontsize=12)
        ax.grid(False)

        if i == 0:
            ax.set_ylabel("Posterior density", fontsize=12)
        else:
            ax.set_ylabel("")

        # Observation reference line (RED)
        if isinstance(observation, dict) and param in observation:
            obs_val = float(observation[param][0])
            ax.axvline(obs_val, color="red", linestyle="-", linewidth=1.8)

        # Posterior point estimate line (GREY dashed)
        if param in posterior_df.columns:
            ax.axvline(float(posterior_df.loc[0, param]), color="grey", linestyle="--", linewidth=1.5)

    pop_handles, pop_labels = axes[0].get_legend_handles_labels()

    ref_handles = [
        Line2D([0], [0], color="red", lw=2, linestyle="-", label="Observed parameter value"),
        Line2D([0], [0], color="grey", lw=2, linestyle="--", label="Posterior point estimate"),
    ]

    all_handles = pop_handles + ref_handles
    all_labels = pop_labels + [h.get_label() for h in ref_handles]

    fig.legend(
        all_handles,
        all_labels,
        loc="upper center",
        ncol=min(5, len(all_labels)),
        fontsize=10,
        frameon=False,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save_fig(fig, "ch6_pyabc_posterior.png", dpi=300)

    # -------------------------
    # FIG 3: diagnostics (Appendix B Figure B.2)
    # -------------------------
    fig, arr_ax = plt.subplots(3, 1, figsize=(8, 14))
    pyabc.visualization.plot_sample_numbers(history, ax=arr_ax[0])
    pyabc.visualization.plot_epsilons(history, ax=arr_ax[1])
    pyabc.visualization.plot_effective_sample_sizes(history, ax=arr_ax[2])
    fig.tight_layout()
    save_fig(fig, "Appendix_B_pyabc_hete_output.png", dpi=300)

    # -------------------------
    # FIG 4: Beta_One vs Beta_Two scatter (Manuscript Figure 15)
    # -------------------------
    abc_output = history.get_population_extended()

    sns.set(rc={"figure.figsize": (20, 15)}, font_scale=2)
    sns.set_palette("Paired")
    sns.set_style("whitegrid", {"axes.grid": False})

    g = sns.lmplot(
        x="par_Beta_One",
        y="par_Beta_Two",
        data=abc_output,
        order=2,
        scatter_kws={"s": 80, "alpha": 0.9, "color": "#02A5B0"},
        line_kws={"color": "#038992"},
        height=8.27,
        aspect=11.7 / 8.27,
        ci=None,
        truncate=False,
    )

    plt.grid(False)

    plt.scatter(
        0.2,
        0.6,
        edgecolor="black",
        facecolor="green",
        label=r"True: $\beta_1$ = {:.1f}, $\beta_2$ = {:.1f}".format(Group1_Beta_PARAM, Group2_Beta_PARAM),
        linewidth=2,
        s=120,
    )

    plt.scatter(
        0.24232129,
        0.23383305,
        edgecolor="black",
        facecolor="red",
        label=r"Estimates: $\beta_1$ = {:.3f}, $\beta_2$ = {:.3f}".format(0.24232129, 0.23383305),
        linewidth=2,
        s=120,
    )

    plt.legend()
    plt.title("pyABC: Beta Parameters", pad=10)
    plt.xlabel("Group 1: Beta Parameter")
    plt.ylabel("Group 2: Beta Parameter")

    sns.despine()

    save_grid(g, "pyabc_beta_beta_param.png", dpi=300)

    # -------------------------
    # FIG 5: 2D KDE heatmap (Manuscript Figure 14)
    # -------------------------
    fig = plt.figure(figsize=(20, 8))
    plt.rcParams["font.size"] = 14

    for i, t in enumerate([0, history.max_t], start=1):
        ax = fig.add_subplot(1, 2, i)
        kde_plot = plot_kde_2d(
            *history.get_distribution(m=0, t=t),
            "Beta_One",
            "Beta_Two",
            numx=200,
            numy=200,
            cmap="mako",
            colorbar=True,
            ax=ax,
        )

        cb = kde_plot.collections[0].colorbar
        cb.set_label("Relative posterior density", fontsize=14)

        ax.scatter(
            0.2,
            0.6,
            edgecolor="black",
            facecolor="green",
            label=r"True: $\beta_1$ = 0.20, $\beta_2$ = 0.60",
            s=120,
        )
        ax.scatter(
            0.24232129,
            0.23383305,
            edgecolor="black",
            facecolor="red",
            label=r"Estimate: $\beta_1$ = 0.242, $\beta_2$ = 0.234",
            s=120,
        )

        ax.set_title(f"pyABC: Posterior Distribution (Population = {t})", pad=10)
        ax.set_xlabel(r"$\beta_{Group 1}$")
        ax.set_ylabel(r"$\beta_{Group 2}$")
        ax.legend()

    fig.tight_layout()
    save_fig(fig, "hetero-heatmap-pop.png", dpi=300)

    print("Done: heterogeneous pyABC figures generated.")


if __name__ == "__main__":
    main()
