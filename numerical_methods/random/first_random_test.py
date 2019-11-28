"""
Generate N pseudo random numbers
between 0 and 1

Beware to keep N<<m !
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from tqdm import tqdm

N = int(1e8)
a = int(1491385138)
c = int(1587317032)
m = int(1e15)
x=1
results = []

for _ in tqdm(range(N)):
    x = (a * x + c) % m
    results.append(x / m)
    
vals, bins, _ = plt.hist(results, bins=1000)

