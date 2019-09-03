import sympy as sp
sp.init_printing()

a0, a1 = sp.symbols('a0 a1', real=True)
gamma, x = sp.symbols('gamma x', real=True)
v = sp.sqrt(1 - 1/ gamma**2)
y = gamma * x

#%%

eq1 = sp.Eq(y**2 * a0 + v* gamma**2 * a1)
eq2 = sp.Eq(a0**2 *(-y**2 / gamma**2) + a1**2 * (gamma**2 / y**2), 1)

sp.solve([eq1, eq2], a0, a1)
