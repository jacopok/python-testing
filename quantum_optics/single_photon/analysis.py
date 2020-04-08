import numpy as np
import pandas as pd
import astropy.units as u
import matplotlib.pyplot as plt

FILENAME = 'data/TimeTags.txt'
RESOLUTION = 80.955 * u.ps
THR = (-20, 100)


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


def get_timediffs(a, g, thr=THR):
    for tick in g:
        i = np.searchsorted(a, tick, side='left')
        try:
            if abs(tick - a[i - 1]) < abs(tick - a[i]):
                res = a[i - 1] - tick
            else:
                res = a[i] - tick
        except IndexError:
            res = a[i] - tick

        if thr[0] <= res < thr[1]:
            yield res


#plt.hist(list(get_coincidences(r, g)), bins=np.arange(0,200), alpha=.5, label='r')


def get_all_timediffs(t, r, g):
    dtt = get_timediffs(t, g)
    dtr = get_timediffs(r, g)

    bins_t = np.arange(*THR)
    bins_r = np.copy(bins_t)
    vals_t = np.zeros_like(bins_t)
    vals_r = np.zeros_like(bins_r)

    for x in dtt:
        vals_t[bins_t == x] += 1
    for x in dtr:
        vals_r[bins_r == x] += 1

    return ((bins_t, vals_t), (bins_r, vals_r))


def shapes(arr, n):
    return [np.shape(arr[arr % n == i])[0] for i in range(n)]


def get_odd_even_ratios(arr, num=50_000):
    dt = []
    for i in range(len(arr) // num):
        c = np.array(shapes(arr[num * i:num * (i + 1)], 2))
        dt.append(c[1] / c[0])
    return (dt)


def plot_oer(t, r, g):
    dt = get_odd_even_ratios(t)
    dr = get_odd_even_ratios(r)
    dg = get_odd_even_ratios(g)

    plt.plot(np.linspace(0, 1, len(dr)), dr, label='refl')
    plt.plot(np.linspace(0, 1, len(dg)), dg, label='gate')
    plt.plot(np.linspace(0, 1, len(dt)), dt, label='tr')
    plt.legend()
    plt.title('odd to even ratios')
    plt.show()


if __name__ == "__main__":
    ticks = get_ticks()

    T, R = get_all_timediffs(*ticks)
    
    