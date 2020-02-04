import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from astropy import units as u
from tqdm import tqdm

import pandas as pd

from collections import defaultdict

THERMAL_PATH = 'data/24, Jan, 2020 - Thermal/'
COHERENT_PATH = 'data/24, Jan, 2020 - Coherent/'
RESOLUTION = 81 * u.picosecond

THERMAL_NAMES = [THERMAL_PATH + 'Part_' + str(i) + '.txt' for i in range(10)]
COHERENT_NAMES = [COHERENT_PATH + 'Part_' + str(i) + '.txt' for i in range(10)]

def read_file(name):
  data = pd.read_csv(name, sep=',', header=None, names=['ticks', 'channel'],dtype=np.int)
  return (data)

def get_ticks(name):
  data = read_file(name)
  ticks = data['ticks'].values
  return(ticks)

def get_all_timediffs(names, resolution = RESOLUTION):
  diffs = []
  for name in names:
    t = get_ticks(name)
    dt = np.ediff1d(t)
    diffs.append(dt)

  return (u.Quantity(np.hstack(diffs), resolution))

def get_n_window(name, window, resolution = RESOLUTION):
  """
  divide times found at location "name"
  into "window" long intervals
  and returns an array of integers, 
  each entry of which is the number of photons detected
  in that window
  """

  t = get_ticks(name) * resolution
  tmax = t[-1]
  N = int((tmax / window).to(''))
  nums = np.zeros(N, dtype=int)
  
  adim_window = window.to(t.unit).value
  adim_t = t.value

  n = 0
  i = 0
  
  while n < N:
    while adim_t[i] < (n + 1) * adim_window:
      nums[n] += 1
      i += 1
    n += 1
  return (nums)

def get_n_from_names(names, window):
  all_ns = []
  for name in tqdm(names):
    ns = get_n_window(name, window)
    all_ns.append(ns)

  max_ns = max([len(x) for x in all_ns])
  full_ns = np.zeros((len(all_ns), max_ns))
  for i, ns in enumerate(all_ns):
    full_ns[i,:len(ns)] = ns

  return(full_ns.flatten())

def moment(b, v, n):
  m = np.average(b, weights=v)
  if (n == 1):
    return(m)
  return (np.sum((b - m)**n * v))

def analyze(b, v):
  moments = {'mean': 1, 'variance': 2, 'skewness': 3, 'kurtosis': 4}
  for m, num in moments.items():
    print(m, ' = ', f'{moment(v, b, num):.3f}')

if __name__ == '__main__':
  # timediffs = {}
  # timediffs['coherent'] = get_all_timediffs(COHERENT_NAMES)
  # timediffs['thermal'] = get_all_timediffs(THERMAL_NAMES)

  # bins = {}
  # values = {}

  # time_unit = u.us
  # max_time = 50

  # for x in timediffs:
  #   times = timediffs[x].to(time_unit).value
  #   mask = times < max_time
  #   values[x], bins[x], _ = plt.hist(times[mask], label=x, bins=200, alpha=.6, density=True)
  # plt.xlabel(f'Time differences [{str(time_unit)}]')
  # plt.xlim(0, max_time)
  # plt.legend()
  # plt.show()

  # for x in timediffs:
  #   print(x)
  #   b = bins[x]
  #   analyze((b[1:]+b[:-1])/2., values[x])

  # for i in [10, 50, 100, 250, 1000]: 
  #   n = get_n_from_names(THERMAL_NAMES, i*u.us) 
  #   plt.plot(np.abs(np.fft.rfft(n)), alpha=.5, label=str(i) +' microseconds window') 
