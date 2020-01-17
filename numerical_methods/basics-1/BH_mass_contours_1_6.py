import numpy as np
import pandas as pd
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
from matplotlib.colors import LogNorm
import matplotlib.cm as cm
from matplotlib.ticker import LogLocator

data = pd.read_csv("contours_data/time_BHillustris1_30.dat", sep=" ", comment = "#", header=None, names = ["identifier", "host total stellar mass host", "formation redshift", "metallicity star", "metallicity pop. synth", "identifier binary", "mass BH1", "mass BH2", "delay time", "merger time (look back)"])

# larger BH
BH1 = list(data["mass BH1"])
# smaller BH
BH2 = list(data["mass BH2"])
n = len(data)

for i in range(n):
    if (BH1[i] < BH2[i]):
        BH1[i], BH2[i] = BH2[i], BH1[i]

# quick solution:
# plt.hist2d(BH1, BH2, bins=100, norm=LogNorm())
# plt.colorbar()
# plt.show()

N= 50
m1 = np.linspace(min(BH1), max(BH1), num=N)
dm1 = m1[1] - m1[0]
m2 = np.linspace(min(BH2), max(BH2), num=N)
dm2 = m2[1] - m2[0]
z = np.ones((N, N))

for bh1, bh2 in zip(np.array(BH1) - min(BH1), np.array(BH2)- min(BH2)):
#     i = np.searchsorted(m1, bh1, side='left')
#     j = np.searchsorted(m2, bh2, side='left')
    i = int(bh1/dm1)
    j = int(bh2/dm2)
    z[j, i] += 1

levels=np.logspace(0,5, num=6)
c = plt.contourf(m1, m2, z,
        cmap=cm.viridis,
        levels=levels,
        locator=LogLocator())
plt.colorbar(c, label='Number of mergers + 1')

plt.ylabel('$m_{2} [M_{\\odot}]$')
plt.xlabel('$m_{1} [M_{\\odot}]$')

plt.show()
