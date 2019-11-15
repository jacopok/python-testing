import numpy as np
from numpy.linalg import matrix_rank
from gaussian_elimination import test_data

def dirty_matrix(A, eps = 1e-5):
    Aflat = A.flatten()
    scale = np.average(np.abs(Aflat))
    nr, nc = np.shape(A)

    for i in range(min(nr, nc)):
        A[i, i] += np.random.normal(scale=scale * eps)
        
    return (A)
    
def iteration_step(A, b, x, relaxation=1):
    xnew = np.zeros_like(x)
    for i in range(len(x)):
        y = b[i]
        for j, val in enumerate(A[i,:]):
            if (j != i):
                y -= val * x[j]
        xnew[i] = y / A[i,i]
    return (relaxation*xnew + (1-relaxation) * x)

def gauss_seidel(A, b, ansatz=None, eps = 1e-10, relaxation=True, verbose=True):
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
        return(None)
        # raise TypeError("Rank too low")
    
    
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
        return None

    if(relaxation):
        Oopt = np.average(Oopt)
        print(f"Oopt = {Oopt}")
    else:
        Oopt = 1

    while dist(xold, xnew) > eps * problem_scale:
        xold = xnew
        xnew = iteration_step(A, b, xold, Oopt)
        n += 1

    if(verbose):
        print(f"Algoritm converged after {n} iterations")
        print(f"Error is {norm(A@xnew - b)}")

    return (xnew)

def test(**kwargs):
    from math import isnan
    from gaussian_elimination import gaussian_elimination
    from time import sleep
    conv = []
    trigger = True
    while (trigger == True):
        try: 
            n=0 
            while(True): 
                n+=1 
                A, b = test_data(3, **kwargs)
                x = gauss_seidel(A, b, relaxation=False, verbose=False)
                if(x is not None): 
                    if(not isnan(x[0])): 
                        print(x) 
                        print(gaussian_elimination(A, b)) 
                        conv.append(n) 
                        sleep(.1)
                        break
            print(f"Found convergence for the {n}th system")
        except KeyboardInterrupt:
            trigger = False
    return(conv)