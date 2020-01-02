import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from two_body_problem import G_mass, G_prime_mass
from diffeq_integrators import hermite
from functools import partial

from two_body_analysis import E, L

masses = np.array([1., 1., 1.])
# pos0 = [[0., 1.], [-np.sqrt(3)/2., -1./2.], [np.sqrt(3)/2., -1./2.]]
pos0 = [[0., 1.1], [-np.sqrt(3)/2., -1./2.], [np.sqrt(3)/2., -1./2.]]
vel0 = [[1., 0.], [-1./2., np.sqrt(3)/2.], [-1./2., -np.sqrt(3)/2.]]

G = partial(G_mass, Gmasses=masses)
G_prime = partial(G_prime_mass, Gmasses=masses)

tmax = 500.
h = 1e-2

pars = [0., tmax, pos0, vel0, h]

ts, xs = hermite(G, G_prime, *pars)

def plot(xs):
  for i,_ in enumerate(masses):
    plt.plot(xs[:,0,i,0], xs[:,0,i,1])