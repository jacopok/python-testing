import numpy as np
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

"""
A = a/GM
L = l/GM
R = r/2GM
"""

def L(A, e, pm):
    return(np.sqrt(3) + pm * np.sqrt((np.sqrt(3)-A*e)**2 - A**2))
def R(L, A, e, pm):
    b2 = (L ** 2 - A ** 2 * (e ** 2 - 1)) / 2.
    return (2*(b2 + pm * np.sqrt(b2 ** 2 - 12 * (L - A * e)** 2)))
    
As = np.linspace(-1, 1, num=400)

plt.close()
ax = plt.gca()
for e in range(5):
    Ls = L(As, e, 1)
    color = next(ax._get_lines.prop_cycler)['color']
    # plt.plot(As, Ls, label=f"$L$ for $e = $ {e}", color=color)
    Rs = R(Ls, As, e, 1)
    plt.plot(As, Rs, label=f"$R$ for $e = $ {e}", color=color)
plt.xlabel("$A = a/ GM$")
plt.ylabel("$L_+$")
plt.legend()
