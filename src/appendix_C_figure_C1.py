import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------
# Resolve paths relative to repo root
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]  # repo root
FIG_DIR = ROOT / "figures" / "appendix"
FIG_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE = ROOT / "data" / "Appendix_C" / "test.pkl.zip"
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Missing data file: {DATA_FILE}\n"
        "Make sure the repository contains data/Appendix_C/test.pkl.zip "
        "(or update the filename/path in this script)."
    )

# -----------------------------
# Load simulation database
# -----------------------------
df = pd.read_pickle(DATA_FILE, compression="zip")

# -----------------------------
# Aggregate across replicates
# -----------------------------
Av = (
    df.groupby("model_number", as_index=False)
      .agg(
          Average=("Average", "mean"),
          Group1_Av=("Group1_Av", "mean"),
          Group2_Av=("Group2_Av", "mean")
      )
)

# -----------------------------
# Plot Figure C.1
# -----------------------------
sns.set_style("ticks")

plt.figure(figsize=(12,8))

# total infected (green dashed)
sns.lineplot(
    data=Av,
    x="model_number",
    y="Average",
    linestyle="--",
    linewidth=3,
    color="#16a34a",
    label="Heterogeneous: Total Infected Fraction"
)

# compute steady-state group infection levels from data
group1_level = Av["Group1_Av"].mean()
group2_level = Av["Group2_Av"].mean()

# homogeneous group 1 (blue horizontal line)
plt.axhline(
    group1_level,
    color="#1d4ed8",
    linewidth=4,
    label="Homogeneous: Group 1"
)

# homogeneous group 2 (magenta horizontal line)
plt.axhline(
    group2_level,
    color="#d946ef",
    linewidth=4,
    label="Homogeneous: Group 2"
)

# grey bars
sns.barplot(
    data=Av,
    x="model_number",
    y="Group1_Av",
    color="grey",
    alpha=0.6,
    linewidth=0,
    errorbar=None,
    label="Homogeneous: Group 2 (Infected Fraction)"
)

# labels
plt.title("Agent Groups and the Fraction of Infected (Panicked) Agents")
plt.xlabel(r"$\theta_1$: Fraction of Group 1")
plt.ylabel("Steady-State Fraction of Infected Agents")

# ticks (0 → 1)
n = Av["model_number"].max()
ticks = [0, n*0.2, n*0.4, n*0.6, n*0.8, n]
labels = ["0","0.2","0.4","0.6","0.8","1.0"]
plt.xticks(ticks, labels)

plt.ylim(0,0.82)

plt.legend(loc="lower right", fontsize="small")

plt.tight_layout()

# save figure
out = FIG_DIR / "Agent_Group.png"
plt.savefig(out, dpi=300, bbox_inches="tight")
print(f"Saved figure to: {out}")

