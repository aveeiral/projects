# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:23:25 2020

@author: Aviral Gaur
"""

import COVID19Py
import matplotlib.pyplot as plt

covid = COVID19Py.COVID19()
data = covid.getAll(timelines=True)
virusdata = dict(data["latest"])


# for US
location = covid.getLocationByCountryCode("ITA", timelines=True)
deardata = dict(location[0]["latest"])
names = list(deardata.keys())
values = list(deardata.values())


#all world
#names = list(virusdata.keys())
#values = list(virusdata.values())

plt.bar(range(len(virusdata)), values, tick_label = names)
plt.show()

print(virusdata)
