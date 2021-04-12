import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from laplace_solver_9_1 import test_iteration, test_field, iteration_step

f1, e1 = test_iteration(test_field, iteration_step, tol=1e-2)
f2, e2 = test_iteration(test_field, iteration_step, tol=1e-2, relax=1.9)

fig, axs = plt.subplots(2,2)

axs[0, 0].imshow(f1)
axs[0,0].set_title('Relaxation = 1.')
axs[0, 1].semilogy(e1)
axs[0,1].set_xlabel('Iteration number')
axs[0,1].set_ylabel('Relative error $\\epsilon$')

axs[1, 0].imshow(f2)
axs[1,0].set_title('Relaxation = 1.9')
axs[1, 1].semilogy(e2)
axs[1,1].set_xlabel('Iteration number')
axs[1,1].set_ylabel('Relative error $\\epsilon$')
plt.show()
