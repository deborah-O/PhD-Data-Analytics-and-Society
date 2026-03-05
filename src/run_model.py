"""
Script for running the panic contagion ABM.
"""

from abm import Model, set_seed
from plotting.style import apply_style


def main():
    """Run a basic simulation."""

    apply_style()
    set_seed(122)

    agent_groups = {
        "Group1": [0.2, 0.01, 1.0]
    }

    model = Model(
        num_of_agents=1000,
        num_iterations=1000,
        agent_groups=agent_groups
    )

    model.run()

    print(model.result.tail())


if __name__ == "__main__":
    main()
