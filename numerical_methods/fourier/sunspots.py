import numpy as np
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
import pandas as pd

sunspots = pd.read_csv('sunspots.txt', sep="\t", names=["Month", "Sunspot number"])

data = sunspots['Sunspot number']

def DFT(data):
  N = len(data)
  