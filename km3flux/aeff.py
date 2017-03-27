"""Utilities for effective Area computation."""
import numpy as np
from scipy.integrate import romberg


def integrated_energy(gamma=1.0, e_min=1.0, e_max=100.0):
    """Integrate area below powerlaw E^-gamma."""
    # make this float, not int
    # numpy complains on `np.power(int, -foo)`
    if gamma == 1.0:
        return np.log(e_max) - np.log(e_min)
    num = np.power(e_max, 1 - gamma) - np.power(e_min, 1 - gamma)
    den = 1.0 - gamma
    return num / den


def integrate_flux_sampled(flux, energy, emin=1, emax=100):
    """Integrate a flux over energy, from given samples."""
    pass


def integrate_flux(flux, emin=1, emax=100, **kwargs):
    """Integrate a flux callable over energy.

    Uses Romberg integration.
    """
    return romberg(flux, emin, emax, vec_func=True, **kwargs)


def integrated_zenith(zen_min=0, zen_max=np.pi):
    # integrate zenith, but while in cosine
    return 2 * np.pi * np.abs(np.cos(zen_max) - np.cos(zen_min))


def aeff_scale_factor(gamma=2, solid_angle=4 * np.pi, divide_by_year=False):
    # what does this even _mean_?
    fact = 1
    if divide_by_year:
        seconds_in_a_year = 365.25 * 24 * 60 * 60
        fact = seconds_in_a_year
    return integrated_energy(gamma) * integrated_zenith() / (fact * solid_angle)


def event_ratio(fluxweight_pre, fluxweight_post):
    n_events_pre = np.sum(fluxweight_pre)
    n_events_post = np.sum(fluxweight_post)
    return n_events_post / n_events_pre


def event_ratio_1d(fluxweight_pre, fluxweight_post, binstat_pre,
                   binstat_post, bins):
    hist_pre, _ = np.histogram(binstat_pre, bins=bins,
                               weights=fluxweight_pre)
    hist_post, _ = np.histogram(binstat_post, bins=bins,
                                weights=fluxweight_post)
    return hist_post / hist_pre


def event_ratio_2d(fluxweight_pre, fluxweight_post, binstat_x_pre,
                   binstat_x_post, binstat_y_pre, binstat_y_post, xbins,
                   ybins):
    hist_pre, _, _ = np.histogram2d(binstat_x_pre, binstat_y_pre,
                                    bins=(xbins, ybins),
                                    weights=fluxweight_pre)
    hist_post, _, _ = np.histogram2d(binstat_x_post, binstat_y_post,
                                     bins=(xbins, ybins),
                                     weights=fluxweight_post)
    return hist_post / hist_pre


def effective_area(incoming_flux, weights_detected_events, emin=1, emax=100):
    """Effective Area.

    Compare the raw incoming flux (sans detector effects) to the
    events detected (including detector effects + cuts).

    Raw flux: integral over e.g. the bare Honda flux.

    detected: corrected_w2 * flux (after cuts ifneedbe)
    """
    pass
