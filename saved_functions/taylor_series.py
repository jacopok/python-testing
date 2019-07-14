import sympy as sp
sp.init_printing()
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

# %%
%%markdown

'''
Number of fringes observed between 0 and theta due to a "thickness" thick layer of medium
of refractive index "index" $n=1$
'''

# %%

theta = sp.symbols('theta')
index, gamma = sp.symbols('n gamma', positive=True)

N_t = sp.sign(theta) / gamma * ( 1 - index - sp.cos(theta)
                                   + sp.sqrt(index**2 - sp.sin(theta)**2))

# %%

N = sp.symbols('N')

theta_t = sp.sign(N) * sp.acos(index**2 - 1 - (gamma * sp.Abs(N) + index - 1)**2)/(2*(gamma*sp.Abs(N)+index-1))

# %%

N_t

theta_t

# %%

#sp.series(theta_t, x=N, x0=1, n=3)

sp.series(N_t, x=theta, x0=0, n=3)

# %%

x = sp.symbols('x')

sp.series(sp.sqrt(1-x), x=x, x0=0, n=4)
