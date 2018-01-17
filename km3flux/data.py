from __future__ import division, absolute_import, print_function

import os.path

import h5py

import km3flux


DATADIR = os.path.dirname(km3flux.__file__) + '/data'
HONDAFILE = DATADIR + '/honda2015_frejus_solarmin.h5'
# DM_GC_FILE = DATADIR + '/gc_spectra.h5'
DM_GC_FILE = DATADIR + '/cirelli_gc.h5'
DM_GC_MASSES = {'100000', '260', '100', '5000', '360', '200', '10', '1000',
                '750', '30000', '2000', '50', '10000', '180', '500', '150',
                '3000', '25', '90', '1500'}
DM_GC_FLAVORS = {'anu_mu', 'nu_mu'}
DM_GC_CHANNELS = {'b', 'mu', 'tau', 'w'}

DM_SUN_FILE = DATADIR + '/sun_spectra.h5'
DM_SUN_MASSES = {'1000', '100', '10', '1500', '176', '150', '2000', '200',
                 '250', '25', '3000', '350', '5000', '500', '50', '750'}
DM_SUN_FLAVORS = {'anu_mu', 'nu_mu'}
DM_SUN_CHANNELS = {'11', '8', '5'}

DM_SUN_CHAN_TRANS = {'8': 'w', '11': 'tau', '5': 'b'}
DM_SUN_CHAN_TRANS_INV = {v: k for k, v in DM_SUN_CHAN_TRANS.items()}

WIMPSIM_ANNIHILATION_CHANNELS = {
    1: 'd d-bar',
    2: 'u u-bar',
    3: 's s-bar',
    4: 'c c-bar',
    5: 'b b-bar',
    6: 't t-bar',
    7: 'glue glue',
    8: 'W+ W-',
    9: 'Z0 Z0',
    10: 'mu- mu+',
    11: 'tau- tau+',
    12: 'nu_e nu_e-bar',
    13: 'nu_mu nu_mu-bar',
    14: 'nu_tau nu_tau-bar',
}


def dm_gc_spectrum(flavor='nu_mu', channel='w', mass='100', full_lims=False):
    """Dark Matter spectra by M. Cirelli."""
    mass = str(mass)
    if mass not in DM_GC_MASSES:
        raise KeyError("Mass '{}' not available.".format(mass))
    if flavor not in DM_GC_FLAVORS:
        raise KeyError("Flavor '{}' not available.".format(flavor))
    if channel not in DM_GC_CHANNELS:
        raise KeyError("Channel '{}' not available.".format(channel))

    fname = DM_GC_FILE
    with h5py.File(fname, 'r') as h5:
        gr = h5[flavor][channel][mass]
        counts = gr['entries'][:]
        bins = gr['binlims'][:]
    if not full_lims:
        bins = bins[:-1]
    return counts, bins


def dm_sun_spectrum(flavor='nu_mu', channel='w', mass='100', full_lims=False):
    """Dark Matter spectra by M. Cirelli."""
    chan_num = DM_SUN_CHAN_TRANS_INV[channel]
    mass = str(mass)
    if mass not in DM_SUN_MASSES:
        raise KeyError("Mass '{}' not available.".format(mass))
    if flavor not in DM_SUN_FLAVORS:
        raise KeyError("Flavor '{}' not available.".format(flavor))
    if chan_num not in DM_SUN_CHANNELS:
        raise KeyError("Channel '{}' not available.".format(channel))

    fname = DM_SUN_FILE
    with h5py.File(fname, 'r') as h5:
        gr = h5[flavor][chan_num][mass]
        counts = gr['entries'][:]
        bins = gr['binlims'][:]
    if not full_lims:
        bins = bins[:-1]
    return counts, bins
