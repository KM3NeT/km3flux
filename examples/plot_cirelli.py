"""
======================
Plot DarkMatter Fluxes
======================

Plot some Fluxes from WimpWimp -> foo in the GC.
"""

# Author: Moritz Lotze <mlotze@km3net.de>
# License: BSD-3

import matplotlib.pyplot as plt
import numpy as np

from km3flux.flux import DarkMatterFlux

import km3pipe.style.moritz     # noqa

#############################################################################
# generate energies, logarithmically spaced, for which to compute fluxes
energy = np.geomspace(10, 1000, 201)
print(energy[:10])

#############################################################################
# show available tables

print('flavors:  ', DarkMatterFlux.flavors)
print('channels: ', DarkMatterFlux.channels)
print('masses:   ', DarkMatterFlux.masses)

#############################################################################
# show a binned flux

dmflux = DarkMatterFlux(flavor='nu_mu', channel='w', mass=3000)
print(
    dmflux(energy[:10])
)
plt.plot(energy, dmflux(energy))
plt.yscale('log')
plt.xscale('log')

#############################################################################
# show the same, but as interpolated flux

plt.plot(energy, dmflux(energy, interpolate=True))
plt.yscale('log')
plt.xscale('log')
