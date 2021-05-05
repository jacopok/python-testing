import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import cm
from multiprocessing import Pool
from numba import njit


ITMAX = int(2e2)
EPS_MANDELBROT = 1e-6
EPS_JULIA = 1e-5


@njit
def iterate(z, c):
    return (z**2 + c)


@njit
def convergence_mandelbrot(c, eps=EPS_MANDELBROT, itmax=ITMAX):

    iterations = 0
    z = 0
    while True:
        z = iterate(z, c)
        if (np.abs(z) > 2):
            return (iterations)
        if (iterations > itmax):
            return (-1)
        iterations += 1


@njit
def convm(xy):
    x, y = xy
    return(convergence_mandelbrot(x + 1j * y))


def convergence_julia(z0, c, rmax, eps=EPS_JULIA, itmax=ITMAX):

    iterations = 0
    z = z0
    while True:
        oldz = z
        z = iterate(z, c)
        if (np.abs(z) > rmax):
            return (iterations)
        if (iterations > itmax):
            return (-1)
        if (np.abs(z - oldz) < eps):
            return (-1)
        iterations += 1


def generate_set(x1, x2, y1, y2,
                 N=int(1e2),
                 ccheck=convergence_mandelbrot,
                 **ccheck_args):
    """
    Good values: -2., .5, -1.2, 1.2 for Mandelbrot.
    For Julia it depends.
    """                 

    xs = np.linspace(x1, x2, num=N)
    ys = np.linspace(y1, y2, num=N)

    cs = np.zeros((N, N))

    # p = Pool(4)

    def process_row(args):
        i, x = args
        for j, y in enumerate(ys):
            c = complex(x, y)
            cs[j, i] = ccheck(c, **ccheck_args)

    for i, x in tqdm(enumerate(xs)):
        process_row((i, x))

    # p.map(process_row, list(enumerate(xs)))

    return (xs, ys, cs)


def plot(xs, ys, cs, color='CMRmap'):
    X, Y = np.meshgrid(xs, ys)
    plt.close()
    plt.contourf(X, Y, cs, cmap=plt.get_cmap(color), levels=40)
    # plt.colorbar(colors)
    plt.axis('off')
    plt.tight_layout()


def rc(c):
    rmax = 1 / 2. + np.sqrt(1 / 4. + np.abs(c))
    return ({'c': c, 'rmax': rmax})
