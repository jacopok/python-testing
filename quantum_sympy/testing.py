from sympy.physics.quantum import *
from sympy.physics.quantum.qubit import *

psi = Qubit(0)

pp = Ket('pp') # psi prime

rho = psi * psi.dual

rho_prime = TensorProduct(pp, Dagger(psi)) - TensorProduct(psi, Dagger(pp))

print(rho)
print(rho_prime)

to_trace = rho * rho_prime * rho_prime

print(to_trace)
