import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')
from math import e as neper
from time import time

N = 101 # x number of points
M = 101 # y number of points
dimensions = (N, M)

test_field = np.zeros(dimensions)
test_field[0,:] = 1.

def sum_neighbours(i, j, matrix):
    neighbours = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    sum = 0.
    for ind in neighbours:
        sum += matrix[ind]
    return(sum)

def iteration_step(field,
        relax=1,
        charge_density=None,
        a=None):
    inner_field = field[1:-1,1:-1]
    if not charge_density:
        # Rescaled Charge Density: 
        # should be rho / a^2
        rcd = np.zeros_like(inner_field)
    error = 0.
    for i, row in enumerate(inner_field):
        for j, phi in enumerate(row):
            new_field = sum_neighbours(i+1, j+1, field) / 4. \
            + rcd[i, j]
            if(new_field > 0.):
                error += np.abs((new_field - phi) / new_field)
            inner_field[i, j] = relax * new_field \
                + (1 - relax) * phi
    n, m = np.shape(field)
    relative_error = error / (n*m)

    return (field, relative_error)

def test_iteration(f, iter, tol, **kwargs):
    field = np.copy(f)
    field, e0 = iter(field, **kwargs)
    errs = [e0]

    error_efolds = np.log(e0 / tol)
    print(f"{int(error_efolds)+1} error e-folds to go")
    current_efold = e0 / neper
    old_time = time()
    efold_counter = 1

    while errs[-1] > tol:
        field, e = iter(field, **kwargs)
        errs.append(e)

        if (e < current_efold):
            new_time = time()
            print(f"Finished efold {efold_counter} in {new_time - old_time :.2f} seconds")
            old_time = new_time
            efold_counter += 1
            current_efold /= neper

        if (e > 10 * e0):
            print("algorithm diverged")
            return (None)
    
    new_time = time()
    print(f"Finished what remained of efold {efold_counter} in {new_time - old_time :.2f} seconds")

    print(f"Finished in {len(errs)} steps")
    return(field, errs)