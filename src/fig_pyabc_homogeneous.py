"""
pyABC calibration – homogeneous model

Source notebook:
pyABC-Homogeneous.ipynb

Loads:
sqlite:///data/pyabc/homo_database.db
run id = 7

Outputs (5 figures):
pyabc_homo_distance.png
pyabc_posterior_homo.png
Appendix_B_pyabc_output_homo.png
pyabc_alpha_beta_param.png
homo-heatmap-pop.png
"""

from pathlib import Path
import re
import sqlite3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyabc
from pyabc.visualization import plot_kde_2d


OUTPUT = Path("figures/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

# --- database presence check (Zenodo) ---
db_file = Path("data/pyabc/homo_database.db")
if not db_file.exists():
    raise FileNotFoundError(
        "Missing pyABC database.\n"
        "Download it from Zenodo: https://doi.org/10.5281/zenodo.18879832\n"
        "and place it at: data/pyabc/homo_database.db"
    )

DB_PATH = f"sqlite:///{db_file.resolve()}"
RUN_ID = 7

def _db_file_from_sqlalchemy_uri(uri: str) -> str:
    """
    Convert sqlite SQLAlchemy URI to a filesystem path usable by sqlite3.
    Supports:
      - sqlite:///relative/path.db
      - sqlite:////absolute/path.db
    """
    m = re.match(r"sqlite:(/*)(.*)$", uri)
    if not m:
        raise ValueError(f"Unsupported DB uri: {uri}")
    slashes, path = m.group(1), m.group(2)
    if uri.startswith("sqlite:////"):
        return "/" + path.lstrip("/")
    return path

def _find_distance_source_sqlite(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    ).fetchall()]

    def cols(t):
        return [r[1] for r in cur.execute(f"PRAGMA table_info({t});").fetchall()]

    # Candidate: particles table contains distance?
    if "particles" in tables and "distance" in cols("particles"):
        conn.close()
        return ("particles", "distance", "population_id", "id")

    # Candidate: a distances-like table contains a 'distance' column
    for t in tables:
        c = cols(t)
        if "distance" in c:
            # find a linking column
            link = None
            for candidate in ["particle_id", "population_id"]:
                if candidate in c:
                    link = candidate
                    break
            if link is not None:
                conn.close()
                return (t, "distance", link, None)

    conn.close()
    raise RuntimeError(
        "Could not locate a table/column storing 'distance'. "
        "Run: sqlite3 data/pyabc/homo_database.db '.tables' and inspect schemas."
    )
    
def save(fig, name: str):
    path = OUTPUT / name
    fig.savefig(path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print("Saved:", path)


def plot_distance_over_time(db_path: Path, run_id: int):
    """
    Notebook-equivalent distance-over-time plot, but computed from the SQLite DB
    in a schema-aware way (no hard-coded particles.distance).
    """
    table, dist_col, link_col, _ = _find_distance_source_sqlite(db_path)

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # populations always gives us t and the population id for a given run
    # We join depending on whether the distance table links by population_id or particle_id.
    if link_col == "population_id":
        query = f"""
        SELECT pop.t, d.{dist_col}
        FROM populations pop
        JOIN {table} d ON d.population_id = pop.id
        WHERE pop.abc_smc_id = ?
        ORDER BY pop.t
        """
        rows = cur.execute(query, (run_id,)).fetchall()

    elif link_col == "particle_id":
        # need to go populations -> particles -> distances-table
        query = f"""
        SELECT pop.t, d.{dist_col}
        FROM populations pop
        JOIN particles part ON part.population_id = pop.id
        JOIN {table} d ON d.particle_id = part.id
        WHERE pop.abc_smc_id = ?
        ORDER BY pop.t
        """
        rows = cur.execute(query, (run_id,)).fetchall()

    else:
        conn.close()
        raise RuntimeError(f"Unexpected link column: {link_col}")

    conn.close()

    if not rows:
        raise RuntimeError(f"No distance rows found for run_id={run_id}.")

    # Aggregate like notebook
    data = {}
    for t, d in rows:
        data.setdefault(int(t), []).append(float(d))

    populations = sorted(data.keys())
    median_distances, q25, q75 = [], [], []

    for t in populations:
        distances = np.array(data[t], dtype=float)
        median_distances.append(np.median(distances))
        q25.append(np.percentile(distances, 25))
        q75.append(np.percentile(distances, 75))

    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
    ax.plot(populations, median_distances, marker="o", color="#d62728", label="Median distance")
    ax.fill_between(populations, q25, q75, alpha=0.3, color="#ff9896", label="IQR (25–75%)")
    ax.set_xlabel("Population (t)")
    ax.set_ylabel("Distance (RMSE)")
    ax.set_title("Distance between Observed and Simulated Data (Over Populations)")
    ax.legend(frameon=False)
    plt.tight_layout()
    return fig, ax
    
def main():
    abc_continued = pyabc.ABCSMC(None, None)
    abc_continued.load(DB_PATH, RUN_ID)
    history = abc_continued.history

    # ---------------------------
    # Figure 1 – distance over time (Manuscript Figure 9)
    # ---------------------------
    fig, ax = plot_distance_over_time(db_file, RUN_ID)
    save(fig, "pyabc_homo_distance.png")

    # ---------------------------
    # Figure 2 – KDE evolution (Manuscript Figure 8)
    # ---------------------------
    params = ["Alpha", "Beta"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), dpi=100)

    for i, param in enumerate(params):
        ax = axes[i]
        for t in range(history.max_t + 1):
            df, w = history.get_distribution(m=0, t=t)
            pyabc.visualization.plot_kde_1d(
                df, w,
                x=param,
                ax=ax,
                label=f"PDF t={t}",
                alpha=1.0 if t == 0 else float(t) / history.max_t,
                color="black" if t == history.max_t else None
            )
        ax.set_title(param)

    axes[-1].legend(fontsize="xx-small")
    fig.tight_layout()
    save(fig, "pyabc_posterior_homo.png")

    # ---------------------------
    # Figure 3 – ABC diagnostics (Appendix B Figure B.1)
    # ---------------------------
    fig, arr_ax = plt.subplots(3, 1, figsize=(8, 14), dpi=100)
    pyabc.visualization.plot_sample_numbers(history, ax=arr_ax[0])
    pyabc.visualization.plot_epsilons(history, ax=arr_ax[1])
    pyabc.visualization.plot_effective_sample_sizes(history, ax=arr_ax[2])
    fig.tight_layout()
    save(fig, "Appendix_B_pyabc_output_homo.png")

    # ---------------------------
    # Figure 4 – alpha vs beta scatter (Manuscript Figure 11)
    # ---------------------------
    abc_output = history.get_population_extended()

    sns.set_style("whitegrid", {"axes.grid": False})
    g = sns.lmplot(
        y="par_Alpha",
        x="par_Beta",
        data=abc_output,
        scatter_kws={"s": 80, "alpha": 0.9},
        height=8,
        ci=None
    )
    g.set_axis_labels("Beta Parameter", "Alpha Parameter")
    g.fig.suptitle("pyABC: Alpha and Beta Parameters")

    out_path = OUTPUT / "pyabc_alpha_beta_param.png"
    g.savefig(out_path, dpi=300)
    plt.close(g.fig)
    print("Saved:", out_path)

    # ---------------------------
    # Figure 5 – posterior heatmaps (Manuscript Figure 10)
    # ---------------------------
    fig = plt.figure(figsize=(20, 8), dpi=100)

    for i, t in enumerate([0, history.max_t], start=1):
        ax = fig.add_subplot(1, 2, i)
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
