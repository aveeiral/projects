# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:44:49 2020

@author: Aviral Gaur
"""

"""

step : Maps a unit of time in the real world. In this case 1 step is 1 hour of time.
type : CASH-IN, CASH-OUT, DEBIT, PAYMENT and TRANSFER
amount : amount of the transaction in local currency
nameOrig : customer who started the transaction
oldbalanceOrg : initial balance before the transaction
newbalanceOrig : customer's balance after the transaction.
nameDest : recipient ID of the transaction.
oldbalanceDest : initial recipient balance before the transaction.
newbalanceDest : recipient's balance after the transaction.
isFraud : identifies a fraudulent transaction (1) and non fraudulent (0)
isFlaggedFraud : flags illegal attempts to transfer more than 200.000 in a single transaction.

"""











import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

df = pd.read_csv("crredit_card.csv")

df.info()
df.isnull().values.any()
df["isFlaggedFraud"].value_counts()
df["step"].value_counts()
df["type"].value_counts()

newdata = df.drop(["nameOrig","nameDest"], axis=1)
newdata.info()

#correaltion analysis
corrMatt = newdata[["amount","oldbalanceOrg","newbalanceOrig","oldbalanceDest","newbalanceDest","isFlaggedFraud","isFraud"]].corr()
mask = np.array(corrMatt)
mask[np.tril_indices_from(mask)] = False
fig,ax= plt.subplots()
fig.set_size_inches(20,10)
sn.heatmap(corrMatt, mask=mask,vmax=.8, square=True,annot=True)



X = newdata.iloc[:, [0,1,2,3,4,5,6,8]]

#X = newdata..iloc[["step","type","amount","oldbalanceOrg","newbalanceOrig","oldbalanceDest","newbalanceDest","isFlaggedFraud"]]
y = newdata["isFraud"]



from sklearn.preprocessing import LabelEncoder
lab_X = LabelEncoder()
lab_y = LabelEncoder()

y = lab_y.fit_transform(newdata["isFraud"])


X["type"] = lab_X.fit_transform(X["type"])


from sklearn.preprocessing import OneHotEncoder
one = OneHotEncoder(categorical_features = [1])
X = one.fit_transform(X)
X = X.toarray()


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

from sklearn.naive_bayes import GaussianNB
n_b = GaussianNB()
n_b.fit(X_train, y_train)

n_b.score(X_train, y_train)
n_b.score(X_test, y_test)
n_b.score(X, y)

from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

log_reg.score(X_train, y_train)
log_reg.score(X_test, y_test)
log_reg.score(X, y)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

knn.score(X_train, y_train)
knn.score(X_test, y_test)
knn.score(X, y)

from sklearn.tree import DecisionTreeClassifier
dtf = DecisionTreeClassifier(max_depth=4)
dtf.fit(X_train, y_train)

dtf.score(X_train, y_train)
dtf.score(X_test, y_test)
dtf.score(X, y)

y_pred = dtf.predict(X_test)


from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

sc = (cm[0,0]+cm[1,1] ) / (cm[0,0]+cm[1,1] +cm[1,0]+ cm[0,1])






corrmat = newdata.corr() 
  
f, ax = plt.subplots(figsize =(9, 8)) 
sn.heatmap(corrmat, ax = ax,vmax=.8, cmap ="YlGnBu", linewidths = 0.1,square=True, annot=True) 


plt.figure(figsize = (9, 5)) 
newdata['step'].plot(kind ="hist")


from xgboost import XGBClassifier
from xgboost import plot_importance, to_graphviz

model = XGBClassifier()
model.fit(X_train, y_train)


to_graphviz(model)














