import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')


data = pd.read_csv('data.csv', delimiter='  ')

x = data['x'].values
y = data['y'].values

plt.figure(1)
plt.plot(x, y, 'b')
plt.xlabel('x')
plt.ylabel('y')

plt.show()