import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

def gauss(x, sigma=2., loc = 0.):
    return(1/np.sqrt(2*np.pi)/sigma*np.exp(-(x-loc)**2/2/sigma**2))

def rejection_sample(pdf=gauss, low=-50, high=50, pdf_max=None, N=int(1e5)):

    if (pdf_max == None):
        pdf_max = pdf(0)

    nsamples = 0
    niterations = 0
    samples = [] 
    while(nsamples<N):
        unif1 = np.random.uniform(low=low, high=high)
        unif2 = np.random.uniform(low=0., high=pdf_max)
        if (pdf(unif1) > unif2):
            samples.append(unif1)
            nsamples += 1
        niterations += 1
    print(f"Took {niterations} iterations for {nsamples} samples: a ratio of {niterations / nsamples} to one.")
    return (samples)
    
if __name__ == '__main__':
    deviates = rejection_sample()
    plt.hist(deviates, density=True, bins=100)
    plt.ylabel('Probability density function')
    plt.show()
    