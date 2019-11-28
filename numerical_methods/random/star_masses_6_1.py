import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from scipy.optimize import curve_fit

N=int(1e7)

def m_from_x(x, alpha=2.3, m_min=0.1, m_max=150):
    N = 1 / (1 - alpha) * (m_max ** (1 - alpha) - m_min ** (1 - alpha))
    m_oneminusalpha = (m_min ** (1 - alpha) + (1 - alpha) * N * x)
    return (m_oneminusalpha ** (1 / (1 - alpha)))
    
uniform_deviates = np.random.uniform(size=N)

ms = m_from_x(uniform_deviates)
log_ms = np.log(ms)

plt.close()
vals, bins, _ = plt.hist(log_ms, bins=40)
nonzero_indices = np.nonzero(vals)
vals = vals[nonzero_indices]
bins = (bins[:-1]+bins[1:])/2
bins = bins[nonzero_indices]

f = lambda x, alpha, C : C * np.exp(-alpha*x)
p, pcov = curve_fit(f, bins, vals, p0=[2, N/10], sigma=np.sqrt(vals)/np.sqrt(max(vals)))

plt.plot(bins, vals)
plt.plot(bins, f(bins, *p))
plt.show()

from scipy import stats

class distribution(stats.rv_continuous):
    def _pdf(self, x):
        self.a = .1
        self.b = 150
        return (x ** (-2.3) / 15.348)
        # normalization computed manually

d = distribution()
masses = np.linspace(.1, 150, num=2000)
plt.plot(masses, d.cdf(masses))
x = np.linspace(0., 1., num=200)
plt.plot(m_from_x(x), x)