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
    xs = np.zeros_like(ts)
    xs[0] = x0

    for i, t in enumerate(ts[1:]):
        x = xs[i-1]
        xs[i] = x + h * f(x, t)
    return (ts, xs)

if __name__ == "__main__":
    ftest = lambda x, t: - x ** 3 + np.sin(t)
    params = (0, 100, 0)
    ts, xs = euler(ftest, *params)
    plt.plot(ts, xs)