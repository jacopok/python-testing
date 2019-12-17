import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import cm

ITMAX = int(2e11)

def iterate(z, c):
    return(z**2 + c)

def convergence(c, eps=1e-6):

    iterations = 0
    z = 0
    while True:
        z = iterate(z, c)
        if (np.abs(z) > 2):
            return(iterations)
        if (iterations>ITMAX):
            return(-1)
        iterations += 1

def generate_set(*args, N=int(1e3)):
    x, y, r = args
    xs = np.linspace(x-r, x+r, num=N)
    ys = np.linspace(y-r, y+r, num=N)

    cs = np.zeros((N, N))

    for i, x in tqdm(enumerate(xs)):
        for j, y in enumerate(ys):
            c = complex(x, y)
            cs[j, i] = convergence(c)
    
    return(xs, ys, cs)

def plot(xs, ys, cs):
    X, Y = np.meshgrid(xs, ys)
    plt.close()
    colors = plt.contourf(X, Y, cs, cmap = cm.plasma)
    plt.colorbar(colors)