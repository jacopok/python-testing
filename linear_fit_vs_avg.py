import numpy as np
import matplotlib.pyplot as plt

# x and F errors' standard deviations
sigma_x = .1
sigma_F = .1

# true elastic parameter
k_true = 1.

# number of mock measurement points
n_measurement_points = 20

# number of trials to run
n_trials = 1000

def trial(seed: int) -> tuple[float, float]:

    # generate N equally-spaced x points between 1 and 20, inclusive
    xi = np.linspace(1, 20, num=n_measurement_points)
    # generate the "true" forces, according to the linear law
    # (without the negative sign for simplicity, it doesn't change anything)
    Fi = k_true * xi

    # add Gaussian random noise to x and F
    rng = np.random.default_rng(seed)    
    xi += rng.normal(scale=sigma_x, size=xi.shape)
    Fi += rng.normal(scale=sigma_F, size=Fi.shape)

    # estimate the elastic parameter with the two approaches
    k_estimate_avg = 1 / n_measurement_points * np.sum(Fi / xi)
    k_estimate_fit =  np.sum(Fi * xi) / np.sum(xi**2)
    
    return k_estimate_avg - k_true, k_estimate_fit - k_true

# run the trial several times to get statistics for the variance
# of the estimator
avg_errs = []
fit_errs = []
for n in range(n_trials):
    # we seed the RNG with the index of the for loop - doesn't really matter,
    # it's useful for reproducibility
    err_avg, err_fit = trial(n)
    avg_errs.append(err_avg)
    fit_errs.append(err_fit)

# make a histogram of the results
plt.hist(avg_errs, alpha=.5, density=True, label='average')
plt.hist(fit_errs, alpha=.5, density=True, label='fit')
plt.xlabel('Estimated minus true $k$')
plt.ylabel('Probability density')
plt.legend()

# to save the figure, one can do
# plt.savefig('linear_fit_vs_avg.png', dpi=150)

# to show it interactively, instead, do
# plt.show()