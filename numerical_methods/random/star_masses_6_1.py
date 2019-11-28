import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from scipy.optimize import curve_fit

alpha = 2.3
N=int(1e7)

def m_from_x(x, alpha=2.3, m_min=0.1, m_max=150):
    N = 1 / (1 - alpha) * (m_max ** (1 - alpha) - m_min ** (1 - alpha))
    m_oneminusalpha = (m_min ** (1 - alpha) + (1 - alpha) * N * x)
    return (m_oneminusalpha ** (1 / (1 - alpha)))
    
uniform_deviates = np.random.uniform(size=N)

ms = m_from_x(uniform_deviates)

vals, bins, _ = plt.hist(ms, bins=100, log=True)

bins = np.sqrt((bins[:-1]*bins[1:]))
f = lambda x, alpha, C: C * x**(-alpha)
p, pcov = curve_fit(f, bins, vals, p0=[2, 1e6], sigma=np.sqrt(vals)/np.sqrt(max(vals)))

plt.plot(bins, vals)
plt.plot(bins, f(bins, *p))