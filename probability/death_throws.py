import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

results = Counter()

def check(throws):
    successes = 0
    fails = 0
    turns = 1

    while True:
        new_throw = next(throws)
        if new_throw == 1:
            fails += 2
        elif 1 < new_throw < 10:
            fails += 1
        elif 10 <= new_throw < 20:
            successes += 1
        elif new_throw == 20:
            return (turns, 'Healed')
        
        if fails >= 3:
            return (turns, 'Dead')
        
        if successes >= 3:
            return (turns, 'Stable')
        
        turns += 1
    

for t1 in range(1, 21):
    for t2 in range(1, 21):
        for t3 in range(1, 21):
            for t4 in range(1, 21):
                for t5 in range(1, 21):
                    throws = iter([t1, t2, t3, t4, t5])
                    results[check(throws)] += 1

nums = np.arange(1, 6)

possible_results = ['Healed', 'Dead', 'Stable']
arrays = {r: np.zeros_like(nums) for r in possible_results}

for (t, r), n in results.items():
    arrays[r][t-1] = n

shifts = {'Healed': -1/4, 'Dead': 0, 'Stable': 1/4}
totals = {}

for n, a in arrays.items():
    plt.bar(nums + shifts[n], a, label=n, width=1/4)
    totals[n] = np.sum(a)

plt.xlabel('Turns')
plt.legend()

total = sum(totals.values())
percents = {n: t / total for n, t in totals.items()}
print(percents)