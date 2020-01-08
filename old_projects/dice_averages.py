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

def simulate_dice(x:int, y:int, z: int, N):
  """
  Plot distribution for x d y+z
  """

  results=[]
  for _ in range(N):
    single_result = z
    for _ in range(x):
      single_result += np.random.randint(1, y + 1)
    results.append(single_result)
  
  return (np.array(results))
  
def plot_dice(x: int, y: int, z: int = 0, N=int(1e5)):
  r=simulate_dice(x, y, z, N)
  m=x * y + z
  
  plt.hist(r / m,
    bins=np.linspace(0, 1, num=m + 2),
    density=True,
    alpha=.5,
    label=f"{x}d{y}+{z}")
  plt.xlabel("Fraction of total result")
  plt.ylabel("Probability density")
  plt.legend()
  plt.show()