import pandas as pd     # noqa

from honda_2015 import HondaFlux, HondaSarcevic


def honda_df(df, average=True):
    df['honda2015'] = 0
    hf = HondaFlux()
    for flav in {'nu_mu', 'anu_mu', 'nu_e', 'anu_e'}:       # noqa
        mask = df.flavor == flav
        if average:
            zen = None
        else:
            zen = df.zenith[mask]
        df.loc[mask, 'honda2015'] = hf.get(flav, df.energy[mask], zen)
    return df


def honda_sarcevic(df):
    df['honda_sarcevic'] = 0
    hf = HondaFlux()
    for flav in {'nu_mu', 'anu_mu', 'nu_e', 'anu_e'}:       # noqa
        mask = df.flavor == flav
        zen = df.zenith[mask]
        df.loc[mask, 'honda_sarcevic'] = hf.get(flav, df.energy[mask], zen)
    return df
