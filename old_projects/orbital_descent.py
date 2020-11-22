import numpy as np
import scipy.constants as sc
from astropy.constants import codata2018 as ac
from astropy.constants import iau2015 as aa
import astropy.units as u
from astropy.cosmology import Planck15 as cosmo
import astropy.uncertainty as aun
import matplotlib.pyplot as plt

R = 600 * u.km + aa.R_earth
R_space = 100 * u.km + aa.R_earth
M = 100 * u.kg
A = 100 * u.m ** 2
emissivity = .5

v = np.sqrt(aa.GM_earth / R)

E_tot = 1 / 2 * M * v ** 2 + aa.GM_earth*(1 / R_space - 1 / R) * M

times = np.logspace(0, 2) * u.d

temperatures = ((E_tot / times / A / emissivity / ac.sigma_sb)**(1 / 4)).to(u.deg_C, equivalencies=u.temperature())

# plt.plot(times, temperatures)
# plt.xlabel(f'Descent time ({times.unit})')
# plt.ylabel(f'Temperature ({temperatures.unit})')
# plt.grid()
# plt.show()

time = 60 * u.d
Rs = aa.R_earth + np.logspace(1, 8) * u.km
vs = np.sqrt(aa.GM_earth / Rs)
E_tots = 1 / 2 * M * vs ** 2 + aa.GM_earth*(1 / R_space - 1 / Rs) * M

temperatures = ((E_tots / time / A / emissivity / ac.sigma_sb)**(1 / 4)).to(u.deg_C, equivalencies=u.temperature())

plt.plot(Rs - aa.R_earth, temperatures)
plt.xlabel(f'Orbit height above ground ({Rs.unit})')
plt.ylabel(f'Temperature ({temperatures.unit})')
plt.grid()
plt.show()
