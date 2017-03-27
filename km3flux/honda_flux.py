"""Honda 2015/Honda Sarcevic Fluxes, in  (m^2 sec sr GeV)^-1"""

import os.path

import h5py
import numpy as np

import km3flux

DATADIR = os.path.dirname(km3flux.__file__)
FLUXFILE = DATADIR + '/data/honda2015_frejus_solarmin.h5'


class Honda2015(object):
    """
    Get Honda 2015 atmospheric neutrino fluxes.

    >>> from km3flux import Honda2015
    >>> flux = Honda2015()

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
        self.avtables = {}
        if filename is None:
            filename = FLUXFILE
        with h5py.File(filename, 'r') as h5:
            self.energy_bins = h5['energy_binlims'][:]
            self.cos_zen_bins = h5['cos_zen_binlims'][:]
            for flavor in ('nu_e', 'anu_e', 'nu_mu', 'anu_mu'):
                self.tables[flavor] = h5[flavor][:]
                self.avtables[flavor] = h5['averaged/' + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001

        # optionally, this can be fixed to make it a single-arg callable
        self._flavor = None

    @property
    def flavor(self):
        return self._flavor

    @flavor.setter
    def flavor(self, flav):
        self._flavor = flav

    def __call__(self, energy):
        # for use e.g. with `scipy.integrate`
        if self.flavor is None:
            raise ValueError("No flavor set! aborting...")
        return self.get(self.flavor, energy)

    def get(self, flavor, energy, zenith=None):
        if zenith is None:
            return self._averaged(flavor, energy)
        else:
            return self._with_zenith(flavor, energy=energy, zenith=zenith)

    def _averaged(self, flavor, energy):
        fluxtable = self.avtables[flavor]
        ene_bin = np.digitize(energy, self.energy_bins)
        ene_bin = ene_bin - 1
        return fluxtable[ene_bin]

    def _with_zenith(self, flavor, energy, zenith):
        fluxtable = self.tables[flavor]
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]


class HondaSarcevic(object):
    """
    Get Honda + Sarcevic atmospheric neutrino fluxes.
    """
    def __init__(self, filename=None):
        self.tables = {}
        self.avtables = {}
        if filename is None:
            filename = FLUXFILE
        with h5py.File(filename, 'r') as h5:
            self.energy_bins = h5['energy_binlims'][:]
            self.cos_zen_bins = h5['cos_zen_binlims'][:]
            for flavor in ('nu_e', 'anu_e', 'nu_mu', 'anu_mu'):
                self.tables[flavor] = h5['honda_sarcevic/' + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001

        # optionally, this can be fixed to make it a single-arg callable
        self._flavor = None

    @property
    def flavor(self):
        return self._flavor

    @flavor.setter
    def flavor(self, flav):
        self._flavor = flav

    def __call__(self, energy):
        # for use e.g. with `scipy.integrate`
        if self.flavor is None:
            raise ValueError("No flavor set! aborting...")
        return self.get(self.flavor, energy)

    def get(self, flavor, energy, zenith):
        return self._with_zenith(flavor, energy=energy, zenith=zenith)

    def _with_zenith(self, flavor, energy, zenith):
        fluxtable = self.tables[flavor]
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]
