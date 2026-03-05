import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------
# Paths (reviewer-proof)
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]  # repo root
FIG_DIR = ROOT / "figures" / "appendix"
FIG_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE = ROOT / "data" / "Appendix_C" / "test.pkl.zip"
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Missing data file: {DATA_FILE}")

# -----------------------------
# Load simulation database
# -----------------------------
df = pd.read_pickle(DATA_FILE, compression="zip")

# -----------------------------
# Aggregate across replicates (by model_number)
# -----------------------------
Av = (
    df.groupby("model_number", as_index=False)
      .agg(
          Average=("Average", "mean"),
          Group1_Av=("Group1_Av", "mean"),
          Group2_Av=("Group2_Av", "mean"),
      )
)

# Ensure numeric
for c in ["Average", "Group1_Av", "Group2_Av", "model_number"]:
    Av[c] = pd.to_numeric(Av[c], errors="coerce")

# -----------------------------
# Extract homogeneous reference levels (horizontal lines)
# Using MODE (most frequent value) to avoid mean() issues
# -----------------------------
if Av["Group1_Av"].dropna().empty or Av["Group2_Av"].dropna().empty:
    raise ValueError("Group1_Av/Group2_Av columns are empty after cleaning. Check input data.")

group1_level = float(Av["Group1_Av"].dropna().mode().iloc[0])
group2_level = float(Av["Group2_Av"].dropna().mode().iloc[0])

# -----------------------------
# Plot: Agent Groups and Infected Fraction
# -----------------------------
sns.set_style("ticks")
plt.figure(figsize=(12, 8))

# Grey bars: heterogeneous group infected fraction (as in your figure)
sns.barplot(
    data=Av,
    x="model_number",
    y="Group1_Av",
    color="grey",
    alpha=0.6,
    linewidth=0,
    ci=None,
    label="Homogeneous: Group 2 (Infected Fraction)",
)

# Green dashed line: heterogeneous total infected fraction
sns.lineplot(
    data=Av,
    x="model_number",
    y="Average",
    linestyle="--",
    linewidth=3,
    color="#16a34a",
    label="Heterogeneous: Total Infected Fraction",
)

# Blue & magenta horizontal lines (homogeneous reference levels from data)
plt.axhline(
    group1_level,
    color="#1d4ed8",
    linewidth=4,
    label="Homogeneous: Group 1",
    zorder=5,
)
plt.axhline(
    group2_level,
    color="#d946ef",
    linewidth=4,
    label="Homogeneous: Group 2",
    zorder=5,
)

# Labels
plt.title("Agent Groups and the Fraction of Infected (Panicked) Agents")
plt.xlabel(r"$\theta_1$: Fraction of Group 1")
plt.ylabel("Steady-State Fraction of Infected Agents")

# Ticks: map model_number -> 0..1 labels
n = int(Av["model_number"].max())
ticks = [0, n * 0.2, n * 0.4, n * 0.6, n * 0.8, n]
labels = ["0", "0.2", "0.4", "0.6", "0.8", "1.0"]
plt.xticks(ticks, labels)

plt.ylim(0, 0.82)
plt.legend(loc="lower right", fontsize="small")
plt.tight_layout()

# Save
out = FIG_DIR / "Agent_Group.png"
plt.savefig(out, dpi=300, bbox_inches="tight")
plt.show()
print(f"Saved figure to: {out}")

# Optional debug print (remove later)
print("Homogeneous reference levels from data:")
print("  Group 1:", group1_level)
print("  Group 2:", group2_level)
