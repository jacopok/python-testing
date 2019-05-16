import numpy as np
from scipy.signal import lombscargle
import matplotlib.pyplot as plt

plt.style.use('bmh')

np.random.seed(12346)

n = 100
x = np.sort(10*np.random.rand(n))
# Dominant periodic signal
y = np.sin(2.5*x)
# Add some smaller periodic components
y += 0.15*np.cos(0.75*x) + 0.2*np.sin(4*x+.1)
# Add some noise
y += 0.2*np.random.randn(x.size)

plt.figure(1)
plt.plot(x, y, 'b')
plt.xlabel('x')
plt.ylabel('y')

plt.show()

dxmin = np.diff(x).min()
duration = x.ptp()
freqs = np.linspace(1/duration, n/duration, 5*n)
periodogram = lombscargle(x, y, freqs)

kmax = periodogram.argmax()
print("%8.3f" % (freqs[kmax],))

plt.figure(2)
plt.plot(freqs, np.sqrt(4*periodogram/(5*n)))
plt.xlabel('Frequency (rad/s)')
plt.axvline(freqs[kmax], color='r', alpha=0.25)
plt.show()