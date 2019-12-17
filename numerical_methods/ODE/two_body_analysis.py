from two_body_probem import *

def single_E(x):
    x1, y1, x2, y2, v1x, v1y, v2x, v2y = x
    E_kin = 1 / 2. * np.linalg.norm([v1x, v1y, v2x, v2y], ord=2)** 2
    distance_vector = [x2 - x1, y2 - y1]
    E_pot = - 1 / np.linalg.norm(distance_vector, ord=2)
    return(E_pot + E_kin)

def single_L(x):
    x1, y1, x2, y2, v1x, v1y, v2x, v2y = x
    r = [x2 - x1, y2 - y1]
    vs = [[v1x, v1y], [-v2x, -v2y]]
    Ls = []
    for v in vs:
        Ls.append(np.cross(r, v))
    L = np.average(Ls)
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
    params = (0, 100, np.array([1, 1, -1, -1, -.5, 0, .5, 0]))
    h0 = .01
    ts, xs = euler(f, *params, h=h0)
    plt.plot(ts, E(xs), label="Euler E")
    plt.plot(ts, L(xs), label="Euler L")
    ts, xs = midpoint(f, *params, h=2*h0)
    plt.plot(ts, E(xs), label="Midpoint E")
    plt.plot(ts, L(xs), label="Midpoint L")
    ts, xs = fourth_order(f, *params, h=4*h0)
    plt.plot(ts, E(xs), label="Runge-Kutta 4 E")
    plt.plot(ts, L(xs), label="Runge-Kutta 4 L")
    plt.legend()