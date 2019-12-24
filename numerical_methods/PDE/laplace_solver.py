import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib import rc
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')

N = 40 # x number of points
M = 50 # y number of points
dimensions = (N, M)

def two_to_one(i, j, N=N):
    return (N * j + i)

def one_to_two(I, N=N):
    return((int(I%N), int(I/N)))

def get_neighbours(I, N=N):
    i, j = one_to_two(I, N)
    return ([(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)])
    
# def create_matrix():
