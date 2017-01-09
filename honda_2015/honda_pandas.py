import pandas as pd
import numpy as np

import honda_2015


def honda_df(flavor, df):
    hf = HondaFlux()
    return hf.binned(flavor, df['zenith'], df['energy'])
