import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from functools import partial
from tqdm import tqdm

from two_body_problem import G_prime_mass, second_order, G
from diffeq_integrators import euler, midpoint, fourth_order, leapfrog_KDK, leapfrog_DKD, hermite


def single_E(x, masses=None):
    pos = x[0]
    vel = x[1]
    if masses is None:
        masses = np.ones_like(vel[:,0])

    E_kin = 0.
    for v, p in zip(vel, vel*masses[:,np.newaxis]):
        E_kin += 1./2. * np.dot(v, p)
    
    E_pot = 0.
    for i, (p, m1) in enumerate(zip(pos, masses)):
        for y, m2 in zip(np.delete(pos, i, 0), np.delete(masses, i, 0)):
            E_pot -= 1 / 2./ np.linalg.norm(p - y, ord=2) * m1 * m2

    return(E_pot + E_kin)

def single_L(x, masses=None):
    pos = x[0]
    if masses is not None:
        vel = x[1] * masses[:, np.newaxis]
    else:
        vel = x[1]
    center = np.average(pos, axis=0)
    L=0
    for p, v in zip(pos, vel):
        r = p - center
        L+= np.cross(r, v)
    return(L)

def E(xs,masses=None, calculate_average=True):
    E0 = single_E(xs[0], masses)

    Es = []
    for i,x in tqdm(enumerate(xs[1:]), desc="E deviation: ", total=np.shape(xs[1:])[0]):
        Es.append(np.abs((single_E(x, masses) - E0) / E0))
        # Es.append((single_E(x, masses) - E0) / E0)
    # print(f"Starting energy: {E0}")
    if(calculate_average):
        print(f"Average energy deviation: {np.average(Es)}")
    return (Es)

def L(xs, masses=None, calculate_average=True):
    L0 = single_L(xs[0], masses)
    Ls = []
    for i,x in tqdm(enumerate(xs[1:]), desc="L deviation: ", total=np.shape(xs[1:])[0]):
        Ls.append(np.abs((single_L(x, masses)- L0)/L0))
    # print(f"Starting angular momentum: {L0}")
    if(calculate_average):
        print(f"Average momentum deviation: {np.average(Ls)}")
    return (np.array(Ls))
    
if __name__ == "__main__":
    tmax = 100
    params = (0, tmax, np.array([[[1., 1.], [-1., -1.]], [[-.5, 0.], [0.5, 0.]]]))
    params_so = (0, tmax, np.array([[1., 1.], [-1., - 1.]]), np.array([[-.5, 0.], [0.5, 0.]]))
    Gp = partial(G_prime_mass, Gmasses=[1.,1.])

    h0=.01
    fig, axs = plt.subplots(1, 2)
    ts, xs = euler(second_order, *params, h=h0)
    axs[0].plot(ts[1:], E(xs), label="Euler E")
    axs[1].plot(ts[1:], L(xs), label="Euler L")
    ts, xs = midpoint(second_order, *params, h=h0)
    axs[0].plot(ts[1:], E(xs), label="Midpoint E")
    axs[1].plot(ts[1:], L(xs), label="Midpoint L")
    ts, xs = fourth_order(second_order, *params, h=h0)
    axs[0].plot(ts[1:], E(xs), label="Runge-Kutta 4 E")
    axs[1].plot(ts[1:], L(xs), label="Runge-Kutta 4 L")
    ts, xs = leapfrog_KDK(G, *params_so, h=h0)
    axs[0].plot(ts[1:], E(xs), label="Leapfrog KDK E")
    axs[1].plot(ts[1:], L(xs), label="Leapfrog KDK L")
    ts, xs = leapfrog_DKD(G, *params_so, h=h0)
    axs[0].plot(ts[1:], E(xs), label="Leapfrog DKD E")
    axs[1].plot(ts[1:], L(xs), label="Leapfrog DKD L")
    ts, xs = hermite(G, Gp, *params_so, h=h0)
    axs[0].plot(ts[1:], E(xs), label="Hermite E")
    axs[1].plot(ts[1:], L(xs), label="Hermite L")
    axs[0].set_ylabel("$\\abs{(E - E_0)/E}$")
    axs[1].set_ylabel("$\\abs{(L - L_0)/L}$")
    for ax in axs:
        ax.legend()
        ax.set_xlabel("Time (arbitrary units)")
        ax.set_yscale("log")
    plt.show()