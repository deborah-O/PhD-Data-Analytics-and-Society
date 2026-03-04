import pyabc
import matplotlib.pyplot as plt
from pyabc.visualization import plot_kde_2d

# -----------------------------
# Database
# -----------------------------
DB_PATH = "sqlite:///data/pyabc/hete_database_run3.db"
RUN_ID = 3

history = pyabc.History(DB_PATH)
history.id = RUN_ID

tmax = history.max_t

# -----------------------------
# Create figure
# -----------------------------
fig = plt.figure(figsize=(12,10))
plt.rcParams["font.size"] = 14


# -------- Panel 1: Alpha vs Beta1 --------
ax1 = fig.add_subplot(2,1,1)

plot_kde_2d(
    *history.get_distribution(m=0, t=tmax),
    x="Beta_One",
    y="Alpha",
    xmin=0,
    xmax=1,
    ymin=0,
    ymax=0.1,
    cmap="mako",
    colorbar=True,
    ax=ax1
)

ax1.set_title("Posterior: α vs β (Group 1)")
ax1.set_xlabel(r"$\beta_{1}$")
ax1.set_ylabel(r"$\alpha$")


# -------- Panel 2: Alpha vs Beta2 --------
ax2 = fig.add_subplot(2,1,2)

plot_kde_2d(
    *history.get_distribution(m=0, t=tmax),
    x="Beta_Two",
    y="Alpha",
    xmin=0,
    xmax=1,
    ymin=0,
    ymax=0.1,
    cmap="mako",
    colorbar=True,
    ax=ax2
)

ax2.set_title("Posterior: α vs β (Group 2)")
ax2.set_xlabel(r"$\beta_{2}$")
ax2.set_ylabel(r"$\alpha$")


# -----------------------------
# Save figure
# -----------------------------
fig.suptitle("Appendix B – Figure B3: Posterior distributions of α and β", fontsize=16)

plt.tight_layout()

plt.savefig(
    "Appendix_B_Figure_B3.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
