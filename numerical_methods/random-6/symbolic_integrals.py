import sympy as sp
sp.init_printing()

x, t = sp.symbols('x t')

f = 3 * ((1 + x ** 2)**(-sp.Rational(5, 2))) * (x ** 2)

primitive = sp.integrate(f, (x, 0, t))

