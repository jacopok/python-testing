import numpy as np
from scipy.odr import RealData, Model, ODR

N = 1000

x = np.linspace(0, 1, num=N)

error_scale = .01

# valori delle y calcolati con un errore rispetto alle x "vere"
y = 8 * x + 5 + np.random.normal(size=N, scale=error_scale)
# aggiungiamo del rumore anche alle x ora
x += np.random.normal(size=N, scale=error_scale)

# vettori costanti per le deviazioni standard -
# possono essere anche non esserlo
# prova ad aumentare questi valori, e.g. moltiplicarli
# per 1000: vedrai che le stime degli errori alla fine 
# cresceranno un sacco
xerr = np.ones_like(x) * error_scale
yerr = np.ones_like(y) * error_scale

def f(params, x):
    """Modello lineare:
    y = m*x + b, 
    dove params[0] == m
    e params[1] == b
    """
    return params[0]*x + params[1]


linear = Model(f)
data = RealData(x, y, sx=xerr, sy=yerr)
# serve un guess iniziale per i parametri di regressione
odr = ODR(data, linear, beta0=[1., 2.])
output = odr.run()
output.pprint()
