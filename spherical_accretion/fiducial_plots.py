import numpy as np

r = 4

v = 0.5

def get_vectors(v, r, M=1/2):
    gamma = 1 / np.sqrt(1-v**2)
    y = gamma * np.sqrt(1 - 2 * M / r)
    e_t = [-y*v, gamma**2 / y]
    e_r = [y, -v*gamma**2 / y]

    return(e_t, e_r)

#%%
%%markdown

I  will return vectors as $(r, t)$ instead of $(t, r)$ since that is most intuitive
for a spacetime diagram.

#%%

def norm(vec, M, r):
    g_00 = - (1 - 2 * M / r)
    g_11 = - 1/g_00
    return(vec[0]**2 * g_00 + vec[1]**2 * g_11)

#%%

import matplotlib.pyplot as plt
plt.style.use('seaborn')
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

v=0.5
r=1.3

e_t, e_r = get_vectors(v=v, r=r)
e_t_schw, e_r_schw = [0,1], [1,0]

origin = [0], [0]

from itertools import cycle
colors = cycle(('firebrick', 'navy', 'lightcoral', 'cornflowerblue'))
x_coords =[]
y_coords =[]

def plot_vector(vec, name):
    plt.quiver(
        *origin,
        *vec,
        color=next(colors),
        scale_units='xy',
        angles='xy',
        scale = 1,
        label=name)
    x_coords.append(vec[0])
    y_coords.append(vec[1])
    return(None)

plt.figure()
plot_vector(e_t, 'fiducial $e_t$')
plot_vector(e_r, 'fiducial $e_r$')
plot_vector(e_t_schw, 'coordinate $e_t$')
plot_vector(e_r_schw, 'coordinate $e_r$')


max_x = np.max(x_coords)
max_y = np.max(y_coords)
min_x = np.min(x_coords)
min_y = np.min(y_coords)

avg_minmax = np.average(np.abs([max_x, max_y, min_x, min_y]))*0.2

plt.xlim(min_x-avg_minmax, max_x+avg_minmax)
plt.ylim(min_y-avg_minmax, max_y+avg_minmax)
plt.xlabel('Coordinate radius $r$')
plt.ylabel('Coordinate time $t$')
title = f'$v = {v}$, $r/2M = {r}$'
figtitle = f'{v}_{r}'
plt.title(title)
plt.legend()
plt.savefig(figtitle+'.pdf', format = 'pdf')

#%%
