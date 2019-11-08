import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import re


# %% 

def get_data(filename):

    time_expr = "^  t  = "
    rhalf_expr = "^  kira_rhalf = "

    results = []
    with open(filename) as file:
        t = None
        rhalf = None
        for line in tqdm(file):
            if re.search(time_expr, line):
                try:
                    t = float(line.split(" ")[-1])
                except (ValueError):
                    raise (TypeError)
            if re.search(rhalf_expr, line):
                try:
                    rhalf = float(line.split(" ")[-1])
                except (ValueError):
                    raise (TypeError)
            if (rhalf and t):
                results.append([t, rhalf])
                t = None
                rhalf = None

    return (np.array(results))

def plot_data(results, name):
    times = results[:, 0]
    rhalf = results[:, 1]

    plt.plot(times, rhalf)
    plt.xlabel("Times")
    plt.ylabel("rhalf")
    plt.savefig(name, format = 'pdf')
#%%

if __name__ == "__main__":
    import os
    import sys
    from tqdm import tqdm

    for x in sys.argv[1:]:
        rawname,ext  = os.path.splitext(x)
        name = rawname + ".pdf"

        results = get_data(x)
        plot_data(results, name)
