import numpy as np
from numpy.linalg import matrix_rank, solve
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from scipy.optimize import curve_fit
from gaussian_elimination_3_1 import gaussian_elimination
from test_data_generation import test_data

def complexity(nmax, every=1, **options):
    from time import time
    from random import sample, randrange

    def n_test(n):
        t1 = time()
        gaussian_elimination(*test_data(n, **options))
        t2 = time()
        return (t2 - t1)
    
    sizes = range(2, nmax, every)

    times= []
    for n in sizes:
        times.append(n_test(n))
    
    model = lambda x, exponent, constant: constant * x**exponent
    popt, pcov = curve_fit(model, range(len(times)), times)
    plt.plot(sizes, times, label=f'Exponent: {popt[0]:.3f} +- {pcov[0,0]:.3f}')
    plt.plot(sizes, model(sizes, *popt))
    plt.legend()
    plt.xlabel('')
    return (popt[0], pcov[0, 0])
    