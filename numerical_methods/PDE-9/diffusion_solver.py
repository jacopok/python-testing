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

N_x=20
test_extremes = (273, 323)
test_state = 293 * np.ones(N_x)
test_length_step = 1 / N_x
test_diffusion_coefficient = 4.25e-2
test_times = np.arange(0, 1, 0.01)

def diffusion(times, initial_state, fixed_extremes,
    diffusion_coefficient=1., length_step = 1.):
  
  num_x=np.shape(initial_state)
  num_x_l=list(num_x)
  num_x_l[0] += 2
  num_x = tuple(num_x_l)
  num_t=np.shape(times)
  solution=np.zeros(num_t + num_x)
  solution[0, 1:-1] = initial_state
  ex1, ex2 = fixed_extremes
  solution[:, 0] = ex1
  solution[:, -1] = ex2
  
  warning_printed= False

  for i, t in enumerate(times[:-1]):
    h = times[i + 1] - t
    const = h * diffusion_coefficient / (length_step ** 2)
    if (const > 1. and not warning_printed):
      print("Warning! time step is too large")
      warning_printed=True
    space_derivative = solution[i,:-2] + solution[i, 2:] - 2 * solution[i, 1:-1]
    solution[i + 1, 1:-1] = solution[i,1:-1] + const * space_derivative

  return (solution)
  
if __name__ == "__main__":
  solution = diffusion(test_times, test_state, test_extremes, test_diffusion_coefficient, test_length_step)