import scipy.constants as sc
from astropy.constants import codata2018 as ac
from astropy.constants import iau2015 as aa
import astropy.units as u
from astropy.cosmology import Planck15 as cosmo
import astropy.uncertainty as aun

import numpy as np

Teff = 3200 * u.K
r0 = 30 * u.R_sun
L = 85 * u.L_sun
M = 6 * u.M_sun
rho0 = 1e-13 * u.g / u.cm ** 3
T = 1e6*u.K

mu = .62

R =  ac.k_B / u.u

a = np.sqrt(R * T / mu)

r_c = ac.G * M / 2 / a ** 2

v0 = a * (r_c / r0)** 2 * np.exp(- 2 * r_c / r0 + 3 / 2)

Mdot = 4 * np.pi * r0 ** 2 * v0 * rho0

e0 = (-ac.G * M / r0 + 1 / 2 * v0 ** 2 + 5 / 2 * R * T / mu).cgs

ec = (-ac.G * M / r_c + 1 / 2 * a ** 2 + 5 / 2 * R * T / mu).cgs

