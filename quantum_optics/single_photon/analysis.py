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


def get_ticks(name=FILENAME):
    """Returns the arrays of times contained in the file at name"""

    data = read_file(name)

    ticks_t = data[data['channel'] == 2]['ticks'].values
    ticks_r = data[data['channel'] == 3]['ticks'].values
    ticks_g = data[data['channel'] == 4]['ticks'].values

    first_tick = min(ticks_t[0], ticks_r[0], ticks_g[0])

    return (ticks_t - first_tick, ticks_r - first_tick, ticks_g - first_tick)


def get_coincidences(t, g):
    for tick in g:
        i = np.searchsorted(t, tick)
        res = tick-t[i]
        if abs(res)<200:
            yield (t[i] - tick)

#plt.hist(list(get_coincidences(r, g)), bins=np.arange(0,200), alpha=.5, label='r')