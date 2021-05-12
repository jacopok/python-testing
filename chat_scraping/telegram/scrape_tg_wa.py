#%%
import json
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


def dict_from_file_tg(fname):
    message_senttimes = defaultdict(list)

    tg_json = json.loads(fname.read_bytes())

    for message in tg_json['messages']:
        dateandtime = datetime.fromisoformat(message['date'])
        
        try:
            message_senttimes[message['from']].append(dateandtime)
        except KeyError:
            message_senttimes[message['actor']].append(dateandtime)
    
    return {
        k: v
        for k, v in message_senttimes.items()
        if len(v) > 1
    }
    

def dict_from_file_wa(fname):
    message_senttimes = defaultdict(list)

    with open(fname) as f:
        for row in f.readlines():
            try:
                date, name = row.split(': ')[0].split(' - ')
                dateandtime = datetime.strptime(date, '%d/%m/%Y, %H:%M')
            except(ValueError):
                continue
                
            message_senttimes[name].append(dateandtime)
    
    return {
        k: v
        for k, v in message_senttimes.items()
        if len(v) > 1
    }

# %%


def messaged_first(message_senttimes, hours_thr):

    names = list(message_senttimes.keys())
    times_list = [message_senttimes[name] for name in names]

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

    names = list(message_senttimes.keys())
    times_list = [message_senttimes[name] for name in names]

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


possible_thrs = np.geomspace(3/60, 24 * 30, num=100)

def make_plot(senttimes: dict, them, possible_thrs=possible_thrs):
    
    plt.figure(dpi=200)
    
    for label, times in senttimes.items():
        ratios = np.array([
            ratio(messaged_first(times, dh), them=them)
            for dh in possible_thrs
        ])

        mask = [r is not np.nan for r in ratios]

        ratios = ratios[mask]

        possible_thrs = possible_thrs[mask]

        # plt.errorbar(possible_thrs,
        #     [r.n for r in ratios],
        #     label=label,
        #     )
        
        y = np.array([r.n for r in ratios])
        yerr = np.array([r.s for r in ratios])
        
        l = plt.plot(possible_thrs,
            y,
            label=label,
            )
            
        plt.fill_between(possible_thrs, y - yerr, y + yerr,
                 color=l[0].get_color(), alpha=0.2)

    
    # plt.errorbar(possible_thrs,
    #     [r.n for r in ratios2],
    #     yerr=[r.s for r in ratios2],
    #     c='blue', label='Last message')

    plt.plot(possible_thrs, np.full_like(possible_thrs, .5), ls=':', c='black')
    plt.xscale('log')

    plt.gca().set_xticks([5/60, 1, 24, 24*7])
    plt.gca().set_xticklabels(['5 minutes', '1 hour', '1 day', '1 week'])
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.))
    plt.grid()
    plt.legend(loc='lower left')

    plt.title(f'Chat with {them}')

    plt.xlabel('Time from the last message')
    plt.ylabel('Percent of the time I (re)started the conversation')


# %%

them = ''

wa_filename = datafolder / f'WhatsApp Chat with {them}.txt'
wa = dict_from_file_wa(wa_filename)

tg_filename = datafolder / f'{them}.json'
tg = dict_from_file_tg(tg_filename)

comb = {k: tg[k] + wa[k] for k in tg}

make_plot(
    {
        'whatsapp': wa,
        'telegram': tg,
        'combined': comb
    },
    them=them
)
# %%
