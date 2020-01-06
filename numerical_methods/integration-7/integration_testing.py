import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text.latex', preamble=r'''\usepackage{amsmath}
\usepackage{physics}
\usepackage{siunitx}
''')

# rectangles vs trapezoids

def rectangle_integrate(f, a, b, h_frac):
    h = (b-a)*h_frac
    x = np.arange(a+h/2., b-h/2., h)
    return (np.sum(f(x)) * h)

def trapezoid_integrate(f, a, b, h_frac):
    h = (b-a)*h_frac
    edges_sum = (f(a) + f(b)) / 2.
    x = np.arange(a + h, b - h, h)
    return (h * (np.sum(f(x)) + edges_sum))
    
func = lambda x: np.exp(-x ** 2) * x ** 2

a = 0
b = 10


h_array = np.logspace(0, -4)

rect_arr = []
trap_arr = []

for h in h_array:
    rect_arr.append(rectangle_integrate(func, a, b, h))
    trap_arr.append(trapezoid_integrate(func, a, b, h))
correct_int = trap_arr[-1]

plt.plot(h_array, np.abs(rect_arr - correct_int), label="Rectangle")
plt.plot(h_array, np.abs(trap_arr - correct_int), label="Trapezoid")
plt.xlim(1, 1e-4)

plt.legend()
plt.show()