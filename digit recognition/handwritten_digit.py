# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 01:59:57 2020

@author: Aviral Gaur
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

my_dataset = pd.read_csv("mnist_train.csv")
#from sklearn.datasets import fetch_mldata
#dataset = fetch_mldata('MNIST original', data_home=data_path)

X = my_dataset.iloc[: ,1:785].values
y = my_dataset.iloc[: ,1].values

some_digit = X[9]
some_digit_image = some_digit.reshape(28, 28)

plt.imshow(some_digit_image, cmap = matplotlib.cm.binary)
plt.show()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

from sklearn.tree import DecisionTreeClassifier
dtf = DecisionTreeClassifier(max_depth = 10)
dtf.fit(X_train, y_train)


dtf.score(X_train, y_train)
dtf.score(X_test, y_test)
dtf.score(X, y)


dtf.predict(X[[0, 4233, 999], 0:784])

















