import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.style.use('seaborn')

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}''')

data = pd.read_csv('full_odd_A.csv', index_col=False)

for index, row in data.iterrows():
    Z = row['Z']
    N = row['N']
    A = Z+N
    energy = row['Binding/A'] * A
    if(np.abs(Z-N) != 1):
        data.drop(index, inplace=True)

Z = data['Z'].values
N = data['N'].values
A = Z+N
energies = np.array(data['Binding/A'].values, dtype=np.float64) * A / 1e3
#because the energies are in kev

DeltaBs = []

for a in range(max(A)):
    Bs = []
    for z, n, e in zip(Z, N, energies):
        if(z+n == a):
            Bs.append(e)
    if(len(Bs)==2):
        DeltaBs.append([a, np.abs(Bs[0] - Bs[1])])

DeltaBs = np.array(DeltaBs)

A23_arr = DeltaBs[:,0]**(2/3)
B_arr = DeltaBs[:,1]

def B_lin(x, aC):
    return(aC * x)

def B_cor(x, aC):
    return(aC*(x - 1/np.sqrt(x)))

a_lin, avar_lin = curve_fit(B_lin, A23_arr, B_arr)
a_cor, avar_cor = curve_fit(B_cor, A23_arr, B_arr)

def chisquare(x, y, B, aC):
    residuals = y - B(x, aC)
    return(np.sum(residuals**2, axis=0) / len(x))

print(f'Linear chisquare: {chisquare(A23_arr, B_arr, B_lin,  a_lin):.3f} MeV^2')
print(f'a_C linear = {1e3*a_lin[0]:.1f} keV +- {1e3*np.sqrt(avar_lin[0][0]):.2f} keV')
print(f'Correct chisquare: {chisquare(A23_arr, B_arr, B_cor,  a_cor):.3f} MeV^2')
print(f'a_C correct = {1e3*a_cor[0]:.1f} keV +- {1e3*np.sqrt(avar_cor[0][0]):.2f} keV')

fit = plt.figure(1)
A_test = np.linspace(1, np.max(A)**(2/3))
plt.scatter(A23_arr, B_arr, label='Data')
plt.plot(A_test, B_lin(A_test, a_lin), 'b-', label = 'Z*Z')
plt.plot(A_test, B_cor(A_test, a_cor), 'g', label = 'Z*(Z-1)')
plt.xlabel('$A^{2/3}$')
plt.ylabel('$B$ difference between $Z = (A\pm1)/2$ [MeV]')
plt.legend()
fit.savefig('odd_A_fit.pdf', format='pdf')

res = plt.figure(2)
plt.plot(A23_arr, B_lin(A23_arr, a_lin) - B_arr, 'bo', label = 'Z*Z')
plt.plot(A23_arr, B_cor(A23_arr, a_cor) - B_arr, 'g^', label = 'Z*(Z-1)')
plt.plot(A23_arr, np.zeros(len(A23_arr)))
plt.xlabel('$A^{2/3}$')
plt.ylabel('$B$ difference between $Z = (A\pm 1)/2$ minus model [MeV]')
plt.legend()
res.savefig('odd_A_residuals.pdf', format='pdf')

plt.close('all')
