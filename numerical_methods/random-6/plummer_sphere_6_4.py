import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from scipy.integrate import quad

M = 1e4  # solar masses
a_scale = 5. # parsec
sigma_speed = 5. # km/s
N = int(M)  # number of simulated stars

np.random.seed(3141592)

class plummer_radius(stats.rv_continuous):
    def __init__(self, a_scale=a_scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = a_scale
        self.a = 0.

    def _pdf(self, r):
        R = r / self.scale
        norm = 3 / (4 * np.pi * self.scale ** 3)  
        power = (1 + R**2 )**(-5/2) * R**2
        return (power * 2/np.pi)

    def _cdf(self, r):
        R = r / self.scale
        return (R ** 3 * (R ** 2 + 1)**(-3./2.) * 2 * np.pi)
    
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

    radii = r_p.rvs(size=N)
    coords = []
    for r in radii:
        coord = r * spherical_to_cartesian(*angular_sample()[0])
        coords.append(coord)
    coordinates = np.array(coords)
    velocities = m_v.rvs(size=N)

    v_moduli = np.linalg.norm(velocities, axis=-1)
    x_moduli = np.linalg.norm(coordinates, axis=-1)

    """
    The coordinates of the new objects
    are contained in "coordinates"

    The velocities are contained in "velocities"
    In order to check that the velocities 
    are correctly distributed do:

    """
    fig, axs = plt.subplots(2, 2)


    v, b, _ = axs[0,1].hist(v_moduli, bins=100, density=True)
    axs[0, 1].plot(b, m_v.pdf(b))
    axs[0,1].set_xlabel('Velocity modulus [$\\SI{}{km/s}$]')

    r, br, _ = axs[0, 0].hist(x_moduli, bins = 1000, density = True)
    rho, brho = np.histogram(x_moduli, bins=1000)

    axs[1, 1].scatter(*(coordinates[:, i] for i in [0,1]), s=1)
    axs[1, 1].set_xlabel('$x$ position [\\SI{}{pc}]')
    axs[1, 1].set_ylabel('$y$ position [\\SI{}{pc}]')
    axs[1, 1].set_xlim((-20, 20))
    axs[1, 1].set_ylim((-20, 20))

    r_bins = (br[1:]+br[:-1])/2
    axs[1, 0].plot(r_bins, np.cumsum(rho))
    # axs[1, 0].plot(r_bins, r_p.cdf(r_bins))
    # axs[0,0].plot(r_bins, r_p.pdf(r_bins))
    for k in (0,1):
        axs[k, 0].set_xlim((0, 30))
        axs[k, 0].set_xlabel('Coordinate modulus [$\\SI{}{pc}$]')
    axs[1,0].set_ylabel('Mass cdf [$M_\\odot$]')
    axs[0,0].set_ylabel('Mass pdf [$M_\\odot / \\SI{}{pc}$]')
    
    plt.show()
