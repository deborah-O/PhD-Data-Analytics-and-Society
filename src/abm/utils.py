"""
Utility functions used across the ABM modules.
"""

import random
import numpy as np
from typing import Optional


def set_seed(seed: Optional[int] = 122) -> None:
    """
    Set random seeds for reproducible simulations.

    Parameters
    ----------
    seed : int
        Seed used for Python and NumPy random generators.
    """

    if seed is None:
        return

    random.seed(seed)
    np.random.seed(seed)
