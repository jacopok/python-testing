import numpy as np
from numpy.linalg import matrix_rank
from gaussian_elimination import test_data

class dirty_matrix():
    def __init__(self, A, eps=1e-5):
        self.A = A
        self.n=min(np.shape(A))
        print(f"Initialized an {self.n}-dimensional matrix")
        self.sumrows=np.sum(np.abs(A), axis=1)

    def __iter__(self):
        return self

    def __next__(self):
        dirtyA = np.copy(self.A)
        for i in range(self.n):
            noise = 0
            while (np.abs(noise) < self.sumrows[i]):
                noise = np.random.normal(scale=self.sumrows[i])

            dirtyA[i, i] += noise
        return (dirtyA)

def not_diagonally_dominant(A):
    return((np.sum(np.abs(A), axis=1) > 2*np.diagonal(np.abs(A))).any())
    
def iteration_step(A, b, x, relaxation=1):
    xnew = np.copy(x)
    for i in range(len(x)):
        y = b[i]
        for j, val in enumerate(A[i,:]):
            if (j != i):
                y -= val * xnew[j]
        xnew[i] = y / A[i,i]
    return (relaxation*xnew + (1-relaxation) * x)

def gauss_seidel(A, b, ansatz=None, eps = 1e-10, relaxation=True, verbose=True, diagonally_dominant=False):
    A_shape = np.shape(A)
    b_shape = np.shape(b)
    if (len(A_shape) != 2):
        raise TypeError("A must be a 2D matrix")
    if (len(b_shape) != 1):
        raise TypeError("b must be a 1D vector")
    if (A_shape[0] != b_shape[0]):
        raise TypeError("column number of A must equal dimension of b")

    n_rows, n_cols = A_shape
    A = np.array(A, dtype=np.float64)
    b = np.array(b, dtype=np.float64)

    if (matrix_rank(A) < min(n_rows, n_cols)):
        return(None, 0)
        # raise TypeError("Rank too low")

    if(not diagonally_dominant):
        if (not_diagonally_dominant(A)):
            print("Doing stochastic calculation")
            iterator = dirty_matrix(A)
            xarray = []
            narray = []
            from tqdm import tqdm
            for _ in tqdm(range(10000)):
                x, n = gauss_seidel(next(iterator), b, ansatz=ansatz, relaxation=relaxation, verbose=False, diagonally_dominant=True)
                xarray.append(x)
                narray.append(n)
            xav = np.average(np.array(xarray),axis=0)
            return(xav, np.sum(n))

    
    norm = lambda y : np.linalg.norm(y, ord=1)
    dist = lambda y,z : norm(y-z)
    
    if (ansatz is not None):
        xnew = ansatz
    else:
        xnew = b

    problem_scale = np.linalg.norm(A, ord='fro')

    # iteration number
    n = 0
    for _ in range(10):
        xold = xnew
        xnew = iteration_step(A, b, xold)
        if(verbose):
            print(xnew)
        n+=1

    if(verbose):
        print(f"Did {n} iterations")

    Dxk = dist(xold,xnew)
    if(verbose):
        print(f"Dx = {Dxk}")

    Oopt = []
    divergence_count=0
    for p in range(1,11):
        xold = xnew
        xnew = iteration_step(A, b, xold)
        Dx = dist(xnew, xold)
        if(Dx>Dxk):
            divergence_count += 1
        else:
            Oopt.append(2/(1+np.sqrt(1-(Dx/Dxk)**(1/p))))
        if(verbose):
            print(f"Dx = {Dx}")
        n += 1
    if(verbose):
        print(f"Did {n} iterations")
    
    if (divergence_count > 5):
        if(verbose): 
            print("Algorithm is diverging")
        return (None, n)

    if(relaxation):
        Oopt = np.average(Oopt)
        if (verbose):
            print(f"Oopt = {Oopt}")
    else:
        Oopt = 1
    
    diverged=False
    while dist(xold, xnew) > eps * problem_scale:
        xold = xnew
        xnew = iteration_step(A, b, xold, Oopt)
        if (dist(xold, xnew) > Dxk):
            divergence_count += 1
        if (divergence_count > 100):
            diverged=True
            break
        n += 1

    if (verbose):
        if(diverged):
            print(f"Algorithm diverged after {n} iterations")
        else:
            print(f"Algoritm converged after {n} iterations")
        print(f"Error is {norm(A@xnew - b)}")

    return (xnew, n)

def test(dim=3, relaxation=False, **kwargs):
    from math import isnan
    from gaussian_elimination import gaussian_elimination
    from time import sleep
    conv = []
    nits = []
    trigger = True
    while (trigger == True):
        try: 
            n=0 
            while(True): 
                n+=1 
                A, b = test_data(dim, **kwargs)
                x, nit = gauss_seidel(A, b, relaxation=relaxation, verbose=False)
                if(x is not None): 
                    if(not isnan(x[0])): 
                        print(x) 
                        print(gaussian_elimination(A, b)) 
                        conv.append(n)
                        nits.append(nit)
                        sleep(.1)
                        break
            print(f"Found convergence for the {n}th system")
        except KeyboardInterrupt:
            trigger = False
    return (conv, nits)

Atest = np.array([
    [4, -1, 1],
    [-1, 4, -2],
    [1, -2, 4]
])
btest = np.array([12, -1, 5])