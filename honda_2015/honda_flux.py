import h5py
import numpy as np


class HondaFlux(object):
    """
    Get Honda 2015 atmospheric neutrino fluxes.

    >>> from honda_flux import HondaFlux
    >>> flux = HondaFlux('file_with_fluxtables.h5')

    >>> zen = np.linspace(0, np.pi, 11)
    >>> ene = np.logspace(0, 2, 11)

    >>> flux('nu_e_bar', zen, ene)
    array([  6.68440000e+01,   1.83370000e+01,   4.96390000e+00,
         1.61780000e+00,   5.05350000e-01,   2.29920000e-01,
         2.34160000e-02,   2.99460000e-03,   3.77690000e-04,
         6.87310000e-05,   1.42550000e-05])

    """
    def __init__(self, filename):
        self.tables = {}
        with h5py.File(filename, 'r') as h5:
            self.energy_bins = h5['energy_binlims'][:]
            self.cos_zen_bins = h5['cos_zen_binlims'][:]
            for flavor in ('nu_e', 'nu_e_bar', 'nu_mu', 'nu_mu_bar'):
                self.tables[flavor] = h5[flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001


    def __call__(self, flavor, zenith, energy):
        fluxtable = self.tables[flavor]
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]
