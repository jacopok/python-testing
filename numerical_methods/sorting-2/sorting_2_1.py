from copy import copy
from scipy.optimize import curve_fit
from time import time
from random import sample, randrange
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
import matplotlib.cm as cm
import numpy as np
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

def bubble_sort(array, comparison = lambda x,y: x<y):
    """
    Comparison should be true for the sorted array
    """
    arr = copy(array)

    n = len(arr)
    while True:
        changes = False
        for i in range(n - 1):
            if (not comparison(arr[i], arr[i + 1])):
                arr[i], arr[i+1] = arr[i+1], arr[i]
                changes = True
        if (changes == False):
            return (arr)

def selection_sort(array, comparison = lambda x,y: x<y):
    """
    Comparison should be true for the sorted array
    """
    arr = copy(array)

    n = len(arr)
    if (n <= 1):
        return arr
    sorted_index = 0 
    while True:
        minimum = arr[sorted_index]
        min_index = sorted_index
        for index, element in enumerate(arr[sorted_index:]):
            if (comparison(element, minimum)):
                minimum = element
                min_index = index + sorted_index
        arr.pop(min_index)
        arr.insert(sorted_index, minimum)
        sorted_index += 1
        if (sorted_index == n - 1):
            return(arr)

def quick_sort(array, comparison = lambda x,y: x<y):
    """
    Comparison should be true for the sorted array
    """
    
    n = len(array)
    if (n<=1):
        return(array)
    else:
        pivot = array[0]
    less_than = []
    more_than = []
    for i in range(1, n):
        if (comparison(array[i], pivot)):
            less_than.append(array[i])
        else:
            more_than.append(array[i])
    sorted_less_than = quick_sort(less_than, comparison)
    sorted_more_than = quick_sort(more_than, comparison)
    return (sorted_less_than + [pivot] + sorted_more_than)

def merge(arr1, arr2, comparison):
    """
    Merges two sorted arrays in O(n1+n2)
    """
    
    n1 = len(arr1) 
    n2 = len(arr2) 
    i = j = 0
    merged = [] 
    while (i + j < n1 + n2): 
        if (comparison(arr1[i], arr2[j])):
            merged.append(arr1[i]) 
            i += 1 
        else: 
            merged.append(arr2[j]) 
            j += 1
        if (i == n1): 
            return(merged + arr2[j:])
        if (j == n2): 
            return( merged + arr1[i:])

def merge_sort(array, comparison = lambda x,y: x<y):
    """
    Comparison should be true for the sorted array
    """
    n = len(array)
    if (n<=1):
        return (array)
    first_half = merge_sort(array[:int(n / 2)], comparison)
    second_half = merge_sort(array[int(n / 2):], comparison)
    return(merge(first_half, second_half, comparison))

def algorithm_comparison(algorithm_list, algorithm_names, num=1000, every=10, test_type="random"):

    def random_swap(array, n):
        n1 = randrange(n)
        n2 = randrange(n)
        array[n1], array[n2] = array[n2], array[n1]
        return(array)

    test_types = {
        "inverse_sorted": lambda n: list(range(n))[::1],
        "random": lambda n: sample(list(range(n)), k=n),
        "almost_sorted": lambda n: random_swap(list(range(n)), n)
    } 

    def n_test(algorithm, n):
        n_list = test_types[test_type](n)
        t1 = time()
        algorithm(n_list)
        t2 = time()
        return(t2-t1)
    
    times_dict = {name:[] for name in algorithm_names}
    for (alg, name) in zip(algorithm_list, algorithm_names):
        print("Testing " + name)
        for n in range(1, num)[::every]:
            times_dict[name].append((n_test(alg, n)))

    color = iter(cm.rainbow(np.linspace(0,1,len(times_dict))))

    model = lambda x, exponent: x * exponent

    for name in times_dict:
        n_array = np.arange(1, every*len(times_dict[name]), every)
        
        popt, pcov = curve_fit(model, np.log(n_array), np.log(times_dict[name]))
        c = next(color)
        plt.loglog(n_array, times_dict[name], label=f'{name}: exponent {popt[0]:.3f}', c=c)
        plt.loglog(n_array, n_array**popt, c=c)

    plt.xlabel('Length of the array')
    plt.ylabel('Time [\\SI{}{s}]')
    plt.grid(True)
    plt.legend()
    plt.title('Sorting algorithm execution types on ' + test_type + ' arrays')

test_list = [9, -3, 5, 2, 6, 8, -6, 1, 3]