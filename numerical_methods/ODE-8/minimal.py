import numpy as np
import matplotlib.pyplot as plt

def initialize(t0, tmax, start, h):
    ts = np.arange(t0, tmax+h, h)
    xs = np.zeros(((len(ts),) + np.shape(start)))
    xs[0] = start
    return(ts, xs)

def euler(f, t0, tmax, x0, h):
    ts, xs = initialize(t0, tmax, x0, h)

    for i, t in enumerate(ts[:-1]):
        x = xs[i]
        xs[i+1] = x + h * f(x, t)
    return (ts, xs)

def G(positions):
    """ 
    positions should be an array of points, each of which is an array of coordinates
    """
    a = np.zeros_like(positions)

    for i, x in enumerate(positions):
        for y in np.delete(positions, i, 0):
            a[i] += (y - x) / np.linalg.norm(x - y, ord=2)**3
    return (a)

def second_order(x, t, G=G):
    pos = x[0]
    vel = x[1]
    return (np.array([vel, G(pos)]))

tmax = 300
h0 = .01
params = (0, tmax, np.array([[[1, 1], [-1, -1]], [[-.5, 0], [0.5, 0]]]))
ts, xs = euler(second_order, *params, h=h0)

for i in range(2):
  plt.plot(xs[:, 0, i, 0], xs[:, 0, i, 1])
  plt.show()