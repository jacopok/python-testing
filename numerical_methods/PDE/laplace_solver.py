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

N = 101 # x number of points
M = 101 # y number of points
dimensions = (N, M)

field = np.zeros(dimensions)
field[0,:] = 1.

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
            old_field = np.copy(phi)
            inner_field[i, j] = relax * (\
            sum_neighbours(i+1, j+1, field) / 4.
            + rcd[i, j])\
            + (relax - 1) * phi
            if(inner_field[i,j] > 0.):
                error += np.abs((inner_field[i, j] - old_field) / inner_field[i,j])
    n, m = np.shape(field)
    relative_error = error / (n*m)

    return (field, relative_error)
