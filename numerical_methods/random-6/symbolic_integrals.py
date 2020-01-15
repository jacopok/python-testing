import sympy as sym
sym.init_printing()

x, t = sym.symbols('x t')

f = 3 * ((1 + x ** 2)**(-sym.Rational(5, 2))) * (x ** 2)

primitive = sym.integrate(f, (x, 0, t))

