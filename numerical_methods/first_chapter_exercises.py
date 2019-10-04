import numpy as np

import matplotlib.pyplot as plt
plt.style.use('seaborn')

#%% Exercise 1.1

g = 9.81 # m*s**(-2)

t = float(input("Please input the time t in seconds"))
t = float(input("Please input the height h in metres"))

x = 1/2 * g * t**2
print(f"x = {x}")

t2 = np.sqrt(2*g*h)
print(f"t_2 = {t2}")

#%% Exercise 1.2

def distance(z, type=None):
    """
    `distance` takes as input:
        the redshift z,
        the `type` parameter, a string which can currently be
        "luminosity" or "comoving", depending on which integral
        one wishes to compute.

    It returns the desired type of distance.
    """

    H0=67.2 #Hubble constant in km/s/Mpc
    convert=1e5/3.086e24*3.1536e7*1e9
    #converts from km/s/Mpc to Gyr
    OmegaM=0.2726 #omega matter, parameter from cosmology
    OmegaL= 0.7274 #omega lambda, parameter from cosmology

    try:
        integrand = {
            "comoving": lambda x: 1./((OmegaM*(1.+x)**3.+ \
                OmegaL)**0.5),
            "luminosity": lambda x: (1.+x)/((OmegaM*(1.+x)**3.+ \
                OmegaL)**0.5),
        }[type]
    except KeyError:
        raise(NotImplementedError("This type of integral is not implemented."))

    import scipy.integrate as integrate

    ltime=integrate.quad(integrand, 0.0, z)
    look=ltime[0]
    look/=(H0*convert)
    return look #function looktime returns look, which is
    #the lookback time at redshift z in comoving framework

#%%

distance(1, "not")

#%%

z=10. #initial redshift
comoving_dist=[] #comoving distance list
luminosity_dist=[] #luminosity distance list
redsh=[] #redshift list
while(z>0.0):
    comoving_dist.append(distance(z, "comoving"))
    luminosity_dist.append(distance(z, "luminosity"))
    redsh.append(z)
    z-=0.1
for i in range(len(look)):
    print(f"z = {redsh[i]:.1f}, D_C = {comoving_dist[i]:.2f}, D_L = {luminosity_dist[i]:.2f}")
