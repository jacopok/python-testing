#%%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm

R = 1+0.3j
L = -2-0.1j

def y(omega, p, R=R, L=L):
    return omega * (R * (1 + p) + L * (1 - p))

ps = np.linspace(0, 1.)
omegas = np.logspace(-1, 1)

omegabar = 1
pbar = 1.

def chisquare(omega, p):
    return abs(y(omega, p) - y(omegabar, pbar))**2
    
O, P = np.meshgrid(omegas, ps)


cs = plt.contourf(O, P, chisquare(O, P), locator=ticker.LogLocator(numticks=9))
plt.colorbar(cs)
plt.xscale('log')
# %%
