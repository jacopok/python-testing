from sympy import *

x = symbols('x')

i = integrate(exp(-x)/x, x)

print(i)
