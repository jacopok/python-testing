# %%

from scipy.constants import *
from math import sqrt
from math import exp

T = 1.5e6 # K
M_sun = 1.98847e30 # kg
R_sun = 696e6 # m
year = 365 * 24 * 3600  # s 
Mdot = 2e-14 * M_sun / year
r0 = 1.003 * R_sun
cgs_to_mks_density =  1e-3 * (1e-2)**(-3)
rho0 = 1e-14 * cgs_to_mks_density  # kg/m**3
mu = .62

# %%

v0 = Mdot / (4* pi * r0**2 * rho0)

E_kin0 = .5 * v0**2 # J/kg
E_grav0 = - G * M_sun / r0   
E_chem0 = 5/2* R*T/mu

# %%

a = sqrt(R * T / mu)
E_kin_crit = .5 * a ** 2
E_grav_crit = - 2 * a**2

# %% [markdown]
# New exercise

# %%

Teff = 3200  # K
R_star = 30 * R_sun
L_sun = 3.828e26 # W
L_star = 85 * L_sun
M_star = 6 * M_sun
T_star = 1e6  # K
rho0_star = 1e-13 * cgs_to_mks_density

#%% 

Mdot = pi * (G*M_star)**2 * (mu/R/T_star)**(3/2) * rho0_star * exp(2 - mu*G*M_star/R/T_star/R_star)

# %%
