#!/usr/bin/env python

from __future__ import division, absolute_import, print_function
import six

import h5py
import numpy as np
import pandas as pd


# define zenith bins
nbins = 20
zen = np.linspace(-1.0, 1.0, nbins + 1)
zen_binsize = 2.0/nbins
zen_low = zen[:-1]
zen_hi = zen[1:]
bins = np.column_stack((zen_low, zen_hi))

dfs = []
for lo, hi in bins:
    fname = 'cos_%s_%s.csv' % (str(lo), str(hi))
    df = pd.read_table(fname, header=1, delim_whitespace=True)
    n_evts = len(df)
    #df['cos_low'] = np.ones(n_evts, float) * lo
    #df['cos_high'] = np.ones(n_evts, float) * hi
    df['cos'] = lo + 0.5 * zen_binsize
    dfs.append(df)

df = pd.concat(dfs)


#rec = df.to_records()
#h5 = h5py.File('honda2015_frejus_solarmin.h5')
#h5.create_dataset('raw_parsed', data=rec)
