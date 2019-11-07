def bubble_sort(array, comparison):
    """
    Comparison should be true for the sorted array
    """

    n = len(array)
    while True:
        changes = False
        for i in range(n - 1):
            if (not comparison(array[i], array[i + 1])):
                array[i], array[i+1] = array[i+1], array[i]
                changes = True
        if (changes == False):
            return (array)

def selection_sort(array, comparison):
    """
    Comparison should be true for the sorted array
    """

    n = len(array)
    if (n <= 1):
        return array
    sorted_index = 0 
    while True:
        minimum = array[sorted_index]
        min_index = 0
        for index, element in enumerate(array[sorted_index:]):
            if (comparison(element, minimum)):
                minimum = element
                min_index = index + sorted_index
        array.pop(min_index)
        array.insert(sorted_index, minimum)
        sorted_index += 1
        if (sorted_index == n - 1):
            return(array)

def quick_sort(array, comparison):
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

def merge_sort(array, comparison, sorted=False):
    """
    Comparison should be true for the sorted array
    """
    
    n = len(array)
    if (n<=1):
        return (array)


def algorithm_comparison(algorithm_list, algorithm_names, num=1000, every=10):
    from time import time
    def n_test(algorithm, n):
        n_list = list(range(n)[::-1])
        t1 = time()
        algorithm(n_list, lambda x, y: x < y)
        t2 = time()
        return(t2-t1)
    
    times_dict = {name:[] for name in algorithm_names}
    for (alg, name) in zip(algorithm_list, algorithm_names):
        for n in range(num)[::every]:
            times_dict[name].append((n_test(alg, n)))
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    model = lambda x, exponent, constant: constant * x**exponent
    plt.style.use('seaborn')
    for name in times_dict:
        popt, pcov = curve_fit(model, range(len(times_dict[name])), times_dict[name])
        plt.plot(times_dict[name], label=f'Exponent: {popt[1]:.1e} for {name}')
    plt.legend()

def merge(arr1, arr2): 
    n1 = len(arr1) 
    n2 = len(arr2) 
    i = j = 0
    comparison = lambda x, y:x<y 
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