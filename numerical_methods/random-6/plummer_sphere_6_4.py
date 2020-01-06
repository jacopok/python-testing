import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

M = 1e4  # solar masses
a_scale = 5. # parsec
sigma_speed = 5. # km/s
N = int(1e4)  # number of simulated stars

class plummer_radius(stats.rv_continuous):
    def __init__(self, a_scale=a_scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = a_scale
        self.a = 0.

    def _pdf(self, r):
        R = r / self.scale
        norm = 3 / (4 * np.pi * self.scale ** 3) 
        power = (1 + R**2 )**(-5/2) * R**2
        return (norm * power)

    def _cdf(self, r):
        R = r / self.scale
        return (R ** 3 * (R ** 2 + 1)**(-3./2.))
    
    def _ppf(self, x):
        R = np.sqrt(1 / (1 - x ** (2 / 3)) - 1)
        return(R * self.scale)

class maxwell_rv_3d(stats.rv_continuous):
    def __init__(self, scale=sigma_speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = scale

    def _pdf(self, v):
        # pdf of the modulus
        scaled_v = v / self.scale 
        norm = np.sqrt(2 / np.pi) * scaled_v ** 2
        exp = np.exp(-scaled_v ** 2 / 2)
        return (norm * exp / self.scale)

    def _rvs(self):
        # sampling the x, y, z components ...
        # will have to fix the inconsistency 
        gauss = stats.norm(loc=0., scale=self.scale)
        newsize = self._size + (3,)
        return(gauss.rvs(size = newsize))

class sine_rv(stats.rv_continuous):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a = 0.
        self.b = np.pi

    def _pdf(self, theta):
        return (np.sin(theta) / 2)
    
    def _ppf(self, x):
        return(np.arccos(1 - 2*x))

def angular_sample(size=None):
    if (not size):
        N = 1
    elif (int(size) == size):
        N = int(size)
    else:
        return (None)

    phi = stats.uniform(loc=0., scale=np.pi * 2)
    theta = sine_rv()
    omegas= []
    for _ in range(N):
        phi_sample = phi.rvs()
        theta_sample = theta.rvs()
        omegas.append([theta_sample, phi_sample])
    return (np.array(omegas))
    
def spherical_to_cartesian(theta, phi):
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    return (np.array([x, y, z]))

if __name__ == "__main__":    
    r_p = plummer_radius()
    m_v = maxwell_rv_3d()

    _radii = r_p.rvs(size=N)
    _coords = []
    for r in _radii:
        coord = r * spherical_to_cartesian(*angular_sample()[0])
        _coords.append(coord)
    coordinates = np.array(_coords)
    velocities = m_v.rvs(size=N)

    v0 = np.zeros(N)
    for i in range(3):
        v0 += velocities[:, i]** 2
    v_moduli = np.sqrt(v0)

    """
    The coordinates of the new objects
    are contained in "coordinates"

    The velocities are contained in "velocities"
    In order to check that the velocities 
    are correctly distributed do:

    plt.plot(b, m_v.pdf(b))
    plt.hist(v_moduli, bins=100, density=True)
    """

