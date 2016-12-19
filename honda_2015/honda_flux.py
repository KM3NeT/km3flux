import os.path

import h5py
import numpy as np

import honda_2015

DATADIR = os.path.dirname(honda_2015.__file__)
FLUXFILE = DATADIR + '/data/honda2015_frejus_solarmin.h5'


class HondaFlux(object):
    """
    Get Honda 2015 atmospheric neutrino fluxes.

    >>> from honda_2015 import HondaFlux
    >>> flux = HondaFlux()

    >>> zen = np.linspace(0, np.pi, 11)
    >>> ene = np.logspace(0, 2, 11)

    >>> flux('nu_e_bar', zen, ene)
    array([  6.68440000e+01,   1.83370000e+01,   4.96390000e+00,
         1.61780000e+00,   5.05350000e-01,   2.29920000e-01,
         2.34160000e-02,   2.99460000e-03,   3.77690000e-04,
         6.87310000e-05,   1.42550000e-05])

    """
    def __init__(self, filename=None):
        self.tables = {}
        if filename is None:
            filename = FLUXFILE
        with h5py.File(filename, 'r') as h5:
            self.energy_bins = h5['energy_binlims'][:]
            self.cos_zen_bins = h5['cos_zen_binlims'][:]
            for flavor in ('nu_e', 'anu_e', 'nu_mu', 'anu_mu'):
                self.tables[flavor] = h5[flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001

    def binned(self, flavor, zenith, energy):
        fluxtable = self.tables[flavor]
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]

    def from_dataframe(self, df):
        flux = np.ones_like(df['zenith'], dtype=float)
        for flavor in df['flavor'].unique():
            where = df['flavor'] == flavor
            flux[where] = self(flavor, df['zenith'][where],
                               df['energy'][where])
        return flux
