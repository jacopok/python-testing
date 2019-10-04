import sympy as sy
import numpy as np
import matplotlib.pyplot as plt

gamma = 1
deltam = 1

t = sy.symbols('t')

delta = sy.E**(-gamma * t) * sy.cos(deltam * t)
delta_t = sy.lambdify(t, delta, 'numpy')

times = np.linspace(0, 15, num=500)

curve = delta_t(times)


plt.plot(times, curve, label = 'delta')
plt.yscale('symlog', linthreshy=1e-6)
plt.show()
