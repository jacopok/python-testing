import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import cm

ITMAX = int(1e3)

def iterate(z, c):
    return(z**2 + c)

def convergence_mandelbrot(c, eps=1e-6):

    iterations = 0
    z = 0
    while True:
        z = iterate(z, c)
        if (np.abs(z) > 2):
            return(iterations)
        if (iterations>ITMAX):
            return(-1)
        iterations += 1

def convergence_julia(z0, c, rmax, eps=1e-5):

    iterations = 0
    z=z0
    while True:
        oldz = z
        z = iterate(z, c)
        if (np.abs(z) > rmax):
            return(iterations)
        if (iterations>ITMAX):
            return (-1)
        if (np.abs(z - oldz) < eps):
            return (-1)
        iterations += 1

def generate_set(*args,
        N=int(1e2),
        ccheck = convergence_mandelbrot,
        **ccheck_args):
    x1, x2, y1, y2 = args
    xs = np.linspace(x1, x2, num=N)
    ys = np.linspace(y1, y2, num=N)

    cs = np.zeros((N, N))

    for i, x in tqdm(enumerate(xs)):
        for j, y in enumerate(ys):
            c = complex(x, y)
            cs[j, i] = ccheck(c, **ccheck_args)
    
    return(xs, ys, cs)

def plot(xs, ys, cs, color='plasma'):
    X, Y = np.meshgrid(xs, ys)
    plt.close()
    colors = plt.contourf(X, Y, cs, cmap = plt.get_cmap('plasma'))
    plt.colorbar(colors)

def rc(c):
    rmax = 1/2. + np.sqrt(1/4. + np.abs(c))
    return({'c':c, 'rmax':rmax}) 