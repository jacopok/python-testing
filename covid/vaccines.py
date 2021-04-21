import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data = pd.read_csv('data.csv')

arr = data['new_vaccinations_smoothed_per_million']

o = np.arange(1, len(arr)+1)

model = lambda x, C, r: C * np.exp2(r * x)

p, pcov = curve_fit(model, o, arr, p0=[5e-2, 1/50])

# print(f'Rate: {p[1]:.3f} +- {np.sqrt(pcov[1,1]):.4f} (inverse days)')
print(f'Doubling time: {1/p[1]:.1f} +- {np.sqrt(pcov[1,1]) / p[1]**2:.1f} days')

plt.semilogy(arr)
plt.semilogy(o, model(o, *p))
plt.title(f'{data["Day"][0]} to {data["Day"].values[-1]}')
plt.show()