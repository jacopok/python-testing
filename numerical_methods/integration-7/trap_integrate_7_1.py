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
    solar_mass = 1.9885e30
    sigma_1 = 1e4  # m/s
    rmax_1 = 10  # pc
    
    rho0_2 = 1e8  # solar_mass / kpc**3
    r_s_2 = 10  # kpc
    rmax_2 = 100 # times r_s_2
    from scipy.constants import G
    from scipy.constants import parsec as pc

    singular_consts = 2 * sigma_1**2 / G / solar_mass * pc
        
    singular = np.vectorize(lambda x:1, otypes=[np.float64])
    
    NFW_consts = rho0_2 * r_s_2**3 * 4 * np.pi # solar_masses

    def NFW(R):
        return(R /(1+R)**2)
    
    sing_int = []
    sing_analytic = 4.65e5 # solar mass
    NFW_int = []
    NFW_analytic = 4.56e12 # solar mass
    # NFW_rect = []
    # sing_rect = []

    hrange = np.logspace(0, -5, num=100)
    for h in hrange:
        sing_int.append(singular_consts * trapezoid_integrate(singular, 0, rmax_1, h))
        NFW_int.append(NFW_consts * trapezoid_integrate(NFW, 0, rmax_2, h))
        # NFW_rect.append(NFW_consts * rectangle_integrate(NFW, 0, rmax_2, h))
        # sing_rect.append(singular_consts * rectangle_integrate(singular, 0, rmax_1, h))
    
    plt.loglog(hrange, np.abs(np.array(sing_int) - sing_analytic)/sing_analytic, label="sing")
    plt.loglog(hrange, np.abs(np.array(NFW_int) - NFW_analytic)/NFW_analytic, label="NFW")
    # plt.loglog(hrange, np.abs(np.array(NFW_rect) - NFW_analytic)/NFW_analytic, label="NFW rectangle")
    # plt.loglog(hrange, np.abs(np.array(sing_int) - sing_analytic)/sing_analytic, label="sing rectangle")
    plt.xlabel('subdivisions divided by integration region: $h$')
    plt.ylabel('Relative difference between numerical result and given value')
    plt.legend()
    plt.show()
    print(f'Singular: numeric {sing_int[-1]:.3e}, analytic {sing_analytic:.3e}')
    print(f'NFW: numeric {NFW_int[-1]:.3e}, analytic {NFW_analytic:.3e}')

    x1, x2 = plt.xlim()
    if(x1<x2):
        plt.xlim(x2, x1)

