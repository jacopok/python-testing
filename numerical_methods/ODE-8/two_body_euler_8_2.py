import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

from diffeq_integrators import euler
from two_body_problem import second_order

tmax = 300
h0 = .01
x0 = [[1, 1], [-1, -1]]
v0 = [[-.5, 0], [0.5, 0]]

params = (0, tmax, np.array([x0, v0]))

ts, xs = euler(second_order, *params, h=h0)

"""
xs = xs[time, x/v, body#, coordinate]
"""

if __name__ == '__main__':
    for i, pos in enumerate(np.rollaxis(xs[:,0,:,:], 1)): # we loop through the positions the two particles
        # pos = pos [time , coordinate]
        # we need to plot the x and y coordinates
        # which are on the second axis
        # so we transpose
        plt.plot(*pos.T, label=f"Body {i+1}")

    plt.xlabel("$x$ coordinate")
    plt.ylabel("$y$ coordinate")
    plt.legend()
    plt.show()