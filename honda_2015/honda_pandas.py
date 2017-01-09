import pandas as pd     # noqa

from honda_2015 import HondaFlux


def honda_df(df):
    df['honda2015'] = 0
    hf = HondaFlux()
    for flav in {'nu_mu', 'anu_mu', 'nu_e', 'anu_e'}:       # noqa
        mask = df.flavor == flav
        df.loc[mask, 'honda2015'] = hf.binned(flav, df.zenith[mask], df.energy[mask])
    return df
