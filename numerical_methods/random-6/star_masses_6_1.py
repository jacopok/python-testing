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
vals, bins, _ = plt.hist(log_ms, bins=100)
# nonzero_indices = np.nonzero(grad_vals)
# grad_vals = grad_vals[nonzero_indices]
# bins = bins[nonzero_indices]
# binsizes = bins[1:] - bins[:-1]
bins = (bins[:-1]+bins[1:])/2
grad_vals = -np.gradient(vals, bins) / np.exp(bins)

f = lambda x, alpha, C : C * np.exp(-alpha*x)
p_grad, _ = curve_fit(f, bins, grad_vals, p0=[2, N / 10])
p_N, _ = curve_fit(f, bins, vals, p0=[2, N / 10])

#  sigma=np.sqrt(grad_vals)/np.sqrt(max(grad_vals))

plt.plot(bins, grad_vals)
plt.plot(bins, f(bins, *p_N))
plt.plot(bins, f(bins, *p_grad))
plt.show()

