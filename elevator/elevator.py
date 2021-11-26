#%%

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

fnames = [f'Data{i}.csv' for i in range(1, 4)]

for fname in fnames:
    data = pd.read_csv(fname)
    times = data['Time (s)']
    dt = np.average(np.gradient(times))
    ay = data['Acceleration y (m/s^2)']

    # early = times < 3
    g = np.average(ay)
    ay -= g

    vy = np.cumsum(ay * np.gradient(times))
    y = np.cumsum(vy * np.gradient(times))

    plt.plot(times, y)
plt.ylabel('Position [m]')
plt.show()

# %%
