"""Generic Fluxes, e.g. E^-2"""

import numpy as np


def e2flux(energy, scale=1e-4):
    """E^-2 spectrum."""
    return scale * np.power(energy, -2)
