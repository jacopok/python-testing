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

import re

def get_data(filename):

    time_expr = "^  t  = "
    rhalf_expr = "^  kira_rhalf = "

    results = []
    with open(filename) as file:
        t = None
        rhalf = None
        for line in tqdm(file, total=45503380):
                #hardcoded for prettiness in the exam
            if re.search(time_expr, line):
                t = float(line.split(" ")[-1])
            if re.search(rhalf_expr, line):
                rhalf = float(line.split(" ")[-1])
            if (rhalf and t):
                results.append([t, rhalf])
                t = None
                rhalf = None

    return (np.array(results))

def plot_data(results, name):
    times = results[:, 0]
    rhalf = results[:, 1]

    plt.plot(times, rhalf)
    plt.xlabel("times (internal code units)")
    plt.ylabel("rhalf: half-mass radius (\\SI{}{pc})")
    plt.savefig(name, format = 'pdf')

if __name__ == "__main__":
    import os
    import sys
    from tqdm import tqdm

    for x in sys.argv[1:]:
        rawname,ext  = os.path.splitext(x)
        name = rawname + ".pdf"

        results = get_data(x)
        plot_data(results, name)
