# %%

import numpy as np
import sympy as sp
sp.init_printing()

# %%
x = sp.symbols('x')
f = sp.sin(x)**2 / x**2

# %%

sp.integrate(f, (x, -sp.oo, +sp.oo))

# %%

%matplotlib inline
sp.plot(f)
