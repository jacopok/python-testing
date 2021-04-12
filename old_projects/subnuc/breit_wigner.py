import matplotlib.pyplot as plt
plt.style.use('seaborn')

import numpy as np


def breit_wigner(E, M_R, gamma, gamma_i, gamma_f, s_a, s_b, J):
    return((2*J+1)/(2*s_a+1)*(2*s_b+1)
    *(4*np.pi)/E**2
    *gamma_i*gamma_f/((E-M_R)**2 + (gamma/2)**2))

def normalize(x):
    return(x / np.sum(x))

E = np.linspace(400, 1000, num=500) # MeV

bw_omega = breit_wigner(E, 782, 8, 4, 4, 0, 0, 0)
bw_eta = breit_wigner(E, 548, 1.3, 1.3/2, 1.3/2, 0, 0, 0)

fig = plt.figure(1)
plt.plot(E, normalize(bw_eta+bw_omega), label='Combined Breit-Wigner')
plt.xlabel('Energy [MeV]')
plt.ylabel('Number of events')
plt.legend()
plt.show()
