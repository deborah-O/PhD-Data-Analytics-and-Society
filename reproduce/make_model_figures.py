from subprocess import run

SCRIPTS = [
    "figures/fig4_infected_agents_comparison.py",
    "figures/fig5_rescaledgamma.py",
    "figures/fig6_sensitivity.py",
]

for s in SCRIPTS:
    print(f"Running {s}")
    run(["python", s], check=True)

print("Done. Model figures are in figures/output/")
