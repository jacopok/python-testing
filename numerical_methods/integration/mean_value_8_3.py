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

def mean_value_integrate(f, a, b, N=int(1e6)):
    xs=uniform(a, b, size=N)
    return (np.sum(f(xs)) * (b - a) / N)

ns = np.logspace(4, 7, num=20)
f = lambda x: np.sin(1 / (x * (2 - x)))** 2
edges = (1e-10, 2-1e-10)
ints = []

for n in ns:
    i = mean_value_integrate(f, *edges, int(n))
    ints.append(i)

plt.plot(ns, ints)