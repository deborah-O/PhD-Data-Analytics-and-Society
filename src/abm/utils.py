import random
import numpy as np
from typing import Optional


def set_seed(seed: Optional[int] = 122) -> None:
    """Set random seeds for reproducibility."""
    if seed is None:
        return

    random.seed(seed)
    np.random.seed(seed)
