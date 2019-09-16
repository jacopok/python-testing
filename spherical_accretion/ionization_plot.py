import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

T = np.logspace(3, 6)

critical_temp = 1.58e5
F = 2 * T * np.exp(-critical_temp / T)

x = F / (1+F)

#%%
%matplotlib inline

fig = plt.figure(1)
plt.loglog(T, x, label = 'Collisional ionization')
plt.loglog(T, F, label = 'F')
plt.xlabel('T [K]')
plt.axvline(x=critical_temp, label=f'{critical_temp} K')
plt.legend()

plt.show()

#%%
%%markdown
Now, we plot equations $5.67a$ and $5.67b$ from the thesis.

Do note that the second one can be cast into

$$
    \rho = \rho_0 (1 + \varepsilon)
$$
and then we can just plot the expression for $\varepsilon$.

In the same vein, we will plot $p / \rho_0$.

The modified Bessel functions' ratio seems to be hard to compute.

#%%

from scipy.constants import k as k_B
from scipy.constants import m_p, m_e, c
from scipy.constants import physical_constants
E_H = physical_constants['Rydberg constant times hc in eV'][0]

from scipy.special import kn

#%%

specific_p = (1 + x) * k_B * T / m_p / c**2

fig = plt.figure(2)
plt.loglog(T, specific_p, label = '$p / \\rho_0$')
plt.xlabel('T')
plt.legend()

#%%


theta = k_B * T / m_e / c**2
k = lambda a : 1
eta = k(1/theta)

#%%

epsilon = ((3/2 * x + (eta - 1)/theta - 1) * k_B * T / m_p \
    + (1-x) * E_H / m_p)/c**2

fig = plt.figure(3)
plt.loglog(T, epsilon, label = '$\\varepsilon$')
plt.xlabel('T [K]')
plt.ylabel('$\\varepsilon$')
plt.legend()

#%%
