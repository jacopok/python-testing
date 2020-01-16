import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from two_body_problem import G_mass, G_prime_mass, fix_com
from diffeq_integrators import leapfrog_DKD
from functools import partial

from two_body_analysis import E, L
from scipy.constants import G
from astropy import units as u
from astropy import constants as ac

v0 = np.load('Nbody/velocities.npy')
p0 = np.load('Nbody/coordinates.npy')

N = 10
p0 *= (u.pc).to('m')
v0 *= (u.km / u.s).to('m/s')
v0 = fix_com(v0)

G = partial(G_mass, Gmasses=np.ones(N)*ac.GM_sun.value*1e4)

dt = 1e10
steps= int(1e2)

ts, xs = leapfrog_DKD(G, 0., steps*dt, p0[:N], v0[:N], dt)

def plot(xs):
  for i, pos in enumerate(np.rollaxis(xs[:,0,:,0:2], 1)): 

    lab = None
    if (i % 10 == 0):
      lab=f"Body {i+1}"
    plt.plot(*pos.T, label=lab, alpha = .7)
    plt.xlabel("$x$ coordinate")
    plt.ylabel("$y$ coordinate")
  plt.legend()
  plt.show()