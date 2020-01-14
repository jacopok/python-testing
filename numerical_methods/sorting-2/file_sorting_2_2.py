import pandas as pd
from sorting_2_1 import merge_sort, quick_sort, bubble_sort
from time import time

filename = "../../../numerical-methods/exercises/sorting/illustris3_135.dat"

t1 = time()
data = pd.read_csv(filename, sep = " ", header=None)
t2 = time()
print(f"Reading the data took {t2-t1:.2f} seconds")

vector = list(data[0])

comparison = lambda x, y: x<y
t3=time()
print(f"Selecting the column took {t3-t2:.2f} seconds")

sorted_vector_merge = merge_sort(vector, comparison=comparison)
t4 = time()
print(f"Sorting the array with merge sort took {t4-t3:.2f} seconds")

sorted_vector_quick = quick_sort(vector, comparison=comparison)
t5 = time()
print(f"Sorting the array with quick sort took {t5-t4:.2f} seconds")

sorted_vector_bubble = bubble_sort(vector, comparison=comparison)
t6 = time()
print(f"Sorting the array with bubble sort took {t6-t5:.2f} seconds")
