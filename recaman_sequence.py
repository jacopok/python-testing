import numpy as np

def recaman(n, k=0):
    """
    Returns n values of the Racaman sequence starting at k
    """
    stuck=0
    x = [k]
    s = set(x)

    for i in range(1,n):
        new_m = x[i - 1] - i
        new_p = x[i - 1] + i
        is_pos = bool(new_m >= 0)
        is_free_m = not(new_m in s)
        if (is_pos and is_free_m):
            x.append(new_m)
            s.add(new_m)
        else:
            x.append(new_p)
            s.add(new_p)
        if not(new_p in s):
            stuck+=1
            # print(f"Got stuck starting at {k} after {i} elements.")
    return (x, stuck)
    
from time import time

times=[]
for j in range(0, 10000, 100):
    t1 = time()
    recaman(j)
    t2 = time()
    times.append(t2-t1)