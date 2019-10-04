#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 17:37:28 2019

@author: jacopo
"""

import numpy as np

total_cost = 530.0

#Fiesso, PN
kids_number_array = np.array([29.0, 18.0])
distance_array = np.array([92.0, 92.0+104.0])

cost_per_kid_per_distance = total_cost / np.dot(kids_number_array, distance_array)

costs_array = cost_per_kid_per_distance * kids_number_array * distance_array

print(costs_array)
