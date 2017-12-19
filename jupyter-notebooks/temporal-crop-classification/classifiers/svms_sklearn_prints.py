# Implementation of SVMs with sklearn

import numpy as np
import pickle
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

X_tr = np.load('../datasets/kings_04_rapideye/train_data.npy')

X_tr = X_tr*1.0/np.max(X_tr)
y_tr = np.load('../datasets/kings_04_rapideye/train_lbl_sc.npy')
X = X_tr[0:60000,:]
y = y_tr[0:60000]
print(X.shape)
print(y)

X_val = np.load('../datasets/kings_04_rapideye/val_data.npy')
X_val = X_val*1.0/np.max(X_val)
y_val = np.load('../datasets/kings_04_rapideye/val_lbl_sc.npy')
print(X_val.shape)
print(y_val)
print(y_val.shape)

X_test = np.load('../datasets/kings_04_rapideye/test_data.npy')
X_test = X_test*1.0/np.max(X_test)
y_test = np.load('../datasets/kings_04_rapideye/test_lbl_sc.npy')
print(X_test.shape)
print(y_test)
print(y_test.shape)

for C in [1000000]: #[100000, 1000000]:
    for gamma in [0.1]: #[0.001, 0.01]:
        print('---------')
        print('C: , gamma: ')
        print(C, gamma)
        rbf_svc = svm.SVC(kernel='rbf', C=C, gamma=gamma)
        print('.')
        rbf_svc.fit(X, y)  
        print('..')
        y_pred = rbf_svc.predict(X)
        print('Result on training set')
        print(classification_report(y, y_pred))
        print('Acc:')
        print(accuracy_score(y, y_pred))
        y_val_pred = rbf_svc.predict(X_val)
        print('Result on validation set')
        print(classification_report(y_val, y_val_pred))
        print('Acc:')
        print(accuracy_score(y_val, y_val_pred))
        y_test_pred = rbf_svc.predict(X_test)
        print('Result on test set')
        print(classification_report(y_test, y_test_pred))
        print('Acc:')
        print(accuracy_score(y_test, y_test_pred))
        fname = 'svm_kings04_temporal.sav'
        pickle.dump(rbf_svc, open(fname, 'wb'))
