import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from astropy import units as u
from tqdm import tqdm
import pandas as pd
from collections import defaultdict
from multiprocessing import Pool
from functools import partial
import numba
from matplotlib import cm
from scipy.special import factorial
from scipy.stats import poisson

THERMAL_PATH = 'data/24, Jan, 2020 - Thermal/'
COHERENT_PATH = 'data/24, Jan, 2020 - Coherent/'
RESOLUTION = 81 * u.picosecond
MAX_TICKS = int(1e4)

THERMAL_NAMES = [THERMAL_PATH + 'Part_' + str(i) + '.txt' for i in range(10)]
COHERENT_NAMES = [COHERENT_PATH + 'Part_' + str(i) + '.txt' for i in range(10)]

def read_file(name):
    data = pd.read_csv(name, sep=',', header=None, names=['ticks', 'channel'], dtype=np.int)
    return (data)

def get_ticks(name):
    data = read_file(name)
    ticks = data['ticks'].values
    return(ticks)

def get_ticks_names(names):
    all_ticks=[]
    for name in names:
        all_ticks.append(get_ticks(name))
    return ([x - x[0] for x in all_ticks])

thermal_ticks = get_ticks_names(THERMAL_NAMES)
coherent_ticks = get_ticks_names(COHERENT_NAMES)

def sum_arrays(arrays):
    max_len = max([len(a) for a in arrays])
    result = np.zeros(max_len)
    for a in arrays:
        result[:len(a)] += a
    return(result)

@numba.jit(nopython=True)
def base_get_n_in_window(ticks, adim_window):
    tmax = ticks[-1]
    N = int(tmax / adim_window)
    nums = np.zeros(N)

    indices = np.searchsorted(ticks, np.arange(N+1)*adim_window)
    nums = np.ediff1d(indices)
    n = np.zeros(max(nums)+1)
    for num in nums:
        n[num] += 1
    return (n)


def get_n_in_window_from_ticks(ticks, window, resolution = RESOLUTION):
        """
    divide the ticks (which must start at zero!)
    into "window" long intervals
    and returns an array of integers, 
    each entry of which is the number of photons detected
    in that window
    """

    len_ticks = len(ticks)
    # print(len_ticks)
    additional_factor_small_windows = int(max( (np.sqrt(1*u.us / window)).to(u.dimensionless_unscaled).value, 1))
    # total_ticks = int(MAX_TICKS * additional_factor_small_windows)
    total_ticks = MAX_TICKS

    number_subdivisions = len_ticks // total_ticks
    adim_window = (window/resolution).to(u.dimensionless_unscaled).value

    all_nums = []
    for n in range(number_subdivisions):
        current_ticks = ticks[n * total_ticks:(n + 1) * total_ticks]
        nums = base_get_n_in_window(current_ticks - current_ticks[0], adim_window)
        all_nums.append(nums)

    return(sum_arrays(all_nums))

def get_n_in_window_from_all_ticks(all_ticks, window):

    print(f'Analyzing window size {window}')
    # all_ns = []
    # for ticks in all_ticks:
    #     ns = get_n_in_window_from_ticks(ticks, window)
    #     all_ns.append(ns)
    pool = Pool(6)
    func = partial(get_n_in_window_from_ticks, window=window)
    all_ns = pool.map(func, all_ticks)
    pool.close() # no more tasks
    pool.join()    # wrap up current tasks

    return (sum_arrays(all_ns))
    
def get_photon_counts(thermal_ticks, coherent_ticks, window):
    photon_counts = {}
    photon_counts['thermal'] = get_n_in_window_from_all_ticks(thermal_ticks, window)
    photon_counts['coherent'] = get_n_in_window_from_all_ticks(coherent_ticks, window)
    return(photon_counts)

def thermal(n, nbar):
    return ((nbar/(1+nbar)) ** n / (1 + nbar))
    
def coherent(n, nbar):
    return(poisson.pmf(n, nbar))
    # return (np.exp(-nbar) * nbar ** n / factorial(n))

theoretical_distributions = {    
    'thermal': thermal,
    'coherent': coherent,
}

def moment(b, v, n):
    m = np.average(b, weights=v)
    if (n == 1):
        return(m)
    return (np.sum((b - m)**n * v / np.sum(v)))

def analyze(dist, ns, nbar):
    bins = dist(ns, nbar)
    th_desc = {}
    th_desc['variance'] = moment(ns, bins, 2)
    th_desc['skewness'] = moment(ns, bins, 3) / moment(ns, bins, 2)**(3/2)
    th_desc['kurtosis'] = moment(ns, bins, 4) / moment(ns, bins, 2)**(4/2)
    return(th_desc)

def describe(distribution, dist_type):
    description = {}
    nums = range(len(distribution))
    description['mode'] = np.argmax(distribution)
    description['mean'] = moment(nums, distribution, 1)

    th_desc = analyze(theoretical_distributions[dist_type], nums, description['mean'])

    description['variance'] = moment(nums, distribution, 2)
    description['theoretical variance'] = th_desc['variance']
    description['skewness'] = moment(nums, distribution, 3) / moment(nums, distribution, 2)**(3/2)
    description['theoretical skewness'] = th_desc['skewness']
    description['kurtosis'] = moment(nums, distribution, 4) / moment(nums, distribution, 2)**(4/2)
    description['theoretical kurtosis'] = th_desc['kurtosis']

    return (description)

def plot_descriptions(windows, descriptions):
    fig, axs = plt.subplots(1, 2)

    for i, (name, description) in enumerate(descriptions.items()):
        colors = ['purple', 'lime', 'red', 'red', 'blue', 'blue', 'green', 'green']
        for (characteristic, color) in zip(description[0], colors):
            ls = '--' if 'theoretical' in characteristic else '-'

            axs[i].loglog(windows, [y[characteristic] for y in description], label=characteristic, ls=ls, c=color)

        axs[i].set_title(name)
        axs[i].legend()
        axs[i].set_xlabel(f'window size [{windows.unit}]')
    plt.tight_layout()
    plt.savefig('descriptions.pdf', format = 'pdf')
    plt.show(block=False)

def get_descriptions(windows):
    descriptions = defaultdict(list)

    for window in windows:
        photon_counts = get_photon_counts(thermal_ticks, coherent_ticks, window)

        for name, distribution in photon_counts.items():
            description = describe(distribution, name)
            descriptions[name].append(description)

    return(descriptions)

def get_rate(descriptions, windows, unit = u.kHz):
    rates = {}
    for name, description in descriptions.items():
        distribution_rates = []
        for w, d in zip(windows.value, description):
            mean = d['mean']
            rate = mean / w
            distribution_rates.append(rate)
        rates[name] = np.average(distribution_rates) / windows.unit
        if unit is not None:
            rates[name] = rates[name].to(unit)
    rates['ratio'] = (rates['thermal'] / rates['coherent']).to(u.percent)

    return(rates)

if __name__ == '__main__':
    windows = np.logspace(-2, 3.5, num=40) * u.us

    # photon_counts = get_photon_counts(thermal_ticks, coherent_ticks, 10*u.us)
    
    # for name, distribution in photon_counts.items():
    #     plt.bar(range(len(distribution)), distribution, label=name, alpha=.5)     
    
    # plt.show()
