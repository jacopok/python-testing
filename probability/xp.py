#%%
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from scipy.optimize import curve_fit
plt.style.use(astropy_mpl_style)

lvl = np.arange(1, 21)
new_lvl = lvl[1:]
xp = np.array([
    0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000, 100000,
    120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000
])
new_xp = np.ediff1d(xp)

plt.semilogy(new_lvl, new_xp)

#%%

e = lambda x, A, b: A * np.exp(b * x)


p, pcov = curve_fit(e, new_xp, new_lvl, p0=p0)

plt.plot(new_lvl, new_xp)
plt.plot(new_lvl, e(new_lvl, *p))