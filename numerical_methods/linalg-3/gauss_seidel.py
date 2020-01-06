import numpy as np
from numpy.linalg import matrix_rank
from gaussian_elimination import test_data
    
def iteration_step(A, b, x, relaxation=1):
    """
    Inputs:
    A: a matrix, shape = (n,n)
    b: a vector, shape = (n,)
    x: a vector, shape = (n,)
    relaxation: a scalar, which defaults to 1.
    for extrapolation set relaxation>1
    
    Ouputs: 
    x: a vector, shape (n,)

    The output vector is obtained through a step in the Gauss-Seidel algorithm.
    """

    xnew = np.copy(x)
    for i in range(len(x)):
        y = b[i]
        for j, val in enumerate(A[i,:]):
            if (j != i):
                y -= val * xnew[j]
        xnew[i] = y / A[i,i]
    return (relaxation*xnew + (1-relaxation) * x)

def gauss_seidel(A, b, ansatz=None, eps=1e-10, relaxation=True, verbose=True):
    """
    Inputs:
    A: a matrix, shape = (n,n)
    
    b: a vector, shape = (n,)
    
    ansatz: None or a vector, shape = (n,)
        the starting vector for the Gauss-Seidel algorithm
        if None, the vector b is used as an ansatz for the algorithm
    
    eps: a scalar, defaults to 1e-10
        the algorithm terminates when the inequality
            dist < eps * scale
        is satisfied, where:
            dist is the distance between two successive steps, 
            scale is the scale of the system, estimated with the Frobenius norm of A

    relaxation: a boolean, defaults to True
        if True, after 15 iterations the algorithm estimates a relaxation parameter which can be used to extrapolate, 
        in order to decrease the total number of iterations
        if False, no relaxation is used

    verbose: a boolean, defaults to True
        if True, the algorithm outputs information to the 
        standard output during the computation
        if False, this does not happen

    Ouputs: 
    x: a vector, shape (n,), or None
        the solution of the system Ax=b,
        or None if the algorithm diverged
    n: an integer
        the number of iterations

    Solves the linear system Ax=b iteratively.
    Convergence is guaranteed if:
        A is symmetric and positive definite
        A is diagonally dominant
    """

    # some checks on the shape of the matrices
    # and vectors involved
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

    # the solution of the problem in the nontrivial
    # kernel case is not implemented
    if (matrix_rank(A) < min(n_rows, n_cols)):
        return(None, 0)
    
    # utility functions
    norm = lambda y : np.linalg.norm(y, ord=2)
    dist = lambda y,z : norm(y-z)
    
    # define ansatz
    if (ansatz is not None):
        xnew = ansatz
    else:
        xnew = b

    # an estimate of the length scale of the 
    # linear system
    problem_scale = np.linalg.norm(A, ord='fro')

    # iteration number
    n = 0

    # first 10 iterations: they are always done
    # without relaxation 
    for _ in range(9):
        # store old value in the variable xold
        # in order to compute the distance 
        # between the kth and (k+1)th iteration
        # later
        xold = xnew
        xnew = iteration_step(A, b, xold)
        n+=1

    # distance at the 10th step:
    # will be used later to compute the optimal relaxation
    # and to check for divergence
    Dxk = dist(xold,xnew)

    divergence_count=0
    
    # do 5 more iterations if relaxation is set to True
    # and compute the optimum relaxation parameter
    if(relaxation):
        Oopt_vec = []
        for p in range(1,6):
            xold = xnew
            xnew = iteration_step(A, b, xold)
            Dx = dist(xnew, xold)
            if(Dx>Dxk):
                divergence_count += 1
            else:
                Oopt_vec.append(2/(1+np.sqrt(1-(Dx/Dxk)**(1/p))))
            n += 1

        if (divergence_count > 5):
            if(verbose): 
                print("Algorithm is diverging")
            return (None, n)

        Oopt = np.average(Oopt_vec)
        if (verbose):
            print(f"Oopt = {Oopt}")
    else:
        Oopt = 1
    

    # main cycle: keep iterating until either 
    # a solution is found, or the differences 
    # are staying large, which means the algorithm
    # is diverging
    diverged=False
    while norm(A@xnew-b) > eps * problem_scale:
        xold = xnew
        xnew = iteration_step(A, b, xold, Oopt)
        if (dist(xold, xnew) > Dxk):
            divergence_count += 1
        if (divergence_count > 20):
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

def test_algorithm(iterations=100, dim=3, relaxation=False, **kwargs):
    from math import isnan
    from gaussian_elimination import gaussian_elimination
    from tqdm import tqdm
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

Atest = np.array([
    [4, -1, 1],
    [-1, 4, -2],
    [1, -2, 4]
])
btest = np.array([12, -1, 5])

if __name__ == "__main__":
    from time import sleep
    sleep(.5)
    print("Let us tes the algorithm for the system with:")

    print("A = \n", Atest)
    print("b = ", btest)

    sleep(2)

    print("First with relaxation: ")
    x, n = gauss_seidel(Atest, btest)
    print("The solution given is ", x)

    sleep(2)

    print("First without relaxation: ")
    x, n = gauss_seidel(Atest, btest, relaxation=False)
    print("The solution given is ", x)

    sleep(2)

    print("Let us test convergence for generic matrices")

    convergence, iterations = test_algorithm()

    print(f"Convergence was reached for one matrix in {np.average(convergence)}, and the median of the number of iterations was {np.median(iterations)}.")

    sleep(2)

    print("Now let us compare relaxation with no relaxation: first, with relaxation, for 5-dimensional matrices to make the problem harder")

    convergence, iterations = test_algorithm(dim=5, relaxation=True)

    print(f"Convergence was reached for one matrix in {np.average(convergence)}, and the median of the number of iterations was {np.median(iterations)}.")

    print("Now without relaxation: ")

    convergence, iterations = test_algorithm(dim=5, relaxation=False)

    print(f"Convergence was reached for one matrix in {np.average(convergence)}, and the median of the number of iterations was {np.median(iterations)}.")