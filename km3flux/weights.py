"""Utilities to compute event weights."""
import numpy as np


def nu_wgt(w2, n_gen, adjust_orca_overlap=False, energy=None):
    """Get neutrino weight, optionally adjust for ORCA energy overlap.

    Aka crazy Joao hack:
        // If energy in overlap region, divide by 2
        if(nu.E>3 && nu.E<5) weight /= 2;
   """
    wgt = w2 / n_gen
    if adjust_orca_overlap and energy:
        overlap_mask = (3 <= energy) & (energy <= 5)
        wgt[overlap_mask] /= 2
    return wgt


def atmu_wgt(livetime_sec):
    """Compute mupage weight."""
    return 1 / livetime_sec


def make_weights(w2, n_gen, livetime_sec, is_neutrino,
                 adjust_orca_overlap=False, energy=None):
    """Generate weights for events of mixed flavor.

    This assumes that all arrays have the same length. If you have mixed
    neutrino + atmu events, just pad the unused fields (e.g. livetime for
    neutrinos, w2 for atmu) with anything, they will be ignored.

    Of course, if your data has only neutrinos/mupage, use the dedicated
    methods for them instead: `nu_wgt` and `atmu_wgt`.

    Parameters
    ==========
    w2: array-like
    n_gen: scalar or array-like
        number ov generated events *in the entire production*
        for gSeaGen, this is already n_gen.
        For GenHen, this is `n_gen * n_files`
    livetime_sec: scalar or array-like
        livetime *in seconds*
    is_neutrino: boolean array
    adjust_orca_overlap: bool, default=False
        Some Orca productions (2016) have energy overlap, between 3-5 GeV.
        If set True, you need to pass in an energy.
    energy: array, default=None
        If `adjust_orca_overlap` is set, you need to pass this.
    """
    wgt = np.ones(len(w2))
    wgt[is_neutrino] = nu_wgt(w2[is_neutrino], n_gen[is_neutrino],
                              adjust_orca_overlap=adjust_orca_overlap,
                              energy=energy)
    wgt[~is_neutrino] = atmu_wgt(livetime_sec[~is_neutrino])
    return wgt
