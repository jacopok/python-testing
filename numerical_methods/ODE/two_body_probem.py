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

from diffeq_integrators import euler, midpoint, fourth_order

def f(x1, y1, x2, y2, v1x, v1y, v2x, v2y, t):
    distance_vector = [x2 - x1, y2 - y1]
    norm_cubed = np.linalg.norm(distance_vector, ord=2)** 3

    a1x = (x2 - x1) / norm_cubed
    a1y = (y2 - y1) / norm_cubed
    a2x = -a1x
    a2y = -a1y

    return (np.array([v1x, v1y, v2x, v2y, a1x, a1y, a2x, a2y]))

def E(xs):
    Es = []
    for i,x in enumerate(xs):
        x1, y1, x2, y2, v1x, v1y, v2x, v2y = x
        E_kin = 1 / 2. * np.linalg.norm([v1x, v1y, v2x, v2y], ord=2)** 2
        distance_vector = [x2 - x1, y2 - y1]
        E_pot = - 1 / np.linalg.norm(distance_vector, ord=2)
        if (i == 0):
            E0 = E_pot + E_kin
            Es.append(0)
        else: 
            Es.append(np.abs(E_pot + E_kin - E0))
    return(Es)

if __name__ == "__main__":
    params = (0, 300, np.array([1, 1, -1, -1, -.5, 0, .5, 0]))
    ts, xs = euler(f, *params, h=.01)
    # plt.plot(xs[:,0], xs[:,1])
    # plt.plot(xs[:, 2], xs[:, 3])
    plt.plot(ts, E(xs))
    ts, xs = midpoint(f, *params, h=.01)
    # plt.plot(xs[:,0], xs[:,1])
    # plt.plot(xs[:, 2], xs[:, 3])
    plt.plot(ts, E(xs))
    ts, xs = fourth_order(f, *params, h=.01)
    # plt.plot(xs[:,0], xs[:,1])
    # plt.plot(xs[:, 2], xs[:, 3])
    plt.plot(ts, E(xs))