# %%

import sympy as sp

x3, y3, z3, x2, y2, z2 = sp.symbols('x3 y3 z3 x2 y2 z2', real=True)
E, Em = sp.symbols('E Em', real=True, positive=True)

# %%

eq1 = sp.Eq(E + z2 + z3, 0)
eq2 = sp.Eq(Em, E + sp.sqrt(x3 ** 2 + y3 ** 2 + z3 ** 2) + sp.sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2))

# %%

sols = sp.solve([eq1, eq2], [z2, z3])

# %%

vect = sp.Matrix([E,
    x2, y2, sp.simplify(sols[0][0].subs(x3, -x2).subs(y3, -y2)),
    -x2, -y2, sp.simplify(sols[0][1].subs(x3, -x2).subs(y3, -y2)),
    ])
coords = [E, x2, y2]

# %%

J = vect.jacobian(coords)

probability_element = sp.simplify(sp.sqrt(sp.Abs((J.T * J).det())))

# %%

import numpy as np

Emax = 1
numerical_prob = sp.lambdify([E, x2, y2], probability_element.subs(Em, Emax), "numpy")

# %%

num = 20
E_arr = np.linspace(0, Emax / 2, num=num)
x2_arr = np.linspace(-Emax / 2, Emax / 2, num=num)
y2_arr = np.linspace(-Emax / 2, Emax / 2, num=num)

# %%

Edist = []
sum=0
for E in E_arr:
    for x2 in x2_arr:
        for y2 in y2_arr:
            sum += numerical_prob(E, x2, y2)
    Edist.append(sum)
    sum=0

# %%

import matplotlib.pyplot as plt
plt.style.use('seaborn')

plt.plot(E_arr, Edist)
import math
integral = np.sum([E for E in Edist if not math.isnan(E)]) / num**3
# %%
