import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from two_body_problem import G_mass, G_prime_mass, fix_com
from diffeq_integrators import hermite
from functools import partial

from two_body_analysis import E, L
from scipy.constants import G

masses = G* np.array([2e30, 6e24, 7e22])
# pos0 = [[0., 1.], [-np.sqrt(3)/2., -1./2.], [np.sqrt(3)/2., -1./2.]]
# pos0 = [[0., 1.1], [-np.sqrt(3)/2., -1./2.], [np.sqrt(3)/2., -1./2.]]
# vel0=[[1., 0.], [-1./2., np.sqrt(3) / 2.], [-1./2., - np.sqrt(3) / 2.]]

pos0 = [[0.,0.], [1.5e11, 0.], [1.5e11, 3e8]]
vel0 = [[0.,0.], [0, 3e4], [1e3, 3e4]]

vel0 = fix_com(vel0, masses)

G = partial(G_mass, Gmasses=masses)
G_prime = partial(G_prime_mass, Gmasses=masses)

tmax = 3e7
h = 1e3

pars = [0., tmax, pos0, vel0, h]

# ts, xs=hermite(G, G_prime, *pars)
def plot(xs):
  for i, pos in enumerate(np.rollaxis(xs[:,0,:,:], 1)): 

    plt.plot(*pos.T, label=f"Body {i+1}", alpha = .7)
    plt.xlabel("$x$ coordinate")
    plt.ylabel("$y$ coordinate")
  plt.legend()
  plt.show()