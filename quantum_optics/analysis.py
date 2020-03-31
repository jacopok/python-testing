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
  number_subdivisions = len_ticks //  MAX_TICKS 
  adim_window = (window/resolution).to(u.dimensionless_unscaled).value

  if number_subdivisions < 2:
    tmax = ticks[-1]
    N = int(tmax / adim_window)
    nums = np.zeros(N, dtype=int)

    indices = np.searchsorted(ticks, np.arange(N+1)*adim_window)
    nums = np.ediff1d(indices)
    n = np.zeros(max(nums)+1)
    for num in nums:
      n[num]+=1
    return (n)
  
  else:
    all_nums = []
    max_n = 0
    for n in tqdm(range(number_subdivisions)):
      current_ticks = ticks[n * MAX_TICKS:(n + 1) * MAX_TICKS]
      nums = get_n_in_window_from_ticks(current_ticks - current_ticks[0], window, resolution)
      max_n = max(max_n, max(nums))
      all_nums.append(nums)

    return(sum_arrays(all_nums))

def get_n_in_window_from_all_ticks(all_ticks, window):

  print(f'Analyzing window size {window}')
  pool = Pool(6)
  # all_ns = []
  # for ticks in all_ticks:
  #   ns = get_n_in_window_from_ticks(ticks, window)
  #   all_ns.append(ns)
  func = partial(get_n_in_window_from_ticks, window=window)
  all_ns = pool.map(func, all_ticks)

  return (sum_arrays(all_ns))
  
def get_photon_counts(thermal_ticks, coherent_ticks, window):
  photon_counts = {}
  photon_counts['thermal'] = get_n_in_window_from_all_ticks(thermal_ticks, window)
  photon_counts['coherent'] = get_n_in_window_from_all_ticks(coherent_ticks, window)
  return(photon_counts)

def moment(b, v, n):
  m = np.average(b, weights=v)
  if (n == 1):
    return(m)
  return (np.sum((b - m)**n * v / np.sum(v)))

def describe(distribution):
  description = {}
  nums = range(len(distribution))
  description['mean'] = moment(nums, distribution, 1)
  description['variance'] = moment(nums, distribution, 2)
  description['skewness'] = moment(nums, distribution, 3)
  description['kurtosis'] = moment(nums, distribution, 4)
  description['mode'] = np.argmax(distribution)
  return (description)

def plot_descriptions(descriptions):
  fix, axs = plt.subplots(1, 2)

  for i, (name, description) in enumerate(descriptions.items()):
    for characteristic in description[0]:
      axs[i].semilogx(windows, [y[characteristic] for y in description], label=characteristic)
    axs[i].set_title(name)
    axs[i].legend()
    axs[i].set_xlabel(f'window size [{windows.unit}]')

  plt.show()

if __name__ == '__main__':
  windows = np.logspace(-2, 2, num=30) * u.us
  # windows = [10] * u.us
  descriptions = defaultdict(list)

  for window in windows:
    photon_counts = get_photon_counts(thermal_ticks, coherent_ticks, window)

    for name, distribution in photon_counts.items():
      description = describe(distribution)
      descriptions[name].append(description)

  photon_counts = get_photon_counts(thermal_ticks, coherent_ticks, 10*u.us)
  
  for name, distribution in photon_counts.items():
    plt.bar(range(len(distribution)), distribution, label=name, alpha=.5)   
  
  plt.show()
