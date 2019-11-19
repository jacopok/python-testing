from time import time
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

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

    global times_array
    times_array.append(time())

    n = len(array)
    if (n<=1):
        return (array)
    first_half = merge_sort(array[:int(n / 2)], comparison)
    second_half = merge_sort(array[int(n / 2):], comparison)
    return(merge(first_half, second_half, comparison))

times_array = []
from random import sample

n = 1_000_000
test_arr= list(range(n))[::-1]
# test_arr = sample(list(range(n)), k=n)

s = merge_sort(test_arr)

t = np.array(times_array)
t -= t[0]
t *= 1e3
 
plt.plot(t)
plt.xlabel("Algorithm call")
plt.ylabel("time [ms]")