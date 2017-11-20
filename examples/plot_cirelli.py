"""
===================
Plot Cirelli Fluxes
===================

Plot some Fluxes from WimpWimp -> foo in the GC.
"""

# Author: Moritz Lotze <mlotze@km3net.de>
# License: BSD-3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from km3flux.flux import dmflux, DarkMatterFlux, all_dmfluxes
from km3flux.aeff import effective_area

import km3pipe.style.moritz

###############################################################
# plot flux vs energy

ene = np.logspace(0, 2, 2001)
flux = dmflux(ene, flavor='anu_mu', channel='w', mass=5000)
plt.loglog(ene, flux)

###############################################################
# integrate a flux

flux_callable = DarkMatterFlux(flavor='nu_mu', channel='w', mass=3000)
flux_callable.integrate()

###############################################################
# get the flux collection

flux_coll = all_dmfluxes()
integrated_fluxes = {}
for fluxname, flux in flux_coll.items():
    try:
        integrated_fluxes[fluxname] = flux.integrate()
    except (ValueError, IndexError):
        continue

integrated_fluxes = pd.DataFrame(integrated_fluxes).T
integrated_fluxes.rename(columns={0: 'flux'}, inplace=True)

#integrated_fluxes.sort_values(by='flux', inplace=True)
integrated_fluxes.sort_index(level=2, inplace=True)

###############################################################
# plot them

#eff_areas.groupby(level=1).plot(rot=45, logy=True, sharey=True, subplots=True)
fig, axes = plt.subplots(ncols=4, figsize=(16, 3), sharex=False, sharey=True)
for i, (tag, group) in enumerate(integrated_fluxes.groupby(level=1)):
    group.plot(ax=axes[i], rot=45, logy=True)

###############################################################
# plot them differently

integrated_fluxes.sort_values(by='flux').plot(rot=45)
plt.yscale('log')


###############################################################
# get effective area

effective_area(flux_callable, w2_over_ngen=1e-5,
               solid_angle=4 * np.pi,
               energy=np.geomspace(1, 100, 25)
               )
