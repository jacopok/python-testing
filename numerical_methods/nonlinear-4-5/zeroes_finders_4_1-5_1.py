import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

def relaxation(f, x0, eps=1e-6, rel=1., verbose=False):
    """
    Inputs: 
    f: 1-variable function.
        The system should look like x = f(x)
    x0: starting value
    eps: optional, threshold for convergence
    rel: relaxation parameter 
        (set rel>1 for extrapolation, rel<1 for under-relaxation)
        under relaxation seems to work best
    verbose: defaults to False, then nothing is printed
        if it is True, the number of iterations is printed

    Finds a zero of f in the interval by iterating the 
    function.
    """    

    x = x0
    n = 0
    while True:
        xold = x
        x = f(x)*rel + xold*(1-rel)
        if (np.abs(x - xold) < eps):
            if(verbose):
                print(f'Number of iterations: {n}')
            return (x)
        n+=1

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
        if(verbose):
            if (number_iterations % 100 == 0):
                print(f"{number_iterations} iterations")

def newton_rhapson(f, x0, f_prime=None, eps=1e-10, cdeps=1e-11, verbose=False):
    """
    Inputs: 
    f: 1-variable function
    x0: initial ansatz from which the search starts
    f_prime: optional, 1-variable function: the derivative of f 
        if it is None (or not given) then the derivative is calculated numerically

    eps: optional, threshold for convergence, defaults to 1e-10
    cdeps: optional, step for the numerical derivative, defaults to 1e-11
    verbose: optional defaults to False: if it is True the error is printed
        before returning the value

    Finds a zero of f in the interval.
    """

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
    """
    Inputs:
    f: sympy function
    x0: initial ansatz

    eps: tolerace, defaults to 1e-10

    Finds a zero of the function using the Newton-Rhapson method, 
        with a derivative which is calculated symbolically by sympy. 
    """

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
    other_extreme = 6

    Es = np.linspace(0, 2*np.pi)
    colors = iter(plt.get_cmap('Set1').colors)
    for ecc, F in zip(ecc_list, F_list):
        print(f'Eccentricity is ecc={ecc:.2f}, mean anomaly is F={F:.2f}')
        r_res = relaxation(func_E(ecc, F), starting_point)
        print(f'Relaxation gives {r_res:.2f}')
        nr_res = newton_rhapson(func_0(ecc, F), starting_point)
        print(f'Newton-Rhapson gives {nr_res:.2f}')
        b_res = bisection(func_0(ecc, F), (starting_point, other_extreme))
        print(f'Bisection gives {b_res:.2f}')
        color = next(colors)
        plt.plot(Es, func_0(ecc, F)(Es), label=f'ecc={ecc:.2f}, F={F:.2f}', c=color)
        ax = plt.gca()
        ax.axvline(r_res, c=color, linestyle='dotted', label=f'E = {r_res:.2f}')
    plt.legend()
    plt.xlabel('$E$')
    plt.ylabel('$E - \\text{ecc} \\times \\sin(E) - F$')
    plt.show()