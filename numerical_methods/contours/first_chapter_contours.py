# %% 

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

import os
os.chdir('/home/jacopo/PycharmProjects/python-testing/numerical_methods/contours')

tot_filename = "chirpmass_tmerg_tot.dat"
tmerg_filename = "tmerg_bin.dat"
chirpmass_filename = "chirpmass_bin.dat"

with open(tot_filename) as tot_file:
    tot_data = [np.array(i.strip().split(), dtype=np.float) for i in tot_file.readlines()]
with open(tmerg_filename) as tmerg_file:
    tmerg_data = [i.strip() for i in tmerg_file.readlines() if i[0]!='#']
with open(chirpmass_filename) as chirpmass_file:
    chirpmass_data = [i.strip() for i in chirpmass_file.readlines() if i[0]!='#']

tot_data = np.array(tot_data, dtype=np.float)
tmerg_data = np.array(tmerg_data, dtype=np.float)
chirpmass_data = np.array(chirpmass_data, dtype=np.float)

# %%

import matplotlib.cm as cm
import matplotlib.ticker as ticker

plt.ylim((0, 30))

ctf = plt.contourf(tmerg_data, chirpmass_data, tot_data, cmap=cm.inferno, levels=100)
ct = plt.contour(tmerg_data, chirpmass_data, tot_data)

def fmt(x):
    return(f'{x:.0e}')

ct.levels = [fmt(i) for i in ct.levels]

cb = plt.colorbar(ctf, format=':%.1e')

plt.clabel(ct, ct.levels)

# %%

# # column 1: identifier; col. 2: host total stellar mass host; col. 3: formation redshift; col. 4: metallicity star; col. 5: metallicity pop. synth.; col. 6: identifier binary; col. 7: mass black hole 1/MSun; col. 8: mass black hole 2/Msun; col. 9: delay time/Gyr; col. 10: merger time (look back)/Gyr
