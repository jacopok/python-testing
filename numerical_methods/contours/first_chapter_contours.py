# %% 

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

tot_filename = "chirpmass_tmerg_tot.dat"
tmerg_filename = "tmerg_bin.dat"
chirpmass_filename = "chirpmass_bin.dat"

with open(tot_filename) as tot_file:
    tot_data = [np.array(i.strip().split()) for i in tot_file.readlines()]
with open(tmerg_filename) as tmerg_file:
    tmerg_data = [i.strip() for i in tmerg_file.readlines() if i[0]!='#']
with open(chirpmass_filename) as chirpmass_file:
    chirpmass_data = [i.strip() for i in chirpmass_file.readlines() if i[0]!='#']

tot_data = np.array(tot_data)
tmerg_data = np.array(tmerg_data)
chirpmass_data = np.array(chirpmass_data)

# %%

import matplotlib.cm as cm

plt.ylim((0, 50))
plt.contour(tmerg_data, chirpmass_data, tot_data, cmap=cm.viridis, Nchunk = 10)

# %%
