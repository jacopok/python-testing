import sympy as sp
sp.init_printing()
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

#%%

c = [1.42e-27, 4.4e-10, 6e-22, 1e25, 1.5849e4]


def cooling (T, *c):
    c0, c1, c2, c3, c4 = c
    first_term = c0 * T**(-1/2) * (1 + c1 * T)
    second_term = c2 * T**(-1/2)
    third_term = c3 * (T / c4)**(-12)

    return (((first_term + second_term)**(-1) + third_term)**(-1))

#%%

T = np.logspace(4, 7, num=200)
y = cooling(T, *c)
%matplotlib qt
plt.plot(T, y)
