import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

import numpy as np

from diffeq_integrators import euler, midpoint, fourth_order

ftest = lambda x, t: - x ** 3 + np.sin(t)
params = (0, 100, 0)
htest = .4

t, x_euler = euler(ftest, *params, h=htest)
t, x_midpoint = midpoint(ftest, *params,h=htest)
t, x_fourth_order = fourth_order(ftest, *params, h=htest)

# plt.plot(t, x_euler, label="Euler")
# plt.plot(t, x_midpoint, label="Midpoint")
# plt.plot(t, x_fourth_order, label="Fourth order")
# plt.ylabel('Position $x$')
# plt.legend()

tc, x_correct = fourth_order(ftest, *params, h= htest / 1000)
x_c = x_correct[::1000]
x_e = x_euler - x_c
x_m = x_midpoint - x_c
x_f = x_fourth_order - x_c
plt.plot(t, x_e, label="Euler")
plt.plot(t, x_m, label="Midpoint")
plt.plot(t, x_f, label="Fourth order")
plt.legend()
plt.yscale('symlog', linthreshy=1e-3)
plt.ylabel('Residuals $x - x_c$')

plt.xlabel('Time $t$')
plt.show()