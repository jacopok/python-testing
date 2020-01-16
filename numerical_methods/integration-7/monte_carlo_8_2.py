import numpy as np
from numpy.random import uniform
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text.latex', preamble=r'''\usepackage{amsmath}
\usepackage{physics}
\usepackage{siunitx}
''')

np.random.seed(3141592)

def mc_integrate(f, a, b, vertical_edges=None, N=int(1e6)):
    
    if vertical_edges == None:
        # To generalize: we generate uniform numbers
        # in a box which is found by sampling our function
        x=np.linspace(a, b, num=int(np.sqrt(N)))
        fmax=np.max(f(x))
        fmin=np.min(f(x))
    
    else:
        fmax, fmin = vertical_edges

    count = 0
    for _ in range(N):
        xrand = uniform(a, b)
        yrand = uniform(fmin, fmax)

        under_f = bool(yrand <= f(xrand))
        under_0 = bool(yrand < 0)

        if (under_f and not under_0):
            count += 1
        if (under_0 and not under_f):
            count -= 1
    A = (b - a) * (fmax - fmin)
    return (A * count / N)

ns = np.logspace(3, 6, num=20)
topologists_sine = lambda x: np.sin(1 / (x * (2 - x)))** 2
edges = (0.,2.)
vertical_edges = (0.,1.)
ints = []

for n in ns:
    i = mc_integrate(topologists_sine, *edges, vertical_edges, int(n))
    # i = mc_integrate(np.sin, 0, 2*np.pi, int(n))
    ints.append(np.abs(i))

plt.semilogx(ns, ints)
# plt.plot(ns, 7./np.sqrt(ns))
plt.xlabel("Number of points")
plt.ylabel("Integral estimate")
plt.show()