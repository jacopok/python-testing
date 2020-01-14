import numpy as np

import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

import scipy.integrate as integrate
import scipy.constants as sc
import astropy.constants as ac

from astropy.cosmology import WMAP9 as cosmo

@np.vectorize
def distance(z, integration_type, units = 'Gpc'):
    """
    `distance` takes as input:
        the redshift z,
        the `integration_type` parameter, a string which can be
        "luminosity" or "comoving", depending on which integral
        one wishes to compute.

    It returns the desired type of distance in 'units', 
    the default is 'Gpc'.
    """

    OmegaM = 0.2726 #omega matter, parameter from cosmology
    OmegaL = 0.7274 #omega lambda, parameter from cosmology

    integrand = lambda x: 1./((OmegaM*(1.+x)**3.+ \
                OmegaL) ** .5)
    
    looktime = integrate.quad(integrand, 0.0, z)[0]
    distance = looktime * (ac.c / cosmo.H0).to(units)
        
    if (integration_type == "comoving"):
        pass
    elif (integration_type == "luminosity"):
        distance *= 1+z
    else:
        raise (NotImplementedError('This integration type does not exist'))

    return distance.value

zs = np.logspace(-4,4., num=100)
comoving_dist = distance(zs, "comoving")
luminosity_dist = distance(zs, "luminosity")

# for i, (z, cd, ld) in enumerate(zip(zs, comoving_dist, luminosity_dist)):
#     print(f"z = {z:.1f}, D_C = {cd:.2f} Gpc, D_L = {ld:.2f} Gpc")

plt.loglog(zs, comoving_dist, label="Comoving distance")
plt.loglog(zs, luminosity_dist, label="Luminosity distance")

plt.loglog(zs, (cosmo.comoving_distance(zs)).to('Gpc'), label='Astropy CD')
plt.loglog(zs, (cosmo.luminosity_distance(zs)).to('Gpc'), label='Astropy LD')

plt.ylabel("Distance (\SI{}{Gpc})")
plt.xlabel("redshift $z$")
plt.legend()
plt.show()
