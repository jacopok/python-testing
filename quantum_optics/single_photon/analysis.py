import numpy as np
import pandas as pd
import astropy.units as u

FILENAME = 'data/TimeTags.txt'
RESOLUTION = 80.955 * u.ps

def read_file(name):
    """Returns a pandas dataframe from the comma-separated file at name"""

    data = pd.read_csv(name,
                       sep=';',
                       header=None,
                       names=['ticks', 'channel'],
                       comment='#',
                       dtype=np.int)
    return data
