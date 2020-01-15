import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
plt.style.use('default')

y = np.arange(12)
x = 10.0**y

fig, ax=plt.subplots()
ax.plot(x,y)
ax.set_xscale("log")

locmaj = matplotlib.ticker.LogLocator(base=10,numticks=12) 
ax.xaxis.set_major_locator(locmaj)
locmin = matplotlib.ticker.LogLocator(base=10.0,subs=.1*np.arange(1,10),numticks=12)
ax.xaxis.set_minor_locator(locmin)
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
# plt.grid()
plt.show()

# ax.xaxis.set_major_locator(LogLocator(subs=(.2, .5, 1.), base=10,numticks=12))
# ax.xaxis.set_minor_locator(LogLocator(subs=np.arange(1, 10)/10, base=10, numticks=12))
# ax.tick_params(which='minor', width=1, color='black')
# ax.xaxis.set_minor_formatter(NullFormatter())
