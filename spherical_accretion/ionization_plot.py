import numpy as np
import matplotlib.pyplot as plt

T = np.logspace(3, 8)

F = 2 * T * np.exp(-1.58e5 / T)

x = F / (1+F)

#%%

fig = plt.figure(1)
plt.loglog(T, x, label = 'Collisional ionization')
plt.xlabel('T')
plt.ylabel('x')
plt.legend()

%matplotlib qt

plt.show()
