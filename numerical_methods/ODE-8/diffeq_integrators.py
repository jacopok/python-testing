import numpy as np
from tqdm import tqdm

hdefault = .01

def initialize(t0, tmax, start, h=hdefault):
    # Returns arrays filled with the initial conditions 
    # and then zero, of the right shape

    ts = np.arange(t0, tmax+h, h)
    xs = np.zeros(((len(ts),) + np.shape(start)))
    xs[0] = start
    return (ts, xs)
    
####
#### FIRST ORDER ODE SOLVERS
####

def euler(f, t0, tmax, x0, h=hdefault):
    ts, xs = initialize(t0, tmax, x0, h)

    for i, t in tqdm(enumerate(ts[:-1]), total=int((tmax-t0)/h), desc = "Euler"):
        x = xs[i]
        xs[i+1] = x + h * f(x, t)
    return (ts, xs)

def midpoint(f, t0, tmax, x0, h=hdefault):
    ts, xs = initialize(t0, tmax, x0, h)

    for i, t in tqdm(enumerate(ts[:-1]), total=int((tmax-t0)/h), desc = "Midpoint"):
        x = xs[i]
        xhalf = x + h / 2. * f(x, t)
        thalf = t + h / 2.
        xs[i+1] = x + h * f(xhalf, thalf)
    return (ts, xs)

def fourth_order(f, t0, tmax, x0, h=hdefault):
    ts, xs = initialize(t0, tmax, x0, h)

    for i, t in tqdm(enumerate(ts[:-1]), total=int((tmax-t0)/h), desc = "Fourth order RK"):
        x = xs[i]
        thalf = t + h / 2.
        tnew = t + h
        k1 = h / 2. * f(x, t)
        k2 = h / 2. * f((x + k1), thalf)
        k3 = h * f(x + k2, thalf)
        k4 = h * f(x + k3, tnew)
        xs[i+1] = x + (2.*k1 + 4.*k2 + 2.*k3 + k4)/6.
    return (ts, xs)

#### 
#### SECOND ORDER ODE SOLVERS
#### 

def leapfrog_KDK(G, t0, tmax, x0, v0, h=hdefault):
    """
    To be used only with second order problems, 
    instead of a first order equation it takes
    as input the second order one, G, which should be 
    x'' = G(x, t)
    """

    ts, xs = initialize(t0, tmax, x0, h)
    _, vs = initialize(t0, tmax, v0, h)
    _, a_s = initialize(t0, tmax, G(xs[0]), h)

    for i, _ in tqdm(enumerate(ts[:-1]), total=int((tmax-t0)/h), desc="Leapfrog KDK"):
        x = xs[i]
        v = vs[i]
        a = a_s[i]
        xs[i + 1] = x + h * v + h * h * a / 2.
        a_s[i + 1] = G(xs[i+1])
        vs[i + 1] = v + h / 2. * (a + a_s[i + 1])
    return (ts, np.stack((xs, vs), axis=1))

def leapfrog_DKD(G, t0, tmax, x0, v0, h=hdefault):
    """
    To be used only with second order problems, 
    instead of a first order equation it takes
    as input the second order one, G, which should be 
    x'' = G(x, t)
    """

    ts, xs = initialize(t0, tmax, x0, h)
    _, vs = initialize(t0, tmax, v0, h)

    for i, _ in tqdm(enumerate(ts[:-1]), total=int((tmax-t0)/h), desc = "Leapfrog DKD"):
        x = xs[i]
        v = vs[i]
        xhalf = x + h * v /2.
        ahalf = G(xhalf)
        vs[i + 1] = v + h * ahalf
        xs[i + 1] = x + h * v + h * h / 2. * ahalf
    return(ts, np.stack((xs, vs), axis=1))

def hermite(G, Gprime, t0, tmax, x0, v0, h=hdefault):
    """
    To be used only with second order problems, 
    instead of a first order equation it takes
    as input the second order one, G, which should be 
    x'' = G(x, t)
    This algorithm also requires as input the derivative 
    of the second-order function G: 
    Gprime = dG/dt (x, v, t)
    """
    ts, xs = initialize(t0, tmax, x0, h)
    _, vs = initialize(t0, tmax, v0, h)
    _, a_s = initialize(t0, tmax, G(x0), h) # "as" is a keyword... 
    _, js = initialize(t0, tmax, Gprime(x0, v0), h)

    for i, _ in tqdm(enumerate(ts[:-1]), total=int((tmax-t0)/h), desc = "Hermite"):
        x = xs[i]
        v = vs[i]
        a = a_s[i]
        j = js[i]
        
        xp = x \
            + h * v \
            + h**2 * a / 2. \
            + h**3 * j / 6.
        vp = v \
            + h * a \
            + h**2 * j / 2.
        ap = G(xp)
        jp = Gprime(xp, vp)

        vs[i + 1] = v \
            + h * (a + ap) / 2. \
            + h * h * (j - jp) / 12.
        xs[i + 1] = x \
            + h * (v + vs[i + 1]) / 2. \
            + h * h * (a - ap) / 12.
        a_s[i + 1] = G(xs[i + 1])
        js[i + 1] = Gprime(xs[i + 1], vs[i + 1])
        
    return (ts, np.stack((xs, vs), axis=1))
