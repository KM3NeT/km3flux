"""
===================
Isotropic Fluxes
===================

Demonstrate isotropic neutrino fluxes
"""

# Author: Tamas Gal <tgal@km3net.de>
# License: BSD-3

import matplotlib
import seaborn as sns
import numpy as np
import km3flux

import scipy.interpolate

honda = km3flux.flux.Honda()

f = honda.flux(2014, "Frejus", solar="min", averaged="all")

fig, ax = matplotlib.pyplot.subplots()

energies = np.logspace(-1, 4, 200)

colors = sns.color_palette("tab10")

for c, nu in zip(colors, ["numu", "nue", "anumu", "anue"]):
    ax.plot(f._data.energy, f._data[nu], c=c, label=nu, marker=",", ls="none")
    ax.plot(energies, f[nu](energies), c=c, label=nu + " interp.")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Neutrino energy / GeV")
ax.set_ylabel("Flux / (m$^2$ s sr GeV)$^{-1}$")
ax.legend()
