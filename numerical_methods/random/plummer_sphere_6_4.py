import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

M = 1e4  # solar masses
a_scale = 5. # parsec
sigma_speed = 5. # km/s
N = int(1e4) #simulated stars

class plummer_rv(stats.rv_continuous):
    def __init__(self, M=M, a_scale=a_scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.M = M
        self.scale = a_scale

    def _pdf(self, r):
        scaled_r = r / self.scale
        norm = 3 * self.M / (4 * np.pi * self.scale ** 3)
        power = (1 + scaled_r**2 )**(-5/2)
        return (norm * power)

class maxwell_rv(stats.rv_continuous):
    def __init__(self, scale=sigma_speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = scale

    def _pdf(self, v):
        scaled_v = v / self.scale 
        norm = np.sqrt(2 / np.pi) * scaled_v ** 2 / self.scale 
        exp = np.exp(-scaled_v ** 2 / 2)
        return (norm * exp)
    
    # TODO: either find ppf
    # or define custom self._rvs

class sine_rv(stats.rv_continuous):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a = 0.
        self.b = np.pi

    def _pdf(self, theta):
        return (np.sin(theta) / 2)
    
    def _ppf(self, x):
        return(np.arccos(1 - 2*x))
