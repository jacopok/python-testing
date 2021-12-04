# %%

import numpy as np
from tqdm import tqdm
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.ticker import FuncFormatter, MultipleLocator

bs = np.linspace(5.195, 5.199, num=30)
norm = Normalize(min(bs), max(bs))
cmap = plt.get_cmap('inferno')

infinity = 1e4


def ode(t, uv):

    u, v = uv

    return [v, - u + 3 * u**2]


def cross_horizon(t, uv):
    return uv[0] - 2


cross_horizon.terminal = True


def reach_infinity(t, uv):
    return uv[0] - 1/infinity


reach_infinity.terminal = True
reach_infinity.direction = -1


for b in bs:
    sol = solve_ivp(
        ode,
        t_span=(0, 4 * np.pi),
        y0=[1e-6, 1/b],
        events=[cross_horizon, reach_infinity],
        max_step=.001,
        )

    plt.semilogy(sol.t, 1/sol.y[0], c=cmap(norm(b)))
    plt.ylim(2, infinity/10)
    
    if sol.status == 1:
        if phi := sol.t_events[0]:
            print(f'{b=:.3f}GM, crossed horizon at phi={phi[0]/np.pi:.3f}pi')

        if phi := sol.t_events[1]:
            print(f'{b=:.3f}GM, reached infinity at phi={phi[0]/np.pi:.3f}pi')
            print(f'Minimum radius: {1/ max(sol.y[0]):.3f}GM')
    
    # if ch.any():

    # if ri.any():
    #     print(f'{b=}, reached infinity at phase {1/ri[0][1]}')
    
plt.colorbar(
    ScalarMappable(norm=norm, cmap=cmap),
    label='Impact parameter [units of $GM$]')
plt.xlabel('Angle [rad]')
plt.ylabel('Radius [units of $GM$]')
plt.gca().xaxis.set_major_formatter(FuncFormatter(
   lambda val, pos: '{:.0g}$\pi$'.format(val/np.pi) if val != 0 else '0'
))

plt.gca().xaxis.set_major_locator(MultipleLocator(base=np.pi))

plt.savefig('photon_deflection.png', transparency=False, facecolor="white", dpi=200)

# %%
