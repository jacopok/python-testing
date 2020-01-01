import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

from diffeq_integrators import euler, midpoint, fourth_order, leapfrog_KDK, leapfrog_DKD, hermite

from functools import partial

# def remove_index(list, i):
#     return (np.append(list[:i], list[:i + 1]))
    
def norm_power(x, y, n):
    return (np.linalg.norm(x - y, ord=2)** n)

def G(positions):
    """ 
    positions should be an array of points, each of which is an array of coordinates
    """
    a = np.zeros_like(positions)

    for i, x in enumerate(positions):
        for y in np.delete(positions, i, 0):
            a[i] += (y - x) / norm_power(x, y, 3)
    return (a)

def G_mass(positions, Gmasses):
    """ 
    positions should be an array of points, each of which is an array of coordinates
    """
    a = np.zeros_like(positions)

    for i, x in enumerate(positions):
        rem = lambda k : np.delete(k, i, 0)
        for y, Gm in zip(rem(positions), rem(Gmasses)):
            a[i] += Gm * (y - x) / norm_power(x, y, 3)
    return (a)

def G_prime_mass(positions, velocities, Gmasses):
    j = np.zeros_like(positions)

    for i, (xi, vi) in enumerate(zip(positions, velocities)):
        rem = lambda k: np.delete(k, i, 0)
        for xj, vj, Gmj in zip(rem(positions), rem(velocities), rem(Gmasses)):
            xij = xi - xj
            vij = vi - vj
            j[i] -= Gmj * (
                vij / norm_power(xij, 0, 3) -    
                3. * (np.dot(xij, vij) * xij)
                / norm_power(xij, 0, 5))
    return (j)
    
Gprime = partial(G_prime_mass, Gmasses=[1.,1.])

def second_order(x, t, G=G):
    pos = x[0]
    vel = x[1]
    return(np.array([vel, G(pos)]))

if __name__ == "__main__":
    tmax = 300
    # params = (0, tmax, np.array([[[1, 1], [-1, -1]], [[-.5, 0], [0.5, 0]]]))
    params_so = (0, tmax, np.array([[1., 1.], [-1., -1.]]), np.array([[-.5, 0], [0.5, 0]]))
    h0 = .01
    plt.close()
    # ts, e_xs = euler(second_order, *params, h=h0)
    # ts, m_xs = midpoint(second_order, *params, h=2*h0)
    # ts, f_xs = fourth_order(second_order, *params, h=4*h0)
    Gp = partial(G_prime_mass, Gmasses=[1.,1.])
    ts, l_xs = leapfrog_KDK(G, *params_so, h=h0)
    ts, lD_xs=leapfrog_DKD(G, *params_so, h=h0)
    h_ts, h_xs = hermite(G, Gp, *params_so, h=h0)
    for i in range(2):
        # plt.plot(e_xs[:,0,i,0], e_xs[:,0,i,1], label="Euler")
        # plt.plot(m_xs[:,0,i,0], m_xs[:,0,i,1], label="Midpoint")
        # plt.plot(f_xs[:, 0, i, 0], f_xs[:, 0, i, 1], label="RK")
        plt.plot(l_xs[:, 0, i, 0], l_xs[:, 0, i, 1], label="Leapfrog KDK")
        plt.plot(lD_xs[:, 0, i, 0], l_xs[:, 0, i, 1], label="Leapfrog DKD")
        plt.plot(h_xs[:,0,i,0], h_xs[:,0,i,1], label="Hermite")
    plt.legend()
    plt.show()

    # tmax = 100
    # ratio = 1e-2
    # params = (0, tmax, np.array([[0, 0], [1, 0]]), np.array([[0, -ratio], [0, 1]]))
    # masses = [1, ratio]
    # h0 = .01
    # plt.close()
    # my_G = partial(G_mass, Gmasses=masses)
    # ts, xs = leapfrog_KDK(my_G, *params, h=h0)
    # plt.plot(xs[:, 0, 0, 0], xs[:, 0, 0, 1], label="M")
    # plt.plot(xs[:, 0, 1, 0], xs[:, 0, 1, 1], label="m")
    # plt.legend()
    # plt.show()