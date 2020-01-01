import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import seed

seed(97)

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
    
params_lorenz = {'sigma': 10., 'beta': 8. / 3., 'rho': 29.}
lorenz = partial(general_lorenz, **params_lorenz)

def general_coupled_lorenz(x, t, beta, o, r1, r2, epsilon):
  x1 = x[0]
  x2 = x[1]
  y = np.zeros((2, 3))
  y[0][0] = o*(x1[1] - x1[0])
  y[0][1] = r1*x1[0] - x1[1] - x1[0]*x1[2]
  y[0][2] = - beta*x1[2] + x1[0]*x1[1]
  y[1][0] = o*(x2[1] - x2[0]) + epsilon *(x1[0] -x2[0])
  y[1][1] = r2*x2[0] - x2[1] - x2[0] *x2[2]
  y[1][2] =  - beta * x2[2] + x2[0] * x2[1]
  return(y)

params_coupled_lorenz = {'beta': 8./3., 'o': 10., 'r1': 35., 'r2': 1.15, 'epsilon': 2.85}
coupled_lorenz = partial(general_coupled_lorenz, **params_coupled_lorenz)

def general_rossler(x, t, A, B, C):
    y = np.zeros(3)
    y[0] = -(x[1] + x[2])
    y[1] = x[0] + A * x[1]
    y[2] = B + x[0] * x[2] - C * x[2]
    return(y)


params_rossler={'A': .2, 'B': .2, 'C': 5.7}
rossler = partial(general_rossler, **params_rossler)

def general_lorenz_mod2(x, t, alpha, beta, gamma, delta):
  y = np.zeros(3)
  y[0] = -alpha * x[0] + x[1]** 2 - x[2]** 2 + alpha * gamma
  y[1] = x[0] * (x[1] - beta * x[2]) + delta
  y[2] = -x[2] + x[0] * (beta * x[1] + x[2])
  return(y)

params_lorenz_mod2 = {'alpha': 0.9, 'beta': 5., 'gamma': 9.9, 'delta': 1}
lorenz_mod2 = partial(general_lorenz_mod2, **params_lorenz_mod2)

def general_halvorsen(x, t, alpha):
  y = np.zeros(3)
  y[0] = -alpha * x[0] - 4 * (x[1] + x[2]) - x[1]** 2
  y[1] = -alpha * x[1] - 4 * (x[2] + x[0]) - x[2]** 2
  y[2] = -alpha * x[2] - 4 * (x[0] + x[1]) - x[0]** 2
  return(y)

params_halvorsen = {'alpha': 1.4}
halvorsen = partial(general_halvorsen, **params_halvorsen)

def plot(xs):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    if (isinstance(xs, list)):
      for x in xs:
        ax.plot(x[:, 0], x[:, 1], x[:, 2], linewidth=.5)
    else:
      ax.plot(xs[:, 0], xs[:, 1], xs[:, 2], linewidth=.5)
    plt.show()

# ts, xs = fourth_order(lorenz, 0, 40, [1., 1., 1.], h=1e-4)
# ts, xs = fourth_order(rossler, 0, 400, [1, 1, 1], h=1e-3)
# ts, xs = fourth_order(coupled_lorenz, 0, 200, np.random.rand(6).reshape((2, 3)), h=1e-3)
# ts, xs = fourth_order(lorenz_mod2, 0, 100, np.random.rand(3), h=1e-3)
ts, xs = fourth_order(halvorsen, 0, 200, np.random.rand(3), h=2e-3)