import numpy as np

def box_muller(loc=0., scale=1., N=int(1e6)):

    Ntrue = int(N/2)
    z1 = np.random.uniform(size=Ntrue)
    z2 = np.random.uniform(size=Ntrue)
    
    gaussian_deviates = []

    for (zr, ztheta) in zip(z1, z2):
        r = np.sqrt(-2 * scale ** 2 * np.log(1 - zr))
        theta = 2 * np.pi * ztheta
        
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        gaussian_deviates.append(x)
        gaussian_deviates.append(y)
    return (gaussian_deviates)

