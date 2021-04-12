import sympy as sp
sp.init_printing()
import ipywidgets
import matplotlib.pyplot as plt
import numpy as np

#%%

v = sp.symbols('v')
gamma = 1 / sp.sqrt(1-v**2)

theta_prime = sp.symbols('theta_prime')

theta = sp.atan(1/gamma/(1/sp.tan(theta_prime) + v/sp.sin(theta_prime)))

distribution = sp.diff(theta, theta_prime)

#%%

def plot_distribution(relative_velocity):
    new_distribution = distribution.subs(v, relative_velocity)
    x = sp.symbols('x')
    f= sp.lambdify(x, new_distribution.subs(theta_prime, x), 'numpy')
    theta_primes = np.linspace(1e-10, np.pi-1e-10)
    plt.plot(theta_primes, f(theta_primes))

ipywidgets.interact(plot_distribution, relative_velocity=(0,0.99,0.01))

#%%
x = sp.symbols('x')

f = sp.tan(x)

f2 = sp.lambdify(x, f, 'numpy')
x2 = np.linspace(0,1)
plt.plot(x2, f2(x2))
