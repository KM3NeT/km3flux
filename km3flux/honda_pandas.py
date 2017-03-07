import pandas as pd     # noqa
import numpy as np

from km3flux import HondaFlux, HondaSarcevic


def honda_df(df, nevts=None, average=True, flavors=None):
    if flavors is None:
        flavors = {'nu_mu', 'anu_mu', 'nu_e', 'anu_e'}      # noqa
    if nevts is None:
        nevts = len(df)
    out = np.zeros(nevts)
    hf = HondaFlux()
    for flav in flavors:
        mask = np.array(df.flavor == flav, dtype=bool)
        if average:
            zen = None
        else:
            zen = df.zenith[mask]
        buf = hf.get(flav, df.energy[mask], zen)
        out[mask] = buf
    return out
