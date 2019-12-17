import numpy as np

N = 1000
for b in range(1,N):
    for a in range(1,b):
        if((a**b + 1) % (b**a +1) ==0):
            print(np.log(b) / np.log(a))
            # = log_a(b)
