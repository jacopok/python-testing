import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('seaborn')
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
rc('text.latex', preamble=r'''\usepackage{amsmath}
          \usepackage{physics}
          \usepackage{siunitx}
          ''')


MAP = 'seismic'

import matplotlib.collections as mcoll

def multicolored_lines(z, figname=None):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    """


    theta = np.linspace(0, 2*np.pi, num=400)
    x = np.cos(theta)
    y = np.sin(theta)
    fig, ax = plt.subplots()
    lc = colorline(x, y, z=z(x), cmap=MAP)
    plt.colorbar(lc)
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    if(figname):
        plt.savefig(figname + '.pdf', format = 'pdf')
    else:
        plt.show()

def colorline(
        x, y, z=None, cmap='copper', norm=plt.Normalize(-1.0, 1.0),
        linewidth=3, alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    # to check for numerical input -- this is a hack
    if not hasattr(z, "__iter__"):
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc

def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

multicolored_lines(lambda x:(5*x**3 - 3*x)/2, figname = 'nth_moment')
