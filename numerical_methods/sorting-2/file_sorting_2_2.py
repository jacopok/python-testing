import pandas as pd
from sorting_2_1 import merge_sort, quick_sort, bubble_sort
from time import time
from itertools import combinations

filename = "../../../numerical-methods/exercises/sorting/illustris3_135.dat"

t1 = time()
data = pd.read_csv(filename, sep = " ", header=None)
t2 = time()
print(f"Reading the data took {t2-t1:.2f} seconds")

vector = list(data[0])
length = len(vector)

t3=time()
print(f"Selecting the column took {t3-t2:.2f} seconds")

sorted_vector_merge = merge_sort(vector)
t4 = time()
print(f"Sorting the array with merge sort took {t4-t3:.2f} seconds")

sorted_vector_quick = quick_sort(vector)
t5 = time()
print(f"Sorting the array with quick sort took {t5-t4:.2f} seconds")

len_bubble = 15_000
sorted_vector_bubble = bubble_sort(vector[:len_bubble])
t6 = time()
print(f"Sorting the first {len_bubble / length * 100:.2f}% of the array with bubble sort took {t6-t5:.2f} seconds")

sorted_vector_tim = sorted(vector)
t7 = time()
print(f"Sorting the array with tim sort took {t7-t6:.2f} seconds")

sorted_vectors = {
  'merge': sorted_vector_merge,
  'quick': sorted_vector_quick,
  'tim': sorted_vector_tim
}

for v1, v2 in combinations(sorted_vectors, 2):
  not_string='not '
  if (sorted_vectors[v1] == sorted_vectors[v2]):
    not_string = ''

  print(f'{v1} is {not_string}equal to {v2}')
