from sympy import *

k = symbols('k')
M, m, a = symbols('M m a', real=True)

value = 1

u = 2 * k / M * (E**(k*a) -1)
v = k / m * (E**(k*a) + E**(-k*a) -2)


sol = solve(Eq(u**2, v**2))
x = symbols('x', real=True)

k_arr = []
for i in range(2):
    k_arr.append(solve(Eq(sol[i][M], M).subs(M, m/x).subs(a, value), k))

t = k_arr[0][0]
omega_square = - u.subs(a, value).subs(k, t).subs(M, value)

plot(re(t),-im(t))
plot(re(omega_square), im(omega_square))
