import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use('default')
from scipy.stats import linregress
from matplotlib.ticker import LogLocator, NullFormatter
from matplotlib import rc
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

np.random.seed(3141592)

m_min = 0.1
m_max = 150.
alpha = 2.3

N = int(1e7)

def m_from_x(x, alpha, m_min, m_max):
    Norm = 1 / (1 - alpha) * (m_max ** (1 - alpha) - m_min ** (1 - alpha))
    m_oneminusalpha = (m_min ** (1 - alpha) + (1 - alpha) * Norm * x)
    return (m_oneminusalpha ** (1 / (1 - alpha)))

uniform_deviates = np.random.uniform(size=N)

ms = m_from_x(uniform_deviates, alpha, m_min, m_max)
bins = np.logspace(np.log10(m_min), np.log10(m_max), num=101)
bin_centers = (bins[:-1]+bins[1:])/2.
bin_sizes = (bins[1:]-bins[:-1])

pdf, _, _ = plt.hist(ms, density=True, bins=bins)
plt.yscale('log')
plt.ylabel('Probability density function $\\dv*{p}{M}$ [$1/M_\\odot$, logscale]')
plt.xscale('log')
plt.xlabel('Mass [$M_\\odot$, log scale]')
plt.grid('on')
plt.show()

exponent, log_const, r, p, s = linregress(np.log(bin_centers), np.log(pdf))

print(f"""The sum of the probability density samples
times the bin sizes is {np.sum(pdf*bin_sizes)}.
""")
print(f'The exponent of the powerlaw is {exponent:.2f}.')