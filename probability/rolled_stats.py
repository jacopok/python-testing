#%%
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def RollNDice(n):
    return np.random.randint(1,7,n)
    
def Roll3D6():
    return sum(RollNDice(3))

def Roll4D6D1():
    rolls = RollNDice(4)
    rolls = np.delete(rolls, rolls.argmin()) # delete lowest value
    return sum(rolls)

PointBuyValue = {
    3: -9,
    4: -6,
    5: -4,
    6: -2,
    7: -1,
    8: 0,
    9: 1,
    10: 2,
    11: 3,
    12: 4,
    13: 5,
    14: 7,
    15: 9,
    16: 12,
    17: 15,
    18: 19
}

def RollStats4D6D1():
    return [Roll4D6D1() for _ in range(6)]

def RollStats3D6():
    return [Roll3D6() for _ in range(6)]

def CalculatePointBuy(stats):
    return sum(PointBuyValue[stat] for stat in stats)

def Choose4D6D1():
    pb_max = 0
    for _ in range(4):
        pb = CalculatePointBuy(RollStats4D6D1())
        if pb > pb_max:
            pb_max = pb
    return pb_max


def Choose3D6():
    pb_max = 0
    for _ in range(4):
        pb = CalculatePointBuy(RollStats3D6())
        if pb > pb_max:
            pb_max = pb
    return pb_max

#%%
np.random.seed(42)

n_sims = 10000
record_4d6d1 = []
record_3d6 = []
record_pick4d6d1 = []
record_pick3d6 = []

for _ in range(n_sims):
    record_4d6d1.append(CalculatePointBuy(RollStats4D6D1()))
    record_3d6.append(CalculatePointBuy(RollStats3D6()))
    record_pick4d6d1.append(Choose4D6D1())
    record_pick3d6.append(Choose3D6())

print ("Average Point buy (4d6d1): %.2f" % (np.sum(record_4d6d1)/n_sims))
print ("Average Point buy (3d6): %.2f" % (np.sum(record_3d6)/n_sims))
print ("Average Point buy (Choose 4d6d1): %.2f" %
        (np.sum(record_pick4d6d1)/n_sims))
print ("Average Point buy (Choose 3d6): %.2f" %
        (np.sum(record_pick3d6)/n_sims))

ax = sns.distplot(record_4d6d1, bins=100)
plt.title("Histogram of %d simulated rolls" % n_sims)
ax.set_xlabel("Point Buy Total")
ax.set_ylabel("Count")

sns.distplot(record_3d6, bins=100)
sns.distplot(record_pick4d6d1, bins=100)
sns.distplot(record_pick3d6, bins=100)
plt.legend(labels=['4d6d1', '3d6', 'Choose 4d6d1', 'Choose 3d6'])

# %%
