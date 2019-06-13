import pandas as pd
import numpy as np

data = pd.read_csv('binding_energies.csv', index_col=False)

# intensities = data.iloc[:,2].values
# iarray = []
# for x in intensities:
#     if x:
#         iarray.append(x.strip())
# iarray = list(filter(None, iarray))
# intensities = np.array(iarray, dtype=np.float)

energies = data['Binding/A'].values

even_energies = energies[::2]
