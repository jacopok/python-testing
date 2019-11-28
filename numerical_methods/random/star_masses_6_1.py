import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from scipy.optimize import curve_fit

N=int(1e7)

def m_from_x(x, alpha=3.3, m_min=0.1, m_max=150):
    N = 1 / (1 - alpha) * (m_max ** (1 - alpha) - m_min ** (1 - alpha))
    m_oneminusalpha = (m_min ** (1 - alpha) + (1 - alpha) * N * x)
    return (m_oneminusalpha ** (1 / (1 - alpha)))
    
uniform_deviates = np.random.uniform(size=N)

ms = m_from_x(uniform_deviates)
log_ms = np.log(ms)

vals, bins, _ = plt.hist(log_ms, bins=100)
vals = vals+0.1

bins = (bins[:-1]+bins[1:])/2
f = lambda x, alpha, C : C * np.exp(-alpha*x)
p, pcov = curve_fit(f, bins, vals, p0=[2, N/10], sigma=np.sqrt(vals)/np.sqrt(max(vals)))

plt.plot(bins, vals)
plt.plot(bins, f(bins, *p))