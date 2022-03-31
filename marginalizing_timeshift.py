import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

N = 100000

lambdas = rng.normal(loc=500,scale=200, size=N)
times = rng.normal(loc=0, scale=.01, size=N)

fig, ax = plt.subplots(2, 1, sharex=True)

ax[0].hist2d(lambdas, times, bins=100)

print(f'lambda std: {np.std(lambdas)}')

c = 1e-4
times_2 = times + c * lambdas
ax[1].hist2d(lambdas, times_2, bins=100)
plt.show()