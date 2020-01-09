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
def distance(z, integration_type=None):
    """
    `distance` takes as input:
        the redshift z,
        the `integration_type` parameter, a string which can currently be
        "luminosity" or "comoving", depending on which integral
        one wishes to compute.

    It returns the desired type of distance.
    """

    H0 = cosmo.H0.value #Hubble constant in km/s/Mpc
    convert = 1e6 * sc.year / ac.pc.value
    #converts from km/s/Mpc to Gyr
    OmegaM = 0.2726 #omega matter, parameter from cosmology
    OmegaL = 0.7274 #omega lambda, parameter from cosmology

    integrand = lambda x: 1./((OmegaM*(1.+x)**3.+ \
                OmegaL) ** .5)
    
    looktime = integrate.quad(integrand, 0.0, z)[0]
    distance = looktime / H0 / convert
    
    if (integration_type == "comoving"):
        pass
    elif (integration_type == "luminosity"):
        distance *= 1+z
    else:
        raise (NotImplementedError)

    return distance

zs = np.linspace(0,10., num=100)
comoving_dist = distance(zs, "comoving")
luminosity_dist = distance(zs, "luminosity")

for i, (z, cd, ld) in enumerate(zip(zs, comoving_dist, luminosity_dist)):
    print(f"z = {z:.1f}, D_C = {cd:.2f}, D_L = {ld:.2f}")

plt.plot(zs, comoving_dist, label="Comoving distance")
plt.plot(zs, luminosity_dist, label="Luminosity distance")

plt.ylabel("Distance (light-\SI{}{Gyr})")
plt.xlabel("redshift $z$")
plt.legend()
plt.show()

plt.plot(zs, (cosmo.comoving_distance(zs) / ac.c).to('Gyr'))
plt.plot(zs, (cosmo.luminosity_distance(zs) / ac.c).to('Gyr'))
