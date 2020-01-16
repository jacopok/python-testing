import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from diffeq_integrators import euler, midpoint, fourth_order, leapfrog_KDK, leapfrog_DKD, hermite

from two_body_problem import second_order, G_prime_mass, G

from functools import partial
from matplotlib.cm import rainbow

tmax = 300
x0 = [[1., 1.], [-1., -1.]]
v0 =  [[-.5, 0.], [0.5, 0.]]
params = (0, tmax, np.array([x0, v0]))
params_so = (0, tmax, np.array(x0), np.array(v0))
h0 = .01

ts, e_xs = euler(second_order, *params, h=h0)
ts, m_xs = midpoint(second_order, *params, h=2*h0)
ts, f_xs = fourth_order(second_order, *params, h=4*h0)

ts, l_xs = leapfrog_KDK(G, *params_so, h=2*h0)
ts, lD_xs=leapfrog_DKD(G, *params_so, h=2*h0)

Gp = partial(G_prime_mass, Gmasses=[1.,1.])
h_ts, h_xs = hermite(G, Gp, *params_so, h=4*h0)

solutions={
  "Euler": e_xs,
  "Midpoint": m_xs,
  "Fourth-order RK": f_xs,
  "Leapfrog KDK": l_xs,
  "Leapfrog DKD": lD_xs,
  "Hermite": h_xs
}
color = iter(rainbow(np.linspace(0,1,len(solutions))))

for n in solutions:
    c = next(color)
    for i in range(solutions[n].shape[2]):
        l=None
        if (i == 0):
            l = n
        plt.plot(*np.rollaxis(solutions[n][:,0,i,:], -1), label=l, c=c, alpha=.7)

plt.legend()
plt.show()

