#Importing Required Libraries
import numpy as np #For Mathamatical Calculations
import pandas as pd #For Handling datasets
import matplotlib.pyplot as plt #For plotting Graphs

#Import dataset
dataset = pd.read_csv('blood_csv.csv') #Import csv file
X = dataset.iloc[:, 1].values #Locating Values in X direction
y = dataset.iloc[:, 2].values #Locating values in y direction
X = X.reshape(-1, 1) #Rearranging the data

plt.scatter(X, y) #Plotting the graph
plt.show() #Shows how the graph plotted



#Import SKLEARN library for Training and Testing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)#Preparing to train and test the data

#Import SKLEARN library for Linear Regression
from sklearn.linear_model import LinearRegression
#Train the model
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

y_pred = lin_reg.predict(X_test)#For predicting the values

#Plotting graph with Predicted values for Training set

plt.scatter(X_train, y_train)#Plot the training data
plt.plot(X_train, lin_reg.predict(X_train), c = "r")#Plots the best fit line using predicted values
plt.xlabel('Age') #Label denotes X axis
plt.ylabel('Systolic Blood Pressure') #Label denotes y axis
plt.title('ML Model to Predict Blood Pressure from Age (Training Set)') #Title of the Graph
plt.show()#Shows how the graph plotted

#Plotting graph with Predicted values for Test set

plt.scatter(X_test, y_test)#Plot the training data
plt.plot(X_test, lin_reg.predict(X_test), c = "r")#Plots the best fit line using predicted values
plt.xlabel('Age')#Label denotes X axis
plt.ylabel('Systolic Blood Pressure') #Label denotes y axis
plt.title('ML Model to Predict Blood Pressure from Age (Test Set)') #Title of the Graph
plt.show()#Shows how the graph plotted

lin_reg.predict([[11]])#Test the model with predicted value

#Instead of using prediction we use Score to generate many different types of new values
lin_reg.score(X_train, y_train)   
lin_reg.score(X_test, y_test) 
lin_reg.score(X, y) 

 