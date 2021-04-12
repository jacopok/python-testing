#%%

import numpy as np
from tqdm import tqdm

N = int(2e6)
ms=[4, 6, 8, 10, 12, 20, 50, 100]
averages = []

for m in tqdm(ms):
    tries = []

    for _ in range(N):
        s = 0
        t = 0
        while s < m:
            s += np.random.randint(1, m + 1)
            t += 1
        tries.append(t)
    averages.append(np.average(tries))

averages_minus_one = []

for m in tqdm(ms):
    tries = []

    for _ in range(N):
        s = 0
        t = 0
        while s < m:
            s += np.random.randint(0, m)
            t += 1
        tries.append(t)
    averages_minus_one.append(np.average(tries))

averages_zero_n = []

for m in tqdm(ms):
    tries = []

    for _ in range(N):
        s = 0
        t = 0
        while s < m:
            s += np.random.randint(0, m+1)
            t += 1
        tries.append(t)
    averages_zero_n.append(np.average(tries))


# %%

plt.semilogx(ms, averages, label='Regular dice: 1 to $N$')
plt.semilogx(ms, averages_minus_one, label='Dice from 0 to $N-1$')
plt.semilogx(ms, averages_zero_n, label='Dice from 0 to $N$')
plt.axhline(np.e, c='black', lw=.7, ls=':', label='$e$')
plt.xlabel('Number of sides')
plt.ylabel('Tries needed to surpass $N$')
plt.legend()
plt.savefig('dice_uniform.png')
# %%
