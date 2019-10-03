import numpy as np

import matplotlib.pyplot as plt
plt.style.use('seaborn')

#%% Exercise 1.1

g = 9.81 # m*s**(-2)

t = float(input("t = "))
h = float(input("h = "))

x = 1/2 * g * t**2
print(f"x = {x}")

t2 = np.sqrt(2*g*h)
print(f"t_2 = {t2}")
#%% Exercise 1.2

import scipy.integrate as integrate

def distance(z, type=None): #definition of new function looktime.
    # This function takes one argument (z)
    H0=67.2 #Hubble constant in km/s/Mpc
    convert=1e5/3.086e24*3.1536e7*1e9
    #converts from km/s/Mpc to Gyr
    OmegaM=0.2726 #omega matter, parameter from cosmology
    OmegaL= 0.7274 #omega lambda, parameter from cosmology
    if(type=="comoving"):
        integrand = lambda x: 1./((OmegaM*(1.+x)**3.+ \
            OmegaL)**0.5)
    elif(type=="luminosity"):
        integrand = lambda x: (1.+x)/((OmegaM*(1.+x)**3.+ \
            OmegaL)**0.5)
    else:
        raise(NotImplementedError("This type of integral is not implemented."))

    #integrand is the function I want to integrate
    #between 0 and z
    ltime=integrate.quad(integrand, 0.0, z)
    #ltime is an array of 2 elements:
    # ltime[0] = result of integral
    # ltime[1] = error
    look=ltime[0]
    look/=(H0*convert)
    return look #function looktime returns look, which is
    #the lookback time at redshift z in comoving framework

z=10. #initial redshift
comoving_dist=[] #comoving distance list
luminosity_dist=[] #luminosity distance list
redsh=[] #redshift list
while(z>0.0):
    comoving_dist.append(distance(z, "comoving"))
    luminosity_dist.append(distance(z, "luminosity"))
    redsh.append(z) #store z into list redsh
    z-=0.1
for i in range(len(look)): #loop over the elements of look
    print(redsh[i], comoving_dist[i], luminosity_dist[i]) #prints redshift and
    #corresponding look back time list
