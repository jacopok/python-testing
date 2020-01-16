from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

from diffeq_integrators import euler
from two_body_problem import second_order

tmax = 10
h0 = .01
x0 = [[1, 1], [-1, -1]]
v0 = [[-.5, 0], [0.5, 0]]

params = (0, tmax, np.array([x0, v0]))

ts, xs = euler(second_order, *params, h=h0)

cm_subsection = np.linspace(0., 1., 10)
colors = [ cm.Set1(x) for x in cm_subsection ]

for i in range(xs.shape[2]):
    for t in range(xs.shape[0]):
        # Plot fading tail for past locations.
        plt.plot(*xs[t,0,i,:], 'o', markersize=2, 
                 color=colors[i], alpha=float(t)/xs.shape[0])
    # Plot final location.

    plt.plot(*xs[-1, 0, i,:], 'o', color=colors[i])

plt.show()