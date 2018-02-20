# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:22:12 2018

@author: shaox201
"""


import numpy as np
import pandas as pd
import os
import urllib.request
import time
import sklearn
from collections import Counter


os.chdir(r'C:\Users\shaox201\Dropbox\xys\classes\murray2018\FINA8823_ML\input')
#r need to be added here since \u is a mess
#%%
data = pd.read_csv('hfa2011.csv')
y = data['hfa'].as_matrix().reshape(-1, 1)

#x = data.drop('hfa', axis=1).as_matrix()
x = data[['mv','mktbk','sale_growth','roa','cf','tda']].as_matrix()

# use 3 methods for the prediction of targeting

# Multi-layer perception
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

# Gradient Boosting for classification
from sklearn.ensemble import GradientBoostingClassifier
gbdt = GradientBoostingClassifier( n_estimators=100,max_depth=3,random_state=1)

from sklearn.model_selection import KFold


from sklearn.linear_model import LogisticRegression
logit = LogisticRegression(dual=False, tol=0.0001)

kf = KFold(n_splits = 5)
scores = pd.DataFrame(columns=['MLP','GB'])
for train_indices, test_indices in kf.split(x):
        # print("Multi-layer perception Score")
    clf.fit(x[train_indices], y[train_indices])
    clf_score = clf.score(x[test_indices], y[test_indices])
    # print(clf.score(x[test_indices], y[test_indices]))
    
    gbdt.fit(x[train_indices], y[train_indices])
    gb_score = gbdt.score(x[test_indices], y[test_indices])
    # print("Gradient Boosting for classification Score")
    # print(gbdt.score(x[test_indices], y[test_indices]))
    
# =============================================================================
#     logit.fit(x[train_indices], y[train_indices])
#     logit_score = logit.score(x[test_indices], y[test_indices])
# =============================================================================
    # print("Logit Score")
    # print(logit.score(x[test_indices], y[test_indices]))
    
    temp0 = {'MLP': [clf_score], 'GB': [gb_score]}
    temp = pd.DataFrame(data = temp0)
    scores = scores.append(temp, ignore_index=True)   
# =============================================================================
# 
# 
# from numpy import loadtxt
# 
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# # load data
# dataset = loadtxt('pima-indians-diabetes.csv', delimiter=",")
# # split data into X and y
# X = dataset[:,0:8]
# Y = dataset[:,8]
# # split data into train and test sets
# seed = 7
# test_size = 0.33
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
# # fit model no training data
# model = XGBClassifier()
# model.fit(X_train, y_train)
# # make predictions for test data
# y_pred = model.predict(X_test)
# predictions = [round(value) for value in y_pred]
# # evaluate predictions
# accuracy = accuracy_score(y_test, predictions)
# print("Accuracy: %.2f%%" % (accuracy * 100.0))
# =============================================================================
