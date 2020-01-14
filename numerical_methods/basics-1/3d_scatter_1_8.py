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
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv("contours_data/time_BHillustris1_30.dat", sep=" ", comment="#", header=None, names=["identifier", "host total stellar mass host", "formation redshift", "metallicity star", "metallicity pop. synth", "identifier binary", "mass BH1", "mass BH2", "delay time", "merger time (look back)"])

# n = len(data)
n = int(5e3)
Zs = list(data['metallicity star'])[:n]
BH1 = list(data["mass BH1"])[:n]
BH2 = list(data["mass BH2"])[:n]

for i in range(n):
    if (BH1[i] < BH2[i]):
        BH1[i], BH2[i] = BH2[i], BH1[i]

bh1 = np.array(BH1)
bh2 = np.array(BH2)
m_chirp = (bh1 * bh2)**(3./5.) * (bh1 + bh2)**(-1./5.)

ax = plt.subplot(111, projection='3d')

c = ax.scatter(bh1, bh2, Zs, c=m_chirp)
plt.colorbar(c, label='Chirp mass: $(m_1 m_2)^{3/5} (m_1 + m_2)^{-1/5}$ $[M_\\odot^{2/5}]$')
ax.set_xlabel('$m_1 [M_\\odot]$')
ax.set_ylabel('$m_2 [M_\\odot]$')
ax.set_zlabel('$Z$')
plt.tight_layout()
plt.show()