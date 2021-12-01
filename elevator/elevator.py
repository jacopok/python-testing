#%%

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

fnames = [f'Data{i}.csv' for i in range(1, 6)]

def read_file(fname):
    data = pd.read_csv(fname)
    times = data['Time (s)']
    ay = data['Acceleration y (m/s^2)']

    # early = times < 3
    g = np.average(ay)
    ay -= g
    vy = np.cumsum(ay * np.gradient(times))
    y = np.cumsum(vy * np.gradient(times))

    return times, ay, vy, y    

# for fname in fnames:

#     times, ay, vy, y = read_file(fname)

#     dt = np.average(np.gradient(times))
#     freqs, psd = signal.welch(ay, fs=1/dt)
    
#     plt.loglog(freqs, np.sqrt(psd * freqs))
#     plt.xlabel('Frequency [Hz]')
#     plt.ylabel('Characteristic strain [(m/s$^2$]')


for fname in fnames:

    times, ay, vy, y = read_file(fname)

    plt.plot(times, y)


# plt.xlim(60, 150)

# %%
