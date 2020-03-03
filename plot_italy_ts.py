import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from astropy.time import Time
from astropy.timeseries import TimeSeries
from astropy.table import Table
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import cm
import uncertainties as un

dt = lambda t : Time(datetime.strptime(t, '%m/%d/%y'))

# import sys
# file_name = sys.argv[1]

COUNTRY = 'Italy'
IGN_FIRST= 31

base_path = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'

datasets = {
    'Recovered': 'Recovered.csv',
    'Deaths': 'Deaths.csv',
    'Confirmed': 'Confirmed.csv'
}
TS = {}

def get_series(name, country=COUNTRY):

    data = pd.read_csv(base_path + datasets[name])
    italy = data.loc[data['Country/Region']==country]
    timeseries = italy.iloc[0,4:]

    return (timeseries)

def convert_timeseries(timeseries, name):
    vals = Table(data=[timeseries.values], dtype=[int], names=[name])
    str_times = timeseries.index.values
    times_array = [Time(dt(t)) for t in str_times]
    return(TimeSeries(data=vals, time=times_array))
    # return((times_array, vals))

model = lambda x, C, a : C * np.exp(a*x)

fig, ax = plt.subplots()

color=iter(cm.rainbow(np.linspace(0,1,3)))
for name in datasets:
    c= next(color)
    timeseries = get_series(name)
    TS[name] = convert_timeseries(timeseries, name)
    numbers = np.arange(0,len(timeseries[IGN_FIRST:]))
    popt, pcov = curve_fit(model, numbers, timeseries[IGN_FIRST:])
    
    a = un.ufloat(popt[1], pcov[1, 1])
    doubling_time = np.log(2) / a

    plt.semilogy(timeseries[IGN_FIRST:], label=name + f': doubling time = {doubling_time.n:.2f} days', c=c)
    plt.semilogy(numbers, model(numbers, *popt), c=c, linestyle=':')

plt.grid('on', which='both')
for label in ax.xaxis.get_ticklabels()[::2]:
    label.set_visible(False)
plt.legend(loc ='upper left')
plt.show()
