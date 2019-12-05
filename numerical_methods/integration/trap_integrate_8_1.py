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
    rmax_1 = 10 * pc  # pc
    
    rho0_2 = 1e8 * solar_mass / pc**3   # solar_mass / kpc**3
    r_s_2 = 10 * pc # m
    rmax_2 = 100 * r_s_2
    from scipy.constants import G

    singular_consts = 4 * sigma_1**2 / (2 * G) / solar_mass
        
    singular = np.vectorize(lambda x:1, otypes=[np.float64])
    
    NFW_consts = rho0_2 * r_s_2**3 * 4 * np.pi / solar_mass

    def NFW(R):
        return(R /(1+R))
    
    sing_int_constin = []
    sing_int_constout = []
    NFW_int_constout = []
    NFW_int_constin = []
    hrange = np.logspace(0, -4)
    for h in hrange:
        sing_int_constout.append(singular_consts * trapezoid_integrate(singular, 0, rmax_1, h))
        sing_int_constin.append(trapezoid_integrate(lambda x : singular(x) * singular_consts, 0, rmax_1, h))
        NFW_int_constout.append(NFW_consts * trapezoid_integrate(NFW, 0, rmax_2, h))
        NFW_int_constin.append(trapezoid_integrate(lambda x: NFW(x) * NFW_consts, 0, rmax_2, h))
    
    # plt.loglog(hrange, sing_int_constin)
    plt.loglog(hrange, sing_int_constout, label="sing")
    # plt.loglog(hrange, NFW_int_constin)
    plt.loglog(hrange, NFW_int_constout, label="NFW")
    plt.legend()