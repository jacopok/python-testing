from gauss_seidel_3_2 import gauss_seidel
from math import isnan
from test_data_generation import test_data
from tqdm import tqdm
import numpy as np

def test_algorithm(iterations=100, dim=3, relaxation=False, **kwargs):
    conv = []
    nits = []
    for _ in tqdm(range(iterations)):
        n=0 
        while(True): 
            n+=1 
            A, b = test_data(dim, **kwargs)
            x, nit = gauss_seidel(A, b, relaxation=relaxation, verbose=False)
            if(x is not None): 
                if(not isnan(x[0])):
                    conv.append(n)
                    nits.append(nit)
                    break
    return (conv, nits)

if __name__ == '__main__':
    
    print("Let us test convergence for generic matrices")

    convergence, iterations = test_algorithm()

    print(f"Convergence was reached for one matrix in {np.average(convergence)}, and the median of the number of iterations was {np.median(iterations)}.")

    print("Now let us compare relaxation with no relaxation: first, with relaxation, for 5-dimensional matrices to make the problem harder")

    convergence, iterations = test_algorithm(dim=5, relaxation=True)

    print(f"Convergence was reached for one matrix in {np.average(convergence)}, and the median of the number of iterations was {np.median(iterations)}.")

    print("Now without relaxation: ")

    convergence, iterations = test_algorithm(dim=5, relaxation=False)

    print(f"Convergence was reached for one matrix in {np.average(convergence)}, and the median of the number of iterations was {np.median(iterations)}.")
    