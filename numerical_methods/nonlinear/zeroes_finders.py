import numpy as np
import sympy as sp

def relaxation(f, x0, eps=1e-6):
    """
    Inputs: 
    f: 1-variable function.
        The system should look like x = f(x)
    x0: starting value
    eps: optional, threshold for convergence
    
    Finds a zero of f in the interval by iterating the 
    function.
    """    

    x = x0
    while True:
        xold = x
        x = f(x)
        if (np.abs(x - xold) < eps):
            return (x)

def bisection(f, interval, eps=1e-10, verbose=False):
    """
    Inputs: 
    f: 1-variable function
    interval: tuple of 2 elements, x0 and x1, the extremes of the interval
    eps: optional, threshold for convergence
    Finds a zero of f in the interval, with binary search.
    """
    x0, x1 = interval

    if (f(x0) * f(x1) >= 0):
        print(f"f({x0}) = {f(x0)}")
        print(f"f({x1}) = {f(x1)}")
        raise NotImplementedError("Function has the same sign on the sides of the interval.")
    
    number_iterations = 0
    while True:
        xmid = (x0 + x1) / 2.
        if (np.abs(f(xmid)) < eps):
            return xmid
        if (f(x0) * f(xmid) < 0):
            x1 = xmid
        else:
            x0 = xmid
        number_iterations += 1
        if (number_iterations % 100 == 0 and verbose):
            print(f"{number_iterations} iterations")

def newton_rhapson(f, x0, f_prime=None, eps=1e-10, cdeps=1e-11, verbose=False):
    if (not f_prime):
        f_prime = lambda x : (f(x+cdeps/2) - f(x-cdeps/2))/cdeps

    x = x0
    while True:
        delta_x = f(x) / f_prime(x)
        xold = x
        x -= delta_x
        if (np.abs(xold - x) < eps):
            if (verbose):
                print(f"Error is {f(x)}")
            return (x)

def symbolic_newton_rhapson(f, x0, eps=1e-10, verbose=False):
    x=x0
    x_symb = sp.symbols('x')

    fprime = sp.diff(f)
    
    n_f = sp.lambdify(x_symb, f, 'numpy')
    n_fprime = sp.lambdify(x_symb, fprime, 'numpy')

    while True:
        delta_x = n_f(x) / n_fprime(x)
        xold = x
        x -= delta_x
        if (np.abs(xold - x) < eps):
            if(verbose):
                print(f"Error is {n_f(x)}")
            return(x)

if __name__ == "__main__":
    #equals zero
    func_0 = lambda ecc, F: (lambda E: E - ecc * np.sin(E) - F)
    #equals E
    func_E = lambda ecc, F: (lambda E: ecc * np.sin(E) + F)
    
    ecc_list = [.1, .7, .9, .3]
    F_list = [np.pi / 3, np.pi / 3, np.pi / 3, np.pi]
    
    starting_point = 1
    other_extreme = 2
    for ecc, F in zip(ecc_list, F_list):
        print(relaxation(func_E(ecc, F), starting_point))
        print(newton_rhapson(func_0(ecc, F), starting_point))
        print(bisection(func_0(ecc, F), (starting_point, other_extreme)))