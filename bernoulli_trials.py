#%%

import numpy as np

prob_A = 1/3
prob_B = 1/4
N = int(1e5)
repeats = int(1e6)

prob_vector = [
    prob_A,
    prob_B,
    1 - prob_A - prob_B
]

rng = np.random.default_rng(seed=100)
probability_samples = rng.multinomial(n=N, pvals=prob_vector, size=repeats) / N

p_A = probability_samples[:, 0]
p_B = probability_samples[:, 1]

odds_ratio_samples = p_A / p_B
odds_ratio_average = prob_A / prob_B

print(f'Data standard deviation: {np.std(odds_ratio_samples):.4f}')

my_std = np.sqrt(odds_ratio_average**2 / N * (
    (1 / prob_A) +
    (1 / prob_B)
))

print(f'My formula: {my_std:.4f}')

paper_std = np.sqrt(odds_ratio_average**2 / N * (
    (prob_A / (1 - prob_A)) +
    (prob_B / (1 - prob_B))
))
print(f'Paper formula: {paper_std:.4f}')

# %%
