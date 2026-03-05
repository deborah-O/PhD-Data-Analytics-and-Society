"""
pyABC calibration – homogeneous model

Source notebook:
pyABC-Homogeneous.ipynb

Loads:
sqlite:///data/pyabc/homo_database_run7.db
run id = 7

Outputs (5 figures):
pyabc_homo_distance.png
homo-heatmap-pop.png
Appendix_B_pyabc_output_homo.png
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
import re


OUTPUT = Path("figures/output")
OUTPUT.mkdir(parents=True, exist_ok=True)

DB_PATH = "sqlite:///data/pyabc/homo_database_run7.db"
RUN_ID = 7

def _db_file_from_sqlalchemy_uri(uri: str) -> str:
    # expects sqlite:////absolute/path OR sqlite:///relative/path
    m = re.match(r"sqlite:(/*)(.*)$", uri)
    if not m:
        raise ValueError(f"Unsupported DB uri: {uri}")
    slashes, path = m.group(1), m.group(2)
    # for sqlite:///relative/path we want "relative/path"
    # for sqlite:////abs/path we want "/abs/path"
    if len(slashes) >= 3:
        # absolute path has 4 slashes total: sqlite:////...
        # in our regex slashes includes the ones after colon
        if uri.startswith("sqlite:////"):
            return "/" + path.lstrip("/")
    return path

def save(fig, name):
    path = OUTPUT / name
    fig.savefig(path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print("Saved:", path)

def plot_distance_over_time_sqlite(db_uri: str, run_id: int):
    """
    Plot distance over populations without using history.get_population(t),
    by reading populations.t and particle distances directly from SQLite.
    """
    db_file = _db_file_from_sqlalchemy_uri(db_uri)

    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # Check populations schema
    pop_cols = [r[1] for r in cur.execute("PRAGMA table_info(populations);").fetchall()]
    if "abc_smc_id" not in pop_cols:
        raise RuntimeError(f"'populations' table has no abc_smc_id. Columns: {pop_cols}")
    if "t" not in pop_cols:
        raise RuntimeError(f"'populations' table has no 't' column. Columns: {pop_cols}")
    if "id" not in pop_cols:
        raise RuntimeError(f"'populations' table has no 'id' column. Columns: {pop_cols}")

    # Find where distances live: usually particles.distance, sometimes in another table
    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    ).fetchall()]

    def table_cols(table):
        return [r[1] for r in cur.execute(f"PRAGMA table_info({table});").fetchall()]

    # Prefer particles.distance if available
    dist_query = None

    if "particles" in tables:
        part_cols = table_cols("particles")
        if "population_id" in part_cols and "distance" in part_cols:
            dist_query = """
                SELECT pop.t AS t, part.distance AS distance
                FROM populations pop
                JOIN particles part ON part.population_id = pop.id
                WHERE pop.abc_smc_id = ?
                ORDER BY pop.t
            """

    # Fallback: look for a table with population_id and distance
    if dist_query is None:
        for tname in tables:
            cols = table_cols(tname)
            if "population_id" in cols and "distance" in cols:
                dist_query = f"""
                    SELECT pop.t AS t, d.distance AS distance
                    FROM populations pop
                    JOIN {tname} d ON d.population_id = pop.id
                    WHERE pop.abc_smc_id = ?
                    ORDER BY pop.t
                """
                break

    if dist_query is None:
        con.close()
        raise RuntimeError(
            "Could not find a distance source. "
            "Tried particles.distance and any table with (population_id, distance)."
        )

    rows = cur.execute(dist_query, (run_id,)).fetchall()
    con.close()

    if not rows:
        raise RuntimeError(f"No distance rows found for run_id={run_id}.")

    # Aggregate distance stats per population t
    import numpy as np
    import matplotlib.pyplot as plt

    t_vals = np.array([r[0] for r in rows], dtype=int)
    d_vals = np.array([r[1] for r in rows], dtype=float)

    ts = sorted(np.unique(t_vals))
    med, q25, q75 = [], [], []
    for t in ts:
        d = d_vals[t_vals == t]
        med.append(np.median(d))
        q25.append(np.percentile(d, 25))
        q75.append(np.percentile(d, 75))

    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
    ax.plot(ts, med, marker="o", color="#d62728", label="Median distance")
    ax.fill_between(ts, q25, q75, alpha=0.3, color="#ff9896", label="IQR (25–75%)")
    ax.set_xlabel("Population (t)")
    ax.set_ylabel("Distance (RMSE)")
    ax.set_title("Distance between Observed and Simulated Data (Over Populations)")
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
    fig = plot_distance_over_time_sqlite(DB_PATH, RUN_ID)
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
    save(fig, "pyabc_posterior_homo.png")

    # ---------------------------
    # Figure 3 – ABC diagnostics (Appendix B Figure B.1)
    # ---------------------------
    fig, arr_ax = plt.subplots(3,1, figsize=(8,14))

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
