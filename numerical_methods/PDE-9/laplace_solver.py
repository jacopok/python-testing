import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

from math import e as neper
from time import time

N = 100+1 # x number of points
M = 100+1 # y number of points
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
        a=1.):
    inner_field = field[1:-1,1:-1]
    if charge_density is None:
        # Rescaled Charge Density: 
        # should be rho * a^2 / 4. / epsilon_0
        # I omit the dielectric permeability factor for simplicity
        rcd = np.zeros_like(inner_field)
    else:
        rcd = charge_density * a**2 / 4.
    error = 0.
    for i, row in enumerate(inner_field):
        for j, phi in enumerate(row):
            new_field = sum_neighbours(i+1, j+1, field) /4. + rcd[i, j]
            if(new_field != 0.):
                error += np.abs((new_field - phi) / new_field)
            inner_field[i, j] = relax * new_field \
                + (1 - relax) * phi
    n, m = np.shape(inner_field)
    relative_error = error / (n*m)

    return (field, relative_error)

def test_iteration(f, iter, tol, **kwargs):
    rel = 'relax'
    if rel in kwargs:
        print(f'Testing Laplace solver with relaxation {kwargs[rel]}')
    else:
        print('Testing Laplace solver without relaxation')

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
    return (field, errs)

if __name__ == "__main__":
    
    f1, e1 = test_iteration(test_field, iteration_step, tol=1e-2)
    f2, e2 = test_iteration(test_field, iteration_step, tol=1e-2, relax=1.9)

    fig, axs = plt.subplots(2,2)

    axs[0, 0].imshow(f1)
    axs[0,0].set_title('Relaxation = 1.')
    axs[0, 1].semilogy(e1)
    axs[0,1].set_xlabel('Iteration number')
    axs[0,1].set_ylabel('Relative error $\\epsilon$')

    axs[1, 0].imshow(f2)
    axs[1,0].set_title('Relaxation = 1.9')
    axs[1, 1].semilogy(e2)
    axs[1,1].set_xlabel('Iteration number')
    axs[1,1].set_ylabel('Relative error $\\epsilon$')
    plt.show()
