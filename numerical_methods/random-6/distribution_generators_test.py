N = int(1e6)
for x in (x1, x2):
    v, b = np.hist(x, bins = 100)
    v = v / (b[1:] - b[:-1])
    bx = (b[1:] + b[:-1] )/ 2
    plt.plot(bx, v/N - pdf(bx))
    