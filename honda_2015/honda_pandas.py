import pandas as pd     # noqa
import numpy as np

from honda_2015 import HondaFlux, HondaSarcevic


def honda_df(df, average=True):
    out = np.zeros_like(df.flavor)
    hf = HondaFlux()
    for flav in {'nu_mu', 'anu_mu', 'nu_e', 'anu_e'}:       # noqa
        mask = np.array(df.flavor == flav, dtype=bool)
        if average:
            zen = None
        else:
            zen = df.zenith[mask]
        buf = hf.get(flav, df.energy[mask], zen)
        out[mask] = buf
    return out


def honda_sarcevic_df(df):
    out = np.zeros_like(df.flavor)
    hf = HondaFlux()
    for flav in {'nu_mu', 'anu_mu', 'nu_e', 'anu_e'}:       # noqa
        mask = df.flavor == flav
        zen = df.zenith[mask]
        buf = hf.get(flav, df.energy[mask], zen)
        out[mask] = buf
    return out
