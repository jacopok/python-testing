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


data = pd.read_csv("contours_data/time_BHillustris1_30.dat", sep=" ", comment = "#", header=None, names = ["identifier", "host total stellar mass host", "formation redshift", "metallicity star", "metallicity pop. synth", "identifier binary", "mass BH1", "mass BH2", "delay time", "merger time (look back)"])

# larger BH
BH1 = list(data["mass BH1"])
# smaller BH
BH2 = list(data["mass BH2"])
n = len(data)

for i in range(n):
    if (BH1[i] < BH2[i]):
        BH1[i], BH2[i] = BH2[i], BH1[i]

# quick solution
# plt.hist2d(BH1, BH2, bins=100, norm=LogNorm())
# plt.colorbar()
# plt.show()
