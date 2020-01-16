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
from scipy.stats import linregress

from diffeq_integrators import euler, midpoint, fourth_order, leapfrog_KDK, leapfrog_DKD, hermite

from two_body_problem import second_order, G, Gprime
from two_body_analysis import E, L

methods = {
  'Euler': euler,
  'Midpoint': midpoint,
  'Fourth-order': fourth_order, 
  'Leapfrog KDK': leapfrog_KDK, 
  'Leapfrog DKD': leapfrog_DKD,
  'Hermite': hermite
}

functions = {
  'Euler': (second_order,),
  'Midpoint': (second_order,),
  'Fourth-order': (second_order,), 
  'Leapfrog KDK': (G,), 
  'Leapfrog DKD': (G,),
  'Hermite': (G, Gprime)
}

hs = np.logspace(-1.5, -0.5, num=5)
tmax = 30
params_fo = (0, tmax, np.array([[[1., 1.], [-1., - 1.]], [[-.5, 0.], [0.5, 0.]]]))
params_so = (0, tmax, np.array([[1., 1.], [-1., -1.]]), np.array([[-.5, 0], [0.5, 0]]))

params={
  'Euler': params_fo,
  'Midpoint': params_fo,
  'Fourth-order': params_fo, 
  'Leapfrog KDK': params_so, 
  'Leapfrog DKD': params_so,
  'Hermite': params_so
}

th_order={
  'Euler': 1.,
  'Midpoint': 2.,
  'Fourth-order': 4., 
  'Leapfrog KDK': 2., 
  'Leapfrog DKD': 2.,
  'Hermite': 4.
}

def calculate_errors(hs=hs, methods=methods, params_fo=params_fo, params_so=params_so):
  Es_dict={}
  Ls_dict={}
  
  for method_name in methods:
    for h in hs:
      _, xs = methods[method_name](*functions[method_name], *params[method_name], h)
      if method_name not in Es_dict:
        Es_dict[method_name] = [np.average(E(xs, calculate_average=False))]
      else:
        Es_dict[method_name].append(np.average(E(xs, calculate_average=False)))
      if method_name not in Ls_dict:
        Ls_dict[method_name] = [np.average(L(xs, calculate_average=False))]
      else:
        Ls_dict[method_name].append(np.average(L(xs, calculate_average=False)))
  
  return(Es_dict, Ls_dict)

def make_plot(Es_dict, Ls_dict, fit = True):

  fig, axs = plt.subplots(1, 2)

  for method_name in methods:
    Earr = Es_dict[method_name]
    Larr = Ls_dict[method_name]
    Elab = method_name
    Llab = method_name
    if (fit):
      log_hs = np.log(hs)
      log_E = np.log(Earr)
      log_L = np.log(Larr)
      Eslope, __, __, __, __ = linregress(log_hs, log_E) 
      Lslope, __, __, __, __ = linregress(log_hs, log_L) 
      Elab += f' slope {Eslope:.2f}'
      Llab += f' slope {Lslope:.2f}'
      # axs[0].loglog(hs, powerlaw(hs, *Ep0))
      # axs[1].loglog(hs, powerlaw(hs, *Lp0))

    axs[0].loglog(hs, Earr, label=Elab)
    axs[1].loglog(hs, Larr, label=Llab)
  axs[0].set_title('Energy conservation')
  axs[0].set_ylabel('$\\Delta E / E$')
  axs[1].set_title('Angular momentum conservation')
  axs[1].set_ylabel('$\\Delta L / L$')
  
  for ax in axs:
    ax.legend(loc='lower right')
    ax.set_xlabel('$h$')
  plt.show()

if __name__ == "__main__":
  E, L = calculate_errors()
  make_plot(E, L)