#!/usr/bin/env python

from __future__ import division, absolute_import, print_function
import six

import h5py
import numpy as np
import pandas as pd


# define coszenith bins
nbins = 20
cos_zen_binlims = np.linspace(-1.0, 1.0, nbins + 1)
coszen_binsize = 2.0/nbins
coszen_low = cos_zen_binlims[:-1]
coszen_hi = cos_zen_binlims[1:]
cos_zen = coszen_low + 0.5 * coszen_binsize
bins = np.column_stack((coszen_low, coszen_hi))

prefix = '/home/mlotze/dev/honda_2015'
dfs = []
for lo, hi in bins:
    fname = prefix + '/' + 'cos_%s_%s.csv' % (str(lo), str(hi))
    df = pd.read_table(fname, header=1, delim_whitespace=True)
    n_evts = len(df)
    df['cos_zen'] = lo + 0.5 * coszen_binsize
    dfs.append(df)

df = pd.concat(dfs)
energy = np.unique(df['Enu'])
df = df.set_index(['cos_zen', 'Enu'])

# (Energy, cos) matrices
numu = df['NuMu'].unstack().values
numubar = df['NuMubar'].unstack().values
nue = df['NuE'].unstack().values
nuebar = df['NuEbar'].unstack().values

h5 = h5py.File('honda2015_frejus_solarmin.h5')
h5.create_dataset('energy', data=energy, compression="gzip", compression_opts=5)
h5.create_dataset('cos_zen', data=cos_zen, compression="gzip", compression_opts=5)
h5.create_dataset('cos_zen_binlims', data=cos_zen_binlims, compression="gzip", compression_opts=5)
h5.create_dataset('nu_mu', data=numu, compression="gzip", compression_opts=5)
h5.create_dataset('nu_mu_bar', data=numubar, compression="gzip", compression_opts=5)
h5.create_dataset('nu_e', data=nue, compression="gzip", compression_opts=5)
h5.create_dataset('nu_e_bar', data=nuebar, compression="gzip", compression_opts=5)
h5.close()
