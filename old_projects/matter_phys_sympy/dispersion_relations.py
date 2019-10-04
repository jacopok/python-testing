from sympy import *
import numpy as np
import matplotlib.pyplot as plt

K, M, m = symbols('K M m', real=True, positive=True)
ka = symbols('ka')
sig = symbols('sig', integer=True)

mu = 1/(1/M + 1/m)
sum_m = M+m


omega_square = 1/2 *( sum_m  +
    sig * sqrt(M**2 + m**2 + 2*M*m*(1-2*sin(ka)**2))) / \
    (M*m/2/K)

omega_plus = sqrt(omega_square.subs(sig, 1))
omega_minus = sqrt(omega_square.subs(sig, -1))

omega_plus_estimate = sqrt(2 * K / mu )
omega_minus_estimate = sqrt(2 * K / sum_m) * ka

K_val = 1
m_val = 1
M_val = 1.1

plot(omega_plus.subs(K, K_val).subs(m, m_val).subs(M, M_val),
    omega_minus.subs(K, K_val).subs(m, m_val).subs(M, M_val),
    omega_plus_estimate.subs(K, K_val).subs(m, m_val).subs(M, M_val),
    omega_minus_estimate.subs(K, K_val).subs(m, m_val).subs(M, M_val))

omega_diff = (omega_plus - omega_minus).subs(ka, pi/2).subs(m, 1).subs(K, 1)
func = lambdify(M, omega_diff, 'numpy')
x = np.arange(1, 10, 0.1)
y = func(x)
