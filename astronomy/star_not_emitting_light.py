#%%

import numpy as np
import scipy.constants as sc
from astropy.constants import codata2018 as ac
from astropy.constants import iau2015 as aa
import astropy.units as u

# %%

# The sun's core extends to about .25 R_sun
# its temperature is around 15 MK
# in order to reach helium burning (the next stage)
# it would need to reach ~ 100MK

volume = (.25 * aa.R_sun) ** 3 * 4 * np.pi / 3
density = 150 * u.g / u.cm ** 3
T_hyd = 15e6 * u.K
T_hel = 100e6 * u.K 
heat_capacity = 3 / 2 * ac.k_B / ac.m_p

mass = volume * density

delta_T = T_hel - T_hyd
energy_needed = (delta_T  * mass * heat_capacity).to(u.J)

sun_luminosity = (1 * u.L_sun).to(u.W)

prec = 2

print(energy_needed.to_string(precision=prec, format='e'))
print(f'{sun_luminosity=:s}')

time = (energy_needed / sun_luminosity).to(u.Myr)

print(f'{time=:s}')

# %%

from sunpy.sun.models import interior

