import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import random

# The equation to solve is: 
# Ldot = L wedge (I^-1 L)
# L is a 3d vector, the angular momentum
# I is the inertia tensor

I = np.array([
  [1, 0, 0],
  [0, 2, 0],
  [0, 0, 3]
])

tmax = 100
step = .01
tspan = [0,tmax]
L0 = [1e-8, 1, 0]

Iinv = np.linalg.inv(I)
def func(t, L, Iinv=Iinv):
  # dirty the ODE a bit to see what stability looks like
  return (np.cross(L, Iinv @ L) + random((3,))*1e-3 - 5e-4)

sol = solve_ivp(func, t_span=tspan, y0=L0, max_step=step)

fig = plt.figure()
ax = fig.gca(projection='3d')

omegas = Iinv @ sol.y
max_points_plotted = 10000
every = int(max(tmax / step / max_points_plotted, 1))
ax.plot(*omegas[:,::every])
# for i in range(3):
  # plt.plot(sol.t, omegas[i])

plt.tight_layout()
plt.show(block=False)
