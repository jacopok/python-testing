import sys
sys.path.append('/home/jacopo/spacetimeengine')

from spacetimeengine import *

#%%


schwarzschild_spacetime = SpaceTime(Solution().schwarzschild(), suppress_printing = True)

#%%

Gamma_rij = eye(4)

for i in range(4):
    for j in range(4):
        Gamma_rij[i,j] = schwarzschild_spacetime.get_connection_coefficient("udd", 1, i, j)


chris = Gamma_rij.subs('c', 1).subs('G', 1)
chris = simplify(chris)
print(latex(chris))


#%%

v = Function('v', positive=True, real=True)(x1)

gamma = 1/sqrt(1-v**2)
y = gamma * sqrt(1 - 2 * M / x1)

M = symbols('M')
x1 = symbols('r')

u = Matrix([[gamma / sqrt(1 - 2*M/x1)], [v * gamma * sqrt(1 - 2*M/x1)], [0], [0]])

#%%

simplify(diff(u[1], x1))

#%%

a = diff(u[1], x1) * y * v + simplify(u.T * chris * u)[0]

a = simplify(collect(simplify(factor(a)), diff(v, x1)))

a_th = y**2 * (gamma**2 * v * diff(v, x1) + M / (1- 2 * M / x1) / x1**2)

print(a.equals(a_th))

#%%

dlog = diff(log(y), x1)
dlog

#%%

term1 = a / y**2

term2 = diff(log(y), x1)

simplify(term1-term2)
