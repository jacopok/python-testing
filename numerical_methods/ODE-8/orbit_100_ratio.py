from two_body_problem import fix_com, G_mass
from diffeq_integrators import leapfrog_KDK
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
import numpy as np
from functools import partial

tmax = 100
ratio = 1.1

x0 = np.array([[0., 0.], [1., 0.]])
v0 = np.array([[0., 0.], [0., 1.]])
masses = np.array([1, ratio])
v0 = fix_com(v0, masses)

params = (0, tmax, x0, v0)

h0 = .01

my_G = partial(G_mass, Gmasses=masses)
ts, xs = leapfrog_KDK(my_G, *params, h=h0)

for i, pos in enumerate(np.rollaxis(xs[:,0,:,:], 1)): 

  plt.plot(*pos.T, label=f"Body {i+1}")
  plt.xlabel("$x$ coordinate")
  plt.ylabel("$y$ coordinate")
plt.legend()
plt.show()