import h5py
import numpy as np


class HondaFlux(object):
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
