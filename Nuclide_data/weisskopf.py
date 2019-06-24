import matplotlib.pyplot as plt
plt.style.use('seaborn')
import numpy as np

from scipy.constants import fine_structure, c

def fack(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fack(n-2)

omegas = 10**(np.linspace(19, 21))
R = 4e-15 # typical nuclear radius

for L in range(1,5):
    f = lambda o : 2*fine_structure*(L+1)/L/fack(L)**2 * (o/c)**(2*L+1) *(3/(3+L))**2*R**(2*L)
    plt.plot(omegas, f(omegas))
    plt.plot(omegas, f(omegas)*0.31*100**(-2/3), ls='--')
plt.show()
