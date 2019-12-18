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

# def remove_index(list, i):
#     return (np.append(list[:i], list[:i + 1]))
    
def norm_cubed(x, y):
    return(np.linalg.norm(x-y, ord=2)** 3)

def G(positions):
    """ 
    positions should be an array of points, each of which is an array of coordinates
    """
    a = np.zeros_like(positions)

    for i, x in enumerate(positions):
        for y in np.delete(positions, i, 0):
            a[i] += (y - x) / norm_cubed(x, y)
    return (a)

def second_order(x, t, G=G):
    pos = x[0]
    vel = x[1]
    return(np.array([vel, G(pos)]))

# def f(x1, y1, x2, y2, v1x, v1y, v2x, v2y, t):
#     distance_vector = [x2 - x1, y2 - y1]
#     norm_cubed = np.linalg.norm(distance_vector, ord=2)** 3

#     a1x = (x2 - x1) / norm_cubed
#     a1y = (y2 - y1) / norm_cubed
#     a2x = -a1x
#     a2y = -a1y

#     return (np.array([v1x, v1y, v2x, v2y, a1x, a1y, a2x, a2y]))

if __name__ == "__main__":
    params = (0, 1000, np.array([[[1, 1],[-1,-1]], [[-.5, 0], [0.5, 0]]]))
    h0 = .01
    plt.close()
    ts, xs = euler(second_order, *params, h=h0)
    plt.plot(xs[:,0,0,0], xs[:,0,0,1])
    ts, xs = midpoint(second_order, *params, h=2*h0)
    plt.plot(xs[:,0,0,0], xs[:,0,0,1])
    ts, xs = fourth_order(second_order, *params, h=4*h0)
    plt.plot(xs[:,0,0,0], xs[:,0,0,1])
    plt.legend()
    plt.show()