import numpy as np

import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

import matplotlib.cm as cm
from matplotlib.ticker import LogLocator
from scipy.ndimage.filters import gaussian_filter

fn = 'contours_data/'
tot_filename = fn + "chirpmass_tmerg_tot.dat"
tmerg_filename = fn + "tmerg_bin.dat"
chirpmass_filename = fn + "chirpmass_bin.dat"

with open(tot_filename) as tot_file:
    tot_data = [np.array(i.strip().split(), dtype=np.float) for i in tot_file.readlines()]
with open(tmerg_filename) as tmerg_file:
    tmerg_data = [i.strip() for i in tmerg_file.readlines() if i[0]!='#']
with open(chirpmass_filename) as chirpmass_file:
    chirpmass_data = [i.strip() for i in chirpmass_file.readlines() if i[0]!='#']

tot_data = np.array(tot_data, dtype=np.float)
tmerg_data = np.array(tmerg_data, dtype=np.float)
chirpmass_data = np.array(chirpmass_data, dtype=np.float)

# cleanup: 
# sigma= .5
# tot_data = gaussian_filter(tot_data, sigma)
minimum_value = 1e3
masked_tot_data = np.ma.masked_less_equal(tot_data, minimum_value)

plt.ylim((0, 40))

# tot_data = np.log(tot_data)
contour_levels=[1e4, 5e4, 1e5, 5e5]
contourf_levels=np.logspace(np.log10(minimum_value), np.log10(np.max(tot_data)))

loc = LogLocator(subs=(1.,2.,5.), numdecs=100, numticks=100)

ctf=plt.contourf(tmerg_data, chirpmass_data, masked_tot_data,
    contourf_levels,
    cmap=cm.Reds, locator=loc)
ct = plt.contour(tmerg_data, chirpmass_data, masked_tot_data, levels=contour_levels)

# subs=np.arange(1, 10, .1), numticks=100
def fmt(x):
    r = f'{x:.0e}'.split('e')
    if(int(r[0])==1):
        return(f'$10^{{{int(r[1])}}}$')
    else:
        return(r[0] + f'$\\times 10^{{{int(r[1])}}}$')

ct.levels = [fmt(i) for i in ct.levels]

cb = plt.colorbar(ctf, ticks=loc, label='Number of mergers')
plt.xlabel('$t _{\\text{merg}}$ [\\SI{}{Gyr}]')
plt.ylabel('$m _{\\text{chirp}} [M_{\\odot}]$')

plt.clabel(ct, ct.levels)
plt.show()
