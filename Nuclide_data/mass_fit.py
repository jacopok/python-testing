import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

data = pd.read_csv('binding_energies.csv', index_col=False)

# these correspond to A = 148

# intensities = data.iloc[:,2].values
# iarray = []
# for x in intensities:
#     if x:
#         iarray.append(x.strip())
# iarray = list(filter(None, iarray))
# intensities = np.array(iarray, dtype=np.float)

A = 148

energies = data['Binding/A'].values / 1e3 * A
Z = data['Z'].values
N = data['N'].values

def get_params(*p, A):
    (a, b, c) = p
    a_A = b / 4
    a_C = -( a + b /A )* A**(1/3)
    return(a_A, a_C)

get_a_P = lambda c1, c2, A: A**(1/2) * np.abs(c1-c2) / 2

vertex = lambda a, b, c: -b**2 /4/a + c
# returns the y coordinate of the vertex of the parabola

p_even = np.polyfit(Z[::2], energies[::2], 2)
p_odd = np.polyfit(Z[1::2], energies[1::2], 2)

params_even = get_params(*p_even, A=A)
params_odd = get_params(*p_odd, A=A)

a_A, a_C = np.average(np.stack((params_even, params_odd), axis=0), axis=0)
a_P = get_a_P(vertex(*p_even), vertex(*p_odd), A=A)

experimental_vertex = np.average([vertex(*p_even), vertex(*p_odd)], axis=0)

a_V, a_S = 16, 17

th_constant = a_V* A - a_A*A -  a_S * A**(2/3)

th_b = 4 * a_A

th_a = - a_C * A**(-1/3) - 4 * a_A / A

th_vertex = th_constant - th_b**2 / (4*th_a)

print(f'a_A = {a_A:.2f} MeV')
print(f'a_C = {a_C:.2f} MeV')
print(f'a_P = {a_P:.2f} MeV')

print(f'Vertex energy: theoretical {th_vertex:.0f} MeV, experimental {experimental_vertex:.0f} MeV')
print(f'Calculated with a_V = {a_V} MeV and a_S = {a_S} MeV')

parabola = np.vectorize(lambda x, a, b, c: x**2 *a + x*b + c)

parabolas = plt.figure(1)

Z_array = np.linspace(min(Z), max(Z), num=100)

plt.scatter(Z[::2], energies[::2], label = 'Even energies')
plt.scatter(Z[1::2], energies[1::2], label = 'Odd energies')
plt.plot(Z_array, parabola(Z_array, *p_even), label = 'Even energies, model')
plt.plot(Z_array, parabola(Z_array, *p_odd), label = 'Odd energies, model')

plt.xlabel('Z')
plt.ylabel('B [MeV]')
plt.legend()

parabolas.savefig('parabolic_fits.eps', format='eps')

even_residuals = parabola(Z[::2], *p_even) - energies[::2]
odd_residuals = parabola(Z[1::2], *p_odd) - energies[1::2]

residuals = plt.figure(2)
plt.scatter(Z[::2], 1e3*even_residuals, label = 'Even residuals')
plt.scatter(Z[1::2], 1e3*odd_residuals, label = 'Odd residuals')
plt.plot(Z_array, np.zeros(len(Z_array)))

plt.xlabel('Z')
plt.ylabel('ΔB [keV]')

plt.legend()
residuals.savefig('residuals.eps', format='eps')

plt.close('all')
