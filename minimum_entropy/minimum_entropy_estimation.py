import numpy as np
from scipy.optimize import minimize
from functools import partial
import matplotlib.pyplot as plt

def gaussian_model(x, loc, scale):
    """Model for the probability distribution."""
    return np.exp(- (x - loc)**2 / scale**2 / 2) / np.sqrt(2*np.pi) / scale


def entropy(data, model):
    return np.average(-np.log(model(data)))


def score(params):
    """Given the parameters of the distribution, 
    return the entropy computed on the data."""
    loc, scale = params
    model = partial(gaussian_model, loc=loc, scale=scale)
    return entropy(nums, model)


if __name__ == "__main__":

    # Generate some normally distributed numbers
    nums = np.random.normal(loc=4, scale=2, size=60_000)

    result = minimize(score, x0=[1, 1])

    print(result.x)
    
    th_max = np.log(2 * np.sqrt(2 * np.pi * np.e))
    
    print(f'Theoretical Gaussian entropy: {np.log(2 * np.sqrt(2 * np.pi * np.e))}')
    print(f'Current result: {score(result.x)}')
    print(f'Result with true parameters of the distribution: {score((4, 2))}')
    
    loc_array = np.linspace(3.9, 4.1)
    scale_array = np.linspace(1.9, 2.1)
    
    entropies = np.zeros(loc_array.shape + scale_array.shape)
    
    for i, loc in enumerate(loc_array):
        for j, scale in enumerate(scale_array):
            entropies[i, j] = score((loc, scale)) - th_max
    
    plt.contourf(loc_array, scale_array, entropies, levels=40)
    plt.colorbar()
    plt.show()
    