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

# N_x=20
# test_extremes = (273, 323)
# test_state = 293 * np.ones(N_x)
# test_length_step = 1 / N_x
# test_diffusion_coefficient = 4.25e-2
# test_times = np.arange(0, 1, 0.01)

def diffusion(times, initial_state, fixed_extremes,
    diffusion_coefficient=1., length_step=1.):
  """
  Solves the 1D diffusion equation:

  du/dt = diffusion_coefficient * [d^2 u / dx^2]

  Inputs:
  times: array of the times between which the evolution is calculated
  initial_state: initial condition of the function
  fixed_extremes: boundary terms, will be held at constant values throughout the evolution
  diffusion_coefficient: the term in the equation
  """
  
  # just some gymnastics needed in order to 
  # modify the value in a tuple
  num_x=np.shape(initial_state)
  num_x_l=list(num_x)
  num_x_l[0] += 2
  num_x = tuple(num_x_l)
  num_t=np.shape(times)

  # creating the 2d array for the solution
  # note that tuple addition means appending one to the other
  solution=np.zeros(num_t + num_x)

  # fixing boundary conditions
  solution[0, 1:-1] = initial_state
  ex1, ex2 = fixed_extremes
  solution[:, 0] = ex1
  solution[:, -1] = ex2
  
  warning_printed= False

  for i, t in enumerate(times[:-1]):
    h = times[i + 1] - t
    const = h * diffusion_coefficient / (length_step ** 2)
    # this warning is inside the loop since in principle 
    # we could be working with an arbitrary times array, 
    # which is not evenly spaced, in which case h changes around
    if (const > 1. and not warning_printed):
      print("Warning! time step is too large")
      warning_printed = True
    
    # main calculation
    x = solution[i,:]
    space_derivative = x[:-2] + x[2:] - 2 * x[1:-1]
    solution[i + 1, 1:-1] = x[1:-1] + const * space_derivative

  return (solution)
