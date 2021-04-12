# %%

from sympy.physics.quantum import *
from sympy.physics.quantum.qubit import *
from sympy.physics.paulialgebra import Pauli

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

import sympy as sp
sp.init_printing()

# %%

dim = 2**2
M = sp.Matrix(np.reshape(np.ones(dim**2), (dim, dim)))
id = sp.eye(dim)
D = 1/dim * (M - 2 * id)
D

# %%md

We show the form of the operators used in the Grover algorithm
in the

$\dot z =2 $

case.

# %%

# for x in range(dim):
#     vec = np.ones(dim)
#     vec[x] -=2
#     print(D@vec)
H = 1/np.sqrt(2)* np.array([[1,1], [1,-1]])
H2 = np.kron(H, H)
sigma_x = np.array([[0,1], [1,0]])
sigma_x2 = np.kron(sigma_x, sigma_x)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
idH = np.kron(np.identity(2), H)
Dprime = sigma_x2 @ idH @ CNOT @ idH @ sigma_x2
D = H2 @ sigma_x2 @ idH @ CNOT @ idH @ sigma_x2 @ H2

# %%

print('Dprime = ', Dprime)
print('D = ', D)

# %%

sigma = [
Matrix([[0,1],[1,0]]),
Matrix([[0,I],[-I,0]]),
Matrix([[1,0],[-1,0]])]
