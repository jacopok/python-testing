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

def spectrogram(x, y):
    n = len(x)
    nfreq = int(n / 1000)

    dxmin = np.diff(x).min()
    duration = x.ptp()
    omegas = np.linspace(1 / duration, 100 / duration, nfreq)
    periodogram = lombscargle(x, y, omegas)
    freqs = omegas /(2*np.pi)

    kmax = periodogram.argmax()
    print("%8.3f" % (freqs[kmax],))

    lab = 'x between ' + str(min(x)) + ' and ' + str(max(x))

    plt.figure(1)
    plt.plot(freqs, np.sqrt(4 * periodogram / nfreq), label=lab)
    plt.xlabel('Frequency (1/V)')
    plt.axvline(freqs[kmax], color='r', alpha=0.25)
    plt.show()
    return(freqs[kmax])


length = len(x)//2

fmax = []

fmax.append(spectrogram(x, y))
fmax.append(spectrogram(x[:length], y[:length]))
fmax.append(spectrogram(x[length:], y[length:]))

#plt.legend()

plt.figure(2)
plt.plot(x, y, 'b')
for f in fmax:
    plt.plot(x, np.sin(x * f * 2 * np.pi) * np.max(y), 'r')
plt.xlabel('x')
plt.ylabel('y')

plt.show()
