# Implementation of softmax regression (multi-class logistic regression) with sklearn

import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import pdb

X = np.load('../../datasets/kings_04_rapideye/train_data.npy')
X = X*1.0/np.max(X)
y = np.load('../../datasets/kings_04_rapideye/train_lbl_sc.npy')

all_X = np.load('../../datasets/kings_04_rapideye/all_data.npy')
all_X = all_X*1.0/np.max(all_X)
all_y = np.load('../../datasets/kings_04_rapideye/all_lbls.npy')

logreg = linear_model.LogisticRegression(penalty='l2', C=10, solver='saga', max_iter=10000,  multi_class='multinomial')
lr_fit = logreg.fit(X, y)
print(logreg.score(X, y))

predictions = logreg.predict(all_X)
print(logreg.score(all_X, all_y))
print(classification_report(all_y, predictions))

np.save('logreg_kings04_predictions.npy', predictions)

