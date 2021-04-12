import sympy as sp
sp.init_printing()
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

# %%

x = sp.symbols('x')

sp.series(sp.log(1-x))

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

print(sp.latex(sp.series(N_t, x=theta, x0=0, n=5)))

# %%

x = sp.symbols('x')

sp.series(sp.sqrt(1-x), x=x, x0=0, n=4)

# %%

i = 1.336
g = 2.689e-5
print((i-1)/2/g/i)

# %%

%matplotlib qt
sp.plot_implicit(sp.Eq((index-1)/gamma/index/2, 5000), (index, 1, 2), (gamma, 2e-5, 4e-5))
w
