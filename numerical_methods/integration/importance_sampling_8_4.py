import numpy as np
from scipy import stats
from scipy import integrate
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text.latex', preamble=r'''\usepackage{amsmath}
\usepackage{physics}
\usepackage{siunitx}
''')

def IS_integrate(f, a, b, weight_pdf, weight_ppf, N=int(1e6)):
    
    class weight(stats.rv_continuous):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.a = a
            self.b = b
            self.integral = integrate.quad(weight_pdf, a, b)[0]

        def _pdf(self, x):
            return (weight_pdf(x) / self.integral)
            
        def _ppf(self, x):
            return (weight_ppf(x*self.integral))
    
    w = weight()
    xs = w.rvs(size=N)
    ws = w.pdf(xs)
    fs = f(xs)
    return (np.sum(fs / ws) / N)

f = lambda x: x ** (-1 / 2.) / (1 + np.exp(x))
edges = (0, 1)
weight_pdf = lambda x: x ** (-1 / 2.)
weight_ppf = lambda x: x ** 2 / 4. 

ns = np.logspace(4, 7, num=20)
ints = []

for n in ns:
    i = IS_integrate(f, *edges, weight_pdf, weight_ppf, int(n))
    ints.append(i)

plt.plot(ns, ints)