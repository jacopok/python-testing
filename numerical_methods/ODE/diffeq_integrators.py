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

# def initialize(t0, tmax, x0, h):
#     ts = np.arange(t0, tmax, h)
#     xs = np.zeros((len(ts), len(x0)))
#     xs[0] = x0
#     return(ts, xs)

def initialize(t0, tmax, x0, h):
    ts = np.arange(t0, tmax, h)
    xs = np.zeros(((len(ts),) + np.shape(x0)))
    xs[0] = x0
    return(ts, xs)

# def euler(f, t0, tmax, x0, h=hdefault):
#     ts, xs = initialize(t0, tmax, x0, h)

#     for i, t in enumerate(ts[:-1]):
#         x = xs[i]
#         xs[i+1] = x + h * f(*x, t)
#     return (ts, xs)

def euler(f, t0, tmax, x0, h=hdefault):
    ts, xs = initialize(t0, tmax, x0, h)

    for i, t in enumerate(ts[:-1]):
        x = xs[i]
        xs[i+1] = x + h * f(x, t)
    return (ts, xs)

def midpoint(f, t0, tmax, x0, h=hdefault):
    ts, xs = initialize(t0, tmax, x0, h)

    for i, t in enumerate(ts[:-1]):
        x = xs[i]
        xhalf = x + h / 2. * f(x, t)
        thalf = t + h / 2.
        xs[i+1] = x + h * f(xhalf, thalf)
    return (ts, xs)

def fourth_order(f, t0, tmax, x0, h=hdefault):
    ts, xs = initialize(t0, tmax, x0, h)

    for i, t in enumerate(ts[:-1]):
        x = xs[i]
        thalf = t + h / 2.
        tnew = t + h
        k1 = h / 2. * f(x, t)
        k2 = h / 2. * f((x + k1), thalf)
        k3 = h * f(x + k2, thalf)
        k4 = h * f(x + k3, tnew)
        xs[i+1] = x + (2.*k1 + 4.*k2 + 2.*k3 + k4)/6.
    return (ts, xs)

def leapfrog_KDK(G, t0, tmax, x0, v0, h=hdefault):
    """
    To be used only with second order problems, 
    instead of a first order equation it takes
    as input the second order one, G, which should be 
    x'' = G(x, t)
    """

    ts, xs = initialize(t0, tmax, x0, h)
    _, vs = initialize(t0, tmax, v0, h)
    a_s = vs
    a_s[0] = G(xs[0])

    for i, t in enumerate(ts[:-1]):
        x = xs[i]
        v = vs[i]
        a = a_s[i]
        xs[i + 1] = x + h * v + h * h * a / 2.
        a_s[i + 1] = G(x, t)
        vs[i + 1] = v + h / 2. * (a + a_s[i + 1])
    return(ts, np.array([xs, vs]))

if __name__ == "__main__":
    ftest = lambda x, t: - x ** 3 + np.sin(t)
    params = (0, 100, 0)

    t, x_euler = euler(ftest, *params)
    t, x_midpoint = midpoint(ftest, *params)
    t, x_fourth_order = fourth_order(ftest, *params)
    tc, x_correct = fourth_order(ftest, *params, h=hdefault / 100)
    x_c = x_correct[::100]
    x_e = x_euler - x_c
    x_m = x_midpoint - x_c
    x_f = x_fourth_order - x_c
    plt.plot(t, x_e, label="Euler")
    plt.plot(t, x_m, label="Midpoint")
    plt.plot(t, x_f, label="Fourth order")
    plt.legend()
    plt.yscale('symlog', linthreshy=1e-3)