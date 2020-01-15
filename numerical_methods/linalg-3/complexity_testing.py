import numpy as np
from numpy.linalg import matrix_rank, solve
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from scipy.optimize import curve_fit
from gaussian_elimination_3_1 import gaussian_elimination
from test_data_generation import test_data

def complexity(sizes, alg=gaussian_elimination, **options):
    from time import time
    from random import sample, randrange

    def n_test(n):
        t1 = time()
        alg(*test_data(n, **options))
        t2 = time()
        return (t2 - t1)
    
    times= []
    for n in sizes:
        times.append(n_test(n))
    
    model = lambda x, exponent, constant: constant +  x * exponent
    
    # want to do a logarithmic fit, but with constant errors on the linear data
    # so, we do linear error propagation
    popt, pcov = curve_fit(model, np.log(sizes), np.log(times), sigma=1/np.array(times))
    plt.plot(sizes, times, label=f'Exponent: {popt[0]:.3f} +- {pcov[0,0]:.3f}')
    plt.plot(sizes, np.exp(model(np.log(sizes), *popt)), linestyle=':')
    plt.legend()
    plt.xlabel('Matrix dimension')
    plt.ylabel('Time [s]')
    