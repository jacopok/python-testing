import sympy as sp
sp.init_printing()
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

#%%

def cooling (T, *c):
    c0, c1, c2, c3, c4 = c
    first_term = c0 * T**(+1/2) * (1 + c1 * T)
    second_term = c2 * T**(-1/2)
    third_term = c3 * (T / c4)**(-12)

    return (((first_term + second_term)**(-1) + third_term)**(-1))

#%%

T = np.logspace(3, 9, num=100)
c = [1.42e-27, 4.4e-10, 6e-22, 1e25, 1.5849e4]
c_nofirst = [0, 4.4e-10, 6e-22, 1e25, 1.5849e4]
fig = plt.figure(1)
plt.loglog(T, cooling(T, *c), label='Cooling function')
plt.xlabel('$T$ (Kelvin, log scale)')
plt.ylabel('$\\Lambda(T)$ (\SI{}{erg cm^{-3} s^{-1}, log scale)')
plt.legend()
fig.savefig('cooling_function.pdf', format = 'pdf')
