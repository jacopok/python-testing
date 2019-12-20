import numpy as np
from diffeq_integrators import euler
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

def grav(y, t):
    return (np.array([y[1], -9.81]))

N = int(1e3)
eps = 1e-3
x0=np.array([0.,1.])
params=(0, 3)
h0=.1
rate = 20.

ts, xs=euler(grav, 0, 3, x0, h=h0)

def cost_function(x_vec, final_pos=0):
    return ((x_vec[-1][0] - final_pos)** 2)

iterations=0
while (cost_function(xs) > 1e-3):
    ts, xs = euler(grav, *params, x0, h=h0)
    ts_eps, xs_eps = euler(grav, *params, x0 + eps, h=h0)
    plt.plot(ts, xs)
    grad_cost = cost_function(xs_eps) - cost_function(xs)

    x0 += np.array([0., - rate * grad_cost])
    iterations += 1
print(f"Reached convergence in {iterations} iterations.")