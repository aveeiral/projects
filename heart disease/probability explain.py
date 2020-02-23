# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:05:25 2020

@author: Aviral Gaur
"""

import numpy as np
import random as rd
import matplotlib.pyplot as plt


data = []
for i in range(100000):
    data.append(rd.choice([0,1]))
    
    
counta = 0  
countb = 0    
        

plt.hist(data, histtype='barstacked', align='right')
plt.show()

for j in data:
    if j==0:
        counta += 1
    else:
        countb +=1

print(counta)
print(countb)


print("Probability of 0 :", counta / (counta+ countb))
print("Probability of 1 :", countb / (counta + countb))


















