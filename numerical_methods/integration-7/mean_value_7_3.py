import numpy as np
from numpy.random import uniform
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text.latex', preamble=r'''\usepackage{amsmath}
\usepackage{physics}
\usepackage{siunitx}
''')
from scipy.integrate import quad

np.random.seed(3141592)

def mean_value_integrate(f, a, b, N=int(1e6)):
    # Easy implementation, not memory-efficient at all
    xs=uniform(a, b, size=N)
    return (np.sum(f(xs)) * (b - a) / N)

ns=np.logspace(4, 7, num=100)

# ns1=np.logspace(4, 6, num=3)
# ns2=5 * ns1
# ns = sorted(np.append(ns1, ns2))

topologists_sine = lambda x: np.sin(1 / (x * (2 - x)))** 2
edges = (0,2)
ints = []

for n in ns:
    i = mean_value_integrate(topologists_sine, *edges, int(n))
    ints.append(i)
  
# approximation, but a rather good one 
small = 1e-5
correct_value, err = quad(topologists_sine, small, 2 - small, limit=int(1e5))
correct_value += small

fig, axs = plt.subplots(1, 2)
axs[0].scatter(ns, ints)
axs[1].scatter(ns, abs(np.array(ints) - correct_value))
for ax in axs:
  ax.set_xscale('log')
  ax.set_xlabel("Number of points")
axs[0].set_ylabel("Integral estimate")
axs[1].set_ylabel("Residuals")
axs[1].set_yscale('log')
axs[1].set_ylim((1e-5, 1e-2))
plt.show()
