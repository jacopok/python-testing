import numpy as np
from diffeq_integrators import euler
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

def grav(y, t):
    return (np.array([y[1], -9.81]))

def cost_function(x_vec, final_pos=10):
    return ((x_vec[-1][0] - final_pos)** 2)

# GRADIENT DESCENT IMPLEMENTATION

def shooting_gd(diffeq, diffeq_params, diffeq_h0, guess,
    cost_function, eps=1e-3, threshold=1e-5, rate=20., integrator=euler, plot=False):

    x0 = guess
    ts, xs = integrator(diffeq, *diffeq_params, x0, h=diffeq_h0)

    iterations=0
    while (cost_function(xs) > threshold):
        ts, xs = euler(grav, *diffeq_params, x0, h=diffeq_h0)
        _, xs_eps = euler(grav, *diffeq_params, x0 + eps, h=diffeq_h0)

        grad_cost = cost_function(xs_eps) - cost_function(xs)

        if (plot):
            lab=None
            if (iterations % 3 == 0):
                lab=f"v0 = {x0[1]:.2f}, cost= {cost_function(xs):.2e}"
            plt.plot(xs[:,0], label=lab)

        x0 += np.array([0., - rate * grad_cost])
        iterations += 1
    
    if (plot):
        plt.legend()
        plt.xlabel('$x$ coordinate')
        plt.ylabel('$y$ coordinate')
        plt.show()

    print(f"Reached convergence in {iterations} iterations.")
    
    return (x0, ts, xs)
    
if __name__ == "__main__":
    x0=np.array([0.,1.])
    params=(0., 3.)
    h0=.1

    x0, ts, xs = shooting_gd(grav, params, h0, x0, cost_function, plot=True)
    
