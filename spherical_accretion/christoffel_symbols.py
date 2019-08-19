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



print(latex(Gamma_rij.subs('c', 1).subs('G', 1)))
chris = Gamma_rij.subs('c', 1).subs('G', 1)

#%%

v = symbols('v')

gamma = 1/sqrt(1-v**2)

M = symbols('M')
x1 = symbols('r')

u = Matrix([[gamma / sqrt(1 - 2*M/x1)], [v * gamma * sqrt(1 - 2*M/x1)], [0], [0]])
simplify(u.T * chris * u)
