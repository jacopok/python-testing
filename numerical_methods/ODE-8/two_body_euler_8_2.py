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

for i in range(xs.shape[3]):
    plt.plot(*np.rollaxis(xs[:, 0, i,:], -1))

plt.show()