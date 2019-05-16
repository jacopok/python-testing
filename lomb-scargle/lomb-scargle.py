import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import lombscargle
from scipy.stats import linregress

plt.style.use('bmh')

data = pd.read_csv('datafull.csv')

data = data.sort_values('x')

x = data['x'].values
y_test = data['y'].values

slope, intercept, r, p, err = linregress(x, y_test)
y = y_test - slope * x - intercept

n = len(x)
nfreq = int(n / 10000)

dxmin = np.diff(x).min()
duration = x.ptp()
freqs = np.linspace(1 / duration, 100 / duration, nfreq)
periodogram = lombscargle(x, y, freqs)

kmax = periodogram.argmax()
print("%8.3f" % (freqs[kmax],))

plt.figure(1)
plt.plot(freqs, np.sqrt(4 * periodogram / nfreq))
plt.xlabel('Frequency (rad/s)')
plt.axvline(freqs[kmax], color='r', alpha=0.25)
plt.show()

plt.figure(2)
plt.plot(x, y, 'b')
plt.plot(x, np.sin(x * freqs[kmax]) * np.max(y), 'r')
plt.xlabel('x')
plt.ylabel('y')

plt.show()
