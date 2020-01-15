import numpy as np
import sympy as sym
sym.init_printing()

def symbolic_newton_rhapson(f, x0, eps=1e-10, verbose=False):
    """
    Inputs:
    f: sympy function
    x0: initial ansatz

    eps: tolerace, defaults to 1e-10

    Finds a zero of the function using the Newton-Rhapson method, 
        with a derivative which is calculated symbolically by sympy. 
    """

    x=x0
    x_symb = sym.symbols('x')

    fprime = sym.diff(f)
    
    if (verbose):
      print(f'Derivative: {fprime}')

    n_f = sym.lambdify(x_symb, f, 'numpy')
    n_fprime = sym.lambdify(x_symb, fprime, 'numpy')

    while True:
        delta_x = n_f(x) / n_fprime(x)
        xold = x
        x -= delta_x
        if (np.abs(xold - x) < eps):
            if(verbose):
                print(f"Error is {n_f(x)}")
            return(x)

if __name__ == '__main__':
    x = sym.symbols('x')
    f = sym.sin(x)
    symbolic_newton_rhapson(f, .3, verbose=True)