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

def E(xs, calculate_average=True):
    Es = []
    for i,x in enumerate(xs):
        if (i == 0):
            E0 = single_E(x)
            Es.append(0)
        else: 
            Es.append(np.abs((single_E(x) - E0) / E0))
    # print(f"Starting energy: {E0}")
    if(calculate_average):
        print(f"Average energy deviation: {np.average(Es)}")
    return (Es)

def L(xs, calculate_average=True):
    Ls = []
    for i,x in enumerate(xs):
        if (i == 0):
            L0 = single_L(x)
            Ls.append(0)
        else: 
            Ls.append(np.abs((single_L(x)- L0)/L0))
    # print(f"Starting angular momentum: {L0}")
    if(calculate_average):
        print(f"Average momentum deviation: {np.average(Ls)}")
    return (Ls)
    
if __name__ == "__main__":
    tmax = 100
    params = (0, tmax, np.array([[[1., 1.], [-1., -1.]], [[-.5, 0.], [0.5, 0.]]]))
    params_so = (0, tmax, np.array([[1., 1.], [-1., - 1.]]), np.array([[-.5, 0.], [0.5, 0.]]))
    Gp = partial(G_prime_mass, Gmasses=[1.,1.])

    h0=.01
    fig, axs = plt.subplots(1, 2)
    ts, xs = euler(second_order, *params, h=h0)
    axs[0].plot(ts, E(xs), label="Euler E")
    axs[1].plot(ts, L(xs), label="Euler L")
    ts, xs = midpoint(second_order, *params, h=h0)
    axs[0].plot(ts, E(xs), label="Midpoint E")
    axs[1].plot(ts, L(xs), label="Midpoint L")
    ts, xs = fourth_order(second_order, *params, h=h0)
    axs[0].plot(ts, E(xs), label="Runge-Kutta 4 E")
    axs[1].plot(ts, L(xs), label="Runge-Kutta 4 L")
    ts, xs = leapfrog_KDK(G, *params_so, h=h0)
    axs[0].plot(ts, E(xs), label="Leapfrog KDK E")
    axs[1].plot(ts, L(xs), label="Leapfrog KDK L")
    ts, xs = leapfrog_DKD(G, *params_so, h=h0)
    axs[0].plot(ts, E(xs), label="Leapfrog DKD E")
    axs[1].plot(ts, L(xs), label="Leapfrog DKD L")
    ts, xs = hermite(G, Gp, *params_so, h=h0)
    axs[0].plot(ts, E(xs), label="Hermite E")
    axs[1].plot(ts, L(xs), label="Hermite L")
    axs[0].set_ylabel("$\\abs{(E - E_0)/E}$")
    axs[1].set_ylabel("$\\abs{(L - L_0)/L}$")
    for ax in axs:
        ax.legend()
        ax.set_xlabel("Time (arbitrary units)")