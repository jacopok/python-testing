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

# IGN_FIRST= 30

base_path = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'

datasets = {
    'Recovered': 'Recovered.csv',
    'Deaths': 'Deaths.csv',
    'Confirmed': 'Confirmed.csv'
}
TS = {}

corrected_datum = {
    'Recovered': 1258,
    'Deaths': 1016,
    'Confirmed': 15113
}

def get_series(name, country=COUNTRY):

    data = pd.read_csv(base_path + datasets[name])

    if region is not None:
        data_country = data.loc[(data['Country/Region'] == country) & (data['Province/State'] == region)]
    else:
        data_country = data.loc[data['Country/Region']==country]
    timeseries = data_country.iloc[0, 4:]
    
    if (country == 'Italy'):
        timeseries.loc['3/12/20'] = corrected_datum[name]

    return (timeseries)

IGN_FIRST=0
for name in datasets:
    for i, num in enumerate(get_series(name)):
        if (num == 0):
            IGN_FIRST = max(i, IGN_FIRST)
IGN_FIRST += 1
print(f'No significant infection in the first {IGN_FIRST} days')

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

    fit_succeeded = True
    try:
        popt, pcov = curve_fit(model, numbers, timeseries[IGN_FIRST:], sigma=errors)
    except (RuntimeError):
        fit_succeeded = False

    if(fit_succeeded):
        a = un.ufloat(popt[1], pcov[1, 1])
        doubling_time = np.log(2) / a
        lab = name + f': doubling time = {doubling_time.n:.2f} days'
    else:
        lab = name

    plt.semilogy(timeseries[IGN_FIRST:], label=lab, c=c)
    today = (TS[name].time[-1]).strftime('%d %b %Y')
    next_day = (TS[name].time[-1] + 1).strftime('%d %b %Y')
    next_day_growth_1 = timeseries[-1]*2 - timeseries[-2]
    print(f'Today, {today}, {name} equals: {timeseries[-1]}')
    
    if(fit_succeeded):
        plt.semilogy(numbers, model(numbers, *popt), c=c, linestyle=':')
        next_day_prediction = model(len(timeseries[IGN_FIRST:]), *popt)
    
        print(f'Expected {name} for {next_day}: {next_day_prediction:.0f}')
    
    print(f'{name} for {next_day} needed to have growth factor 1: {next_day_growth_1:.0f}')
    print()

def plot_growth_ratio(name='Confirmed', first=IGN_FIRST, N=4):

    x = TS[name][name][first:]
    if (len(x) - N) < 4:
        print('Not enough data')
        return None 
    differences = np.ediff1d(x)
    ratios = differences[1:] / differences[:-1]
    nums = np.arange(len(ratios))[::-1]
    today = (TS[name].time[-1]).strftime('%d %b %Y')
    
    # geometric running mean: this way, the product of the ratios is closer to being preserved
    ratios_running = np.exp(np.convolve(np.log(ratios), np.ones((N,)) / N, mode='valid'))
    # ratios_running = np.convolve(ratios, np.ones((N,)) / N, mode='valid')

    plt.plot(nums[N-1:], ratios_running)
    a, b = plt.xlim()
    plt.xlim(b, a)
    plt.xlabel(f'Days before {today}')
    plt.ylabel('Growth factor $\\Delta N_d / \\Delta N_{d-1}$'+f', running geometric mean over {N} days')
    plt.axhline(y=1)
    plt.title(f'{COUNTRY} growth factor for {name} numbers')
    plt.show(block=False)
    return(ratios)

plt.title(COUNTRY + ' contagion spread and exponential fits')

plt.grid('on', which='both')
for label in ax.xaxis.get_ticklabels()[::2]:
    label.set_visible(False)
plt.legend(loc ='upper left')
plt.show(block=False)
