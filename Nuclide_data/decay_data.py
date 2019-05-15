import pandas as pd
import numpy as np

data = pd.read_csv('livechart.csv')

intensities = data.iloc[:,2].values
iarray = []
for x in intensities:
    if x:
        iarray.append(x.strip())
iarray = list(filter(None, iarray))
intensities = np.array(iarray, dtype=np.float)