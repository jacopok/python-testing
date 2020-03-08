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

import sys

if (len(sys.argv)>1):
    file_name = sys.argv[1]
    COUNTRY = file_name
else:
    COUNTRY = 'Italy'

if (len(sys.argv) > 2):
    region = sys.argv[2]
else:
    region = None

IGN_FIRST= 30

base_path = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'

datasets = {
    'Recovered': 'Recovered.csv',
    'Deaths': 'Deaths.csv',
    'Confirmed': 'Confirmed.csv'
}
TS = {}

def get_series(name, country=COUNTRY):

    data = pd.read_csv(base_path + datasets[name])
    if region is not None:
        data_country = data.loc[(data['Country/Region'] == country) & (data['Province/State'] == region)]
    else:
        data_country = data.loc[data['Country/Region']==country]
    timeseries = data_country.iloc[0,4:]

    return (timeseries)

def convert_timeseries(timeseries, name):
    vals = Table(data=[timeseries.values], dtype=[int], names=[name])
    str_times = timeseries.index.values
    times_array = [Time(dt(t)) for t in str_times]
    return(TimeSeries(data=vals, time=times_array))
    # return((times_array, vals))

model = lambda x, C, a: C * np.exp(a * x)
# model = lambda x, C, mean, std: C / np.sqrt(2 * np.pi) / std * np.exp(-(x - mean)** 2 / 2 / std ** 2)
# p0=[1e2, 25, 25]


fig, ax = plt.subplots()

color=iter(cm.rainbow(np.linspace(0,1,3)))
for name in datasets:
    c= next(color)
    timeseries = get_series(name)
    TS[name] = convert_timeseries(timeseries, name)
    numbers = np.arange(0, len(timeseries[IGN_FIRST:]))

    errors = numbers[::-1]+1

    popt, pcov = curve_fit(model, numbers, timeseries[IGN_FIRST:], sigma=errors)
    
    a = un.ufloat(popt[1], pcov[1, 1])
    doubling_time = np.log(2) / a

    plt.semilogy(timeseries[IGN_FIRST:], label=name + f': doubling time = {doubling_time.n:.2f} days', c=c)
    plt.semilogy(numbers, model(numbers, *popt), c=c, linestyle=':')
    next_day_prediction = model(len(timeseries[IGN_FIRST:]), *popt)
    today = (TS[name].time[-1]).strftime('%d %b %Y')
    next_day = (TS[name].time[-1] + 1).strftime('%d %b %Y')
    print(f'Today, {today}, {name} equals: {timeseries[-1]}')
    print(f'Expected {name} for {next_day}: {next_day_prediction:.0f}')

def plot_growth_ratio(name='Confirmed'):
    x = TS[name][name][IGN_FIRST:]
    differences = np.ediff1d(x)
    ratios = differences[1:] / differences[:-1]
    plt.plot(ratios)
    plt.show()

plt.title(COUNTRY + ' contagion spread and exponential fits')

plt.grid('on', which='both')
for label in ax.xaxis.get_ticklabels()[::2]:
    label.set_visible(False)
plt.legend(loc ='upper left')
plt.show()
