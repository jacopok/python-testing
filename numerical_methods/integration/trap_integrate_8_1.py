import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text.latex', preamble=r'''\usepackage{amsmath}
\usepackage{physics}
\usepackage{siunitx}
''')

# def rectangle_integrate(f, a, b, h_frac):
#     h = (b-a)*h_frac
#     x = np.arange(a+h/2., b-h/2., h)
#     return (np.sum(f(x)) * h)

def trapezoid_integrate(f, a, b, h_frac):
    h = (b-a)*h_frac
    edges_sum = (f(a) + f(b)) / 2.
    x = np.arange(a + h, b, h)
    return (h * (np.sum(f(x)) + edges_sum))
    
if __name__ == "__main__":
    pc = 3.0857e16
    solar_mass = 2e30
    sigma_1 = 10e3  # km/s
    rmax_1 = 10  # pc
    
    rho0_2 = 1e8  # solar_mass / kpc**3
    r_s_2 = 10  # pc
    rmax_2 = 100 # times r_s_2
    from scipy.constants import G

    singular_consts = 2 * sigma_1**2 / G / solar_mass * pc
        
    singular = np.vectorize(lambda x:1, otypes=[np.float64])
    
    NFW_consts = rho0_2 * (r_s_2*pc)**3 * 4 * np.pi / solar_mass

    def NFW(R):
        return(R /(1+R))
    
    sing_int = []
    NFW_int = []
    hrange = np.logspace(0, -4)
    for h in hrange:
        sing_int.append(singular_consts * trapezoid_integrate(singular, 0, rmax_1, h))
        NFW_int.append(NFW_consts * trapezoid_integrate(NFW, 0, rmax_2, h))
    
    plt.loglog(hrange, sing_int, label="sing")
    plt.loglog(hrange, NFW_int, label="NFW")
    plt.legend()

    x1, x2 = plt.xlim()
    plt.xlim(x2, x1)

