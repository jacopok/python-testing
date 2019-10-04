# %%

from sympy import *
from sympy.physics.quantum import Dagger

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

# %%

P = symbols('P')

U = Matrix([[sqrt(1-P), sqrt(P)],[sqrt(P), sqrt(1-P)]])

# Trying Kraus evolution

E_0 = sqrt(1-P) * eye(2)
E_1 = sqrt(P) * Matrix([[0,1],[0,0]])
E_2 = sqrt(P) * Matrix([[0,0],[1,0]])

E = [E_0, E_1, E_2]
E= [Ei.subs(P, 1/100) for Ei in E]

# Are they Kraus matrices?

#squares = [Dagger(x)*x for x in E]
squares = [x.T*x for x in E]

sum = Matrix([[0,0],[0,0]])
for x in squares:
    sum = sum+x
print(sum)

# Define superoperator

def S(rho, E):
    evolved = zeros(*np.shape(rho))
    for x in E:
        # evolved += x * rho * Dagger(x)
        evolved += x * rho * x.T
    return(evolved)

rho = Matrix([[0,0],[0,1]])


for i in range(1000):
    rho = S(rho, E)

init_printing()
rho
