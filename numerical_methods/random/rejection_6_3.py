import numpy as np

def pdf(x, sigma=2., loc = 0.):
    return(1/np.sqrt(2*np.pi)/sigma*np.exp(-(x-loc)**2/2/sigma**2))

def rejection_sample(pdf, low=-50, high=50, pdf_max=None, N=int(1e6)):

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
    print(niterations)
    return (samples)
    
