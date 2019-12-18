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

if __name__ == "__main__":
    params = (0, 10, np.array([1, 1, -1, -1, -.5, 0, .5, 0]))
    h0 = .01
    ts, xs = euler(f, *params, h=h0)
    plt.close()
    plt.plot(xs[:,0], xs[:,1])
    plt.plot(xs[:, 2], xs[:, 3])
    ts, xs = midpoint(f, *params, h=2*h0)
    plt.plot(xs[:,0], xs[:,1])
    plt.plot(xs[:, 2], xs[:, 3])
    ts, xs = fourth_order(f, *params, h=4*h0)
    plt.plot(xs[:,0], xs[:,1])
    plt.plot(xs[:, 2], xs[:, 3])
    plt.show()