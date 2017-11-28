"""
===============
Plot Honda Flux
===============

Demonstrate the flux API.
"""

# Author: Moritz Lotze <mlotze@km3net.de>
# License: BSD-3

import numpy as np
import matplotlib.pyplot as plt

from km3flux.flux import Honda2015
import km3pipe.style
km3pipe.style.use('moritz')

##############################################
# define energy + zenith range
n_points = 1000

zen = np.linspace(0, np.pi, n_points)
ene = np.logspace(0, 2, n_points)

##############################################
# look at numu flux (binned vs interpolated)

numu_flux = Honda2015('nu_mu')
print(
    numu_flux(ene, interpolate=True)[:10]
)
print(
    numu_flux(ene, interpolate=False)[:10]
)

##############################################
# Plot vs energy, for multiple flavors,
# interpolated by default

flavors = {'nu_mu', 'anu_mu', 'nu_e', 'anu_e'}
for flav in flavors:
    flux = Honda2015(flavor=flav)
    plt.plot(ene, flux(ene, interpolate=True), label=flav)

plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy / GeV')
plt.ylabel(r'Flux / (m$^2$ sec sr GeV)$^{-1}$')
plt.legend()
