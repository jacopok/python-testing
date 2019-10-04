from sympy import *

M = 4.6637e-26

K1, K2 = symbols('K1 K2', real=True, positive=True)

Cn =  2*pi*15.3e12
Dn = 2*15.857e12

C, D = symbols('C D', real=True, positive=True)

eq1 = Eq(sqrt(2*(K1+K2)/M), C)
eq2 = Eq(sqrt((K1*K2)/(2*M*(K1+K2))), D)

sol1 = solve(eq1, K2)

solution = solve(eq2.subs(K2, sol1[0]), K1)
