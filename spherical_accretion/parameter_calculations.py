import sympy as sp
sp.init_printing()

#%%

v = sp.symbols('v', real=True, positive=True)
gamma = 1/sp.sqrt(1 - v**2)

#%%

x = sp.sqrt(v**2 + 1/gamma**2)

sp.simplify(x)

#%%

from mpmath import legendre
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
from mpmath import *

f = lambda x : legendre(2,x)

plot(f)

nprint(polyroots(taylor(f, 0, 2)[::-1]))
print(np.sqrt(1/3))
