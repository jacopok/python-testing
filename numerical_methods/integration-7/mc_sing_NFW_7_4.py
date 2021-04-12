from mean_value_7_3 import mean_value_integrate

import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

np.random.seed(3141592)

solar_mass = 1.9885e30
sigma_1 = 1e4  # m/s
rmax_1 = 10  # pc

rho0_2 = 1e8  # solar_mass / kpc**3
r_s_2 = 10  # kpc
rmax_2 = 100 # times r_s_2
from scipy.constants import G
from scipy.constants import parsec as pc

singular_consts = 2 * sigma_1**2 / G / solar_mass * pc
    
singular = np.vectorize(lambda x:1, otypes=[np.float64])

NFW_consts = rho0_2 * r_s_2**3 * 4 * np.pi # solar_masses

def NFW(R):
    return(R /(1+R)**2)

sing_int = []
sing_analytic = 4.65e5 # solar mass
NFW_int = []
NFW_analytic = 4.56e12 # solar mass
# NFW_rect = []
# sing_rect = []

nrange = np.logspace(0, 7, num=100, dtype=int)
for n in nrange:
    sing_int.append(singular_consts * mean_value_integrate(singular, 0, rmax_1, n))
    NFW_int.append(NFW_consts * mean_value_integrate(NFW, 0, rmax_2, n))

plt.loglog(nrange, np.abs(np.array(sing_int) - sing_analytic)/sing_analytic, label="sing")
plt.loglog(nrange, np.abs(np.array(NFW_int) - NFW_analytic)/NFW_analytic, label="NFW")
plt.xlabel('Number of evaluation points: $N$')
plt.ylabel('Relative difference between numerical result and given value')
plt.legend()
print(f'Singular: numeric {sing_int[-1]:.3e}, analytic {sing_analytic:.3e}')
print(f'NFW: numeric {NFW_int[-1]:.3e}, analytic {NFW_analytic:.3e}')

plt.show()