import sympy as sp
sp.init_printing()
x = sp.symbols('x', positive=True)

f = x**3 / (sp.exp(x) - 1)

sp.integrate(f , (x, 0, sp.oo))

from mpmath import *

quad(lambda x : x**2 / (exp(x)-1), [0, inf])

#%%

g = 1/(1-x**2)

sp.diff(g)


#%%
M, r = sp.symbols('M r')

sp.series(sp.sqrt(1 - 2*M/r), x=r, x0=sp.oo)
