#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 14:16:37 2019

@author: jacopo
"""

import csv

allowed_letters = set('gfmamglasond')
#initials of names of months

names = []
with open('nomi_italiani.txt', newline='') as inputfile:
    for row in csv.reader(inputfile):
        names.append(row)
#import names from file

names = [item for sublist in names for item in sublist]
#squeezes "names" list of lists
#the for loops are nested implicitly in the array definition

for name in names:
    if(set(name) & allowed_letters == set(name)):
        # "&", when working with sets, implements intersection
        print(name)
#prints only the names whose letters are only those included
#in allowed_letters

