import sympy as sp
sp.init_printing()

#%%

v = sp.symbols('v', real=True, positive=True)
gamma = 1/sp.sqrt(1 - v**2)

#%%

x = sp.sqrt(v**2 + 1/gamma**2)

sp.simplify(x)
