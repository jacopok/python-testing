import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
from mpl_toolkits.mplot3d import Axes3D

rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

from diffeq_integrators import fourth_order
from functools import partial

def general_lorenz(x, t, sigma, rho, beta):
    y = np.zeros(3)
    y[0] = sigma * (x[1] - x[0])
    y[1] = x[0] * (rho - x[2]) - x[1]
    y[2] = x[0] * x[1] - beta * x[2]
    return (y)
    
params = {'sigma': 10., 'beta': 8. / 3., 'rho': 29.}
lorenz = partial(general_lorenz, **params)

ts, xs = fourth_order(lorenz, 0, 40, [1., 1., 1.], h=1e-4)

def plot(xs):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(xs[:, 0], xs[:, 1], xs[:, 2], linewidth=1)
    plt.show()
