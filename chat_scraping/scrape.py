from datetime import datetime

filename = 'history.txt'

participants_kws = ['Partecipanti:', 'CONTEGGIO PERSONE COINVOLTE', ]

participant_dict = {}
tmp = []

reading = False

with open(filename) as f:
    
    for row in f:        
        srow = row.rstrip()  # remove trailing newline
        if reading:            
            try:
                date_str = srow.split(',')[0].split('/')
                date_ymd = [int(t) for t in reversed(date_str)]
                date = datetime(*date_ymd)
                participant_dict[date.isoformat()] = tmp
                tmp = []
                reading = False
            except(ValueError):
                pass
        
        if reading and srow:
            tmp.append(srow)
        
        if srow in participants_kws:
            reading = True

from collections import Counter

c = Counter()

for parts in participant_dict.values():
    for p in parts:
        c[p] += 1

print(c)