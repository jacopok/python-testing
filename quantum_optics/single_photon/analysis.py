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


def get_ticks(name):
    """Returns the arrays of times contained in the file at name"""

    data = read_file(name)
    
    ticks_t = data[data['channel'] == 2]['ticks'].values
    ticks_r = data[data['channel'] == 3]['ticks'].values
    ticks_g = data[data['channel'] == 4]['ticks'].values
    return (ticks_t, ticks_r, ticks_g)