# %%

import sympy as sp
sp.init_printing()

# %%
x = sp.symbols('x')
f = sp.sin(x)**2 / x**2

# %%
import sympy as sp
sp.integrate(f, (x, -sp.oo, +sp.oo))
