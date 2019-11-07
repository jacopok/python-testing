# %%

# column 1: identifier; col. 2: host total stellar mass host; col. 3: formation redshift; col. 4: metallicity star; col. 5: metallicity pop. synth.; col. 6: identifier binary; col. 7: mass black hole 1/MSun; col. 8: mass black hole 2/Msun; col. 9: delay time/Gyr; col. 10: merger time (look back)/Gyr

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


data = pd.read_csv("time_BHillustris1_30.dat", sep=" ", comment = "#", header=None, names = ["identifier", "host total stellar mass host", "formation redshift", "metallicity star", "metallicity pop. synth", "identifier binary", "mass BH1", "mass BH2", "delay time", "merger time (look back)"])

# larger BH
BH1 = list(data["mass BH1"])
# smaller BH
BH2 = list(data["mass BH2"])
n = len(data)

for i in range(n):
    if (BH1[i] < BH2[i]):
        BH1[i], BH2[i] = BH2[i], BH1[i]

plt.hist2d(BH1, BH2, bins=100, norm=LogNorm())
plt.colorbar()
plt.show()