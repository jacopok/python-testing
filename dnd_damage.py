import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

@np.vectorize
def average_damage(damage_modifier, die_damage, attack_modifier, armor_class, base_damage=0):
    hit_die = 20
    hit_damage = damage_modifier + base_damage + die_damage
    damage = 0
    for d in 1+np.arange(hit_die):
        if(d == 20):
            damage += hit_damage + die_damage
        elif(d == 1):
            pass
        elif(d + attack_modifier>=armor_class):
            damage += hit_damage
    return damage / hit_die

ac_array = np.arange(0, 30)

damage_d8 = average_damage(3,  4.5, 5, ac_array)
damage_d6 = average_damage(13, 3.5, 0, ac_array)

plt.plot(ac_array, damage_d6, label = "d6")
plt.plot(ac_array, damage_d8, label = "d8")

plt.ylabel("Danno medio")
plt.xlabel("AC")
plt.legend()
plt.show()
