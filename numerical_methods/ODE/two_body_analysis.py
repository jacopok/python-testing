from two_body_problem import *

def single_E(x):
    pos = x[0]
    vel = x[1]
    E_kin = 1 / 2. * np.linalg.norm(vel, ord=2)** 2
    E_pot = 0
    for i, p in enumerate(pos):
        for y in np.delete(pos, i, 0):
            E_pot -= 1 / 2./ np.linalg.norm(p-y, ord=2)
    return(E_pot + E_kin)

def single_L(x):
    pos = x[0]
    vel = x[1]
    center = np.average(pos, axis=0)
    L=0
    for p, v in zip(pos, vel):
        r = p - center
        L+= np.cross(r, v)
    return(L)

def E(xs):
    Es = []
    for i,x in enumerate(xs):
        if (i == 0):
            E0 = single_E(x)
            Es.append(0)
        else: 
            Es.append(np.abs(single_E(x)- E0))
    return (Es)

def L(xs):
    Ls = []
    for i,x in enumerate(xs):
        if (i == 0):
            L0 = single_L(x)
            Ls.append(0)
        else: 
            Ls.append(np.abs(single_L(x)- L0))
    return (Ls)
    
if __name__ == "__main__":
    tmax = 100
    params = (0, tmax, np.array([[[1, 1], [-1, -1]], [[-.5, 0], [0.5, 0]]]))
    params_leapfrog = (0, tmax, np.array([[1, 1], [-1, -1]]), np.array([[-.5, 0], [0.5, 0]]))

    h0 = .01
    ts, xs = euler(second_order, *params, h=h0)
    plt.plot(ts, E(xs), label="Euler E")
    plt.plot(ts, L(xs), label="Euler L")
    ts, xs = midpoint(second_order, *params, h=2*h0)
    plt.plot(ts, E(xs), label="Midpoint E")
    plt.plot(ts, L(xs), label="Midpoint L")
    ts, xs = fourth_order(second_order, *params, h=4*h0)
    plt.plot(ts, E(xs), label="Runge-Kutta 4 E")
    plt.plot(ts, L(xs), label="Runge-Kutta 4 L")
    ts, xs = leapfrog_KDK(G, *params_leapfrog, h=2*h0)
    plt.plot(ts, E(xs), label="Leapfrog KDK E")
    plt.plot(ts, L(xs), label="Leapfrog KDK L")
    plt.xlabel("Time (arbitrary units)")
    plt.ylabel("$\\abs{E - E_0}/E$ and $\\abs{L - L_0}/L$")
    plt.legend()