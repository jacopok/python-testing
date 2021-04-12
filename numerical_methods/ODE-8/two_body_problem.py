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

from functools import partial

"""
The shape of the vectors in the N-body system is as follows: 
axis 0: time, arbitrary
axis 1: 0 for position, 1 for velocity
axis 2: body number
axis 3: coordinate
"""

def norm_power(x, y, n):
    return (np.linalg.norm(x - y, ord=2)** n)

def G(positions):
    """ 
    positions should be an array of points, each of which is an array of coordinates
    """
    a = np.zeros_like(positions)

    for i, x in enumerate(positions):
        for y in np.delete(positions, i, 0):
            a[i] += (y - x) / norm_power(x, y, 3)
    return (a)

def G_mass(positions, Gmasses):
    """ 
    positions should be an array of points, each of which is an array of coordinates
    """
    a = np.zeros_like(positions)

    for i, x in enumerate(positions):
        rem = lambda k : np.delete(k, i, 0)
        for y, Gm in zip(rem(positions), rem(Gmasses)):
            a[i] += Gm * (y - x) / norm_power(x, y, 3)
    return (a)

def G_prime_mass(positions, velocities, Gmasses):
    j = np.zeros_like(positions)

    for i, (xi, vi) in enumerate(zip(positions, velocities)):
        rem = lambda k: np.delete(k, i, 0)
        for xj, vj, Gmj in zip(rem(positions), rem(velocities), rem(Gmasses)):
            xij = xi - xj
            vij = vi - vj
            j[i] -= Gmj * (
                vij / norm_power(xij, 0, 3) -    
                3. * (np.dot(xij, vij) * xij)
                / norm_power(xij, 0, 5))
    return (j)
    
Gprime = partial(G_prime_mass, Gmasses=[1.,1.])

def second_order(x, t, G=G):
    pos = x[0]
    vel = x[1]
    return (np.array([vel, G(pos)]))
    
def fix_com(vel, masses=None):
    # vel should have the shape vel[#body, coord]

    if masses is None:
        masses = np.ones_like(vel[:, 0])

    mom = vel * masses[:, np.newaxis]

    p_tot = np.sum(mom, axis=0)
    m_tot = np.sum(masses)
    v_com = p_tot / m_tot

    return(vel - v_com[np.newaxis, :])

