#%%
from bs4 import BeautifulSoup
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import numpy as np
import uncertainties as un
from uncertainties import unumpy

datafolder = Path(__file__).parent / 'data'

def filename(i):
    return datafolder / f'messages{i}.html'

# The first messages html file should be renamed to "messages1"
# for this to work


def counter():
    i = 1
    while True: 
        yield i
        i += 1

data = ''
for i in counter():
    try:
        with open(filename(i)) as f:
            data += f.read()
    except (FileNotFoundError):
        break

parsed_html = BeautifulSoup(data)


message_senttimes = defaultdict(list)

for message in parsed_html.body.find_all('div', class_="message default clearfix"):
    date = message.find('div', class_="date")
    name = message.find('div', class_="from_name")
    
    date_time_obj = datetime.strptime(date['title'], '%d.%m.%Y %H:%M:%S')
    message_senttimes[name.text.strip()].append(date_time_obj)

# %%

plt.figure(dpi=200)
names = list(message_senttimes.keys())

times_list = [message_senttimes[name] for name in names]
plt.hist(times_list, bins=150, stacked=True, label=names)
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.legend()

# %%

def messaged_first(message_senttimes, hours_thr):

    all_times = sorted([time for sublist in times_list for time in sublist])
    counter = Counter()
    
    for t1, t2 in zip(all_times[:-1], all_times[1:]):
        hours = (t2 - t1) / timedelta(hours=1)
        if hours > hours_thr:
            for name, t_list in message_senttimes.items():
                if t2 in t_list:
                    counter[name] += 1

    return (counter)

def messaged_last(message_senttimes, hours_thr):

    all_times = sorted([time for sublist in times_list for time in sublist])
    counter = Counter()
    
    for t1, t2 in zip(all_times[:-1], all_times[1:]):
        hours = (t2 - t1) / timedelta(hours=1)
        if hours > hours_thr:
            for name, t_list in message_senttimes.items():
                if t1 in t_list:
                    counter[name] += 1

    return (counter)


def poisson_err(n):
    return un.ufloat(n, np.sqrt(n))

def ratio(counter, them, me='Jacopo Tissino'):
    n1 = poisson_err(counter[them])
    n2 = poisson_err(counter[me])
    try:
        return n2 / (n1 + n2)
    except(ZeroDivisionError):
        return np.nan


possible_thrs = np.geomspace(3/60, 24 * 30)

them = 'Leonardo Zampieri'

ratios = np.array([
    ratio(messaged_first(message_senttimes, dh), them=them)
    for dh in possible_thrs
])

ratios2 = np.array([
    ratio(messaged_last(message_senttimes, dh), them=them)
    for dh in possible_thrs
])

mask = [r is not np.nan for r in ratios]

ratios = ratios[mask]
ratios2 = ratios2[mask]

possible_thrs = possible_thrs[mask]


plt.figure(dpi=200)
plt.errorbar(possible_thrs,
    [r.n for r in ratios],
    yerr=[r.s for r in ratios],
    c='black', label='First message')
    
plt.errorbar(possible_thrs,
    [r.n for r in ratios2],
    yerr=[r.s for r in ratios2],
    c='blue', label='Last message')

plt.plot(possible_thrs, np.full_like(possible_thrs, .5), ls=':', c='black')
plt.xscale('log')

plt.gca().set_xticks([5/60, 1, 24, 24*7])
plt.gca().set_xticklabels(['5 minutes', '1 hour', '1 day', '1 week'])
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.))
plt.grid()
plt.legend(loc='lower left')

plt.title(f'Chat with {them} on telegram')

plt.xlabel('Time from the last message')
plt.ylabel('Percent of the time I (re)started the conversation')

# %%
