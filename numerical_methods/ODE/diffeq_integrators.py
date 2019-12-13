import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

hdefault = .4

def euler(f, t0, tmax, x0, h=hdefault):
    ts = np.arange(t0, tmax, h)
    xs = np.zeros((len(ts), len(x0)))
    xs[0] = x0

    for i, t in enumerate(ts[1:]):
        x = xs[i]
        xs[i+1] = x + h * f(*x, t)
    return (ts, xs)

def midpoint(f, t0, tmax, x0, h=hdefault):
    ts = np.arange(t0, tmax, h)
    xs = np.zeros((len(ts), len(x0)))
    xs[0] = x0

    for i, t in enumerate(ts[1:]):
        x = xs[i]
        xhalf = x + h / 2. * f(*x, t)
        thalf = t + h / 2.
        xs[i+1] = x + h * f(*xhalf, thalf)
    return (ts, xs)

def fourth_order(f, t0, tmax, x0, h=hdefault):
    ts = np.arange(t0, tmax, h)
    xs = np.zeros((len(ts), len(x0)))
    xs[0] = x0

    for i, t in enumerate(ts[1:]):
        x = xs[i]
        thalf = t + h / 2.
        tnew = t + h
        k1 = h / 2. * f(*x, t)
        k2 = h / 2. * f(*(x + k1), thalf)
        k3 = h * f(*(x + k2), thalf)
        k4 = h * f(*(x + k3), tnew)
        xs[i+1] = x + (2.*k1 + 4.*k2 + 2.*k3 + k4)/6.
    return (ts, xs)

if __name__ == "__main__":
    ftest = lambda x, t: - x ** 3 + np.sin(t)
    params = (0, 100, [0])

    plt.plot(*euler(ftest, *params), label="Euler")
    plt.plot(*midpoint(ftest, *params), label="Midpoint")
    plt.plot(*fourth_order(ftest, *params), label="Fourth order")
    plt.legend()