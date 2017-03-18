"""Utilities for effective Area computation."""
import numpy as np


def integrated_energy(gamma=1.0, e_min=1.0, e_max=100.0):
    # make this float, not int
    # numpy complains on `np.power(int, -foo)`
    if gamma == 1.0:
        return np.log(e_max) - np.log(e_min)
    num = np.power(e_max, 1 - gamma) - np.power(e_min, 1 - gamma)
    den = 1.0 - gamma
    return num / den


def integrated_zenith(zen_min=0, zen_max=np.pi):
    return 2 * np.pi * np.abs(np.cos(zen_max) - np.cos(zen_min))


def aeff_scale_factor(gamma=2, solid_angle=4 * np.pi):
    seconds_in_a_year = 365.25 * 24 * 60 * 60
    return integrated_energy(gamma) * integrated_zenith() * \
        seconds_in_a_year / solid_angle
