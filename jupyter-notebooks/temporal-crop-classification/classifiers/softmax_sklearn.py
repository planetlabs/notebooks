# Implementation of softmax regression (multi-class logistic regression) with sklearn

import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import pdb

X_tr = np.load('../../datasets/kings_04_rapideye/train_data.npy')
X_tr = X_tr*1.0/np.max(X_tr)
y_tr = np.load('../../datasets/kings_04_rapideye/train_lbl_sc.npy')

X_val = np.load('../../datasets/kings_04_rapideye/val_data.npy')
X_val = X_val*1.0/np.max(X_val)
y_val = np.load('../../datasets/kings_04_rapideye/val_lbl_sc.npy')

X_test = np.load('../../datasets/kings_04_rapideye/test_data.npy')
X_test = X_test*1.0/np.max(X_test)
y_test = np.load('../../datasets/kings_04_rapideye/test_lbl_sc.npy')

# Define the model, you may need to explore many for the best results.
logreg = linear_model.LogisticRegression(penalty='l2', C=10, solver='saga', max_iter=10000,  multi_class='multinomial')
lr_fit = logreg.fit(X_tr, y_tr)
print(logreg.score(X_tr, y_tr))

predictions = logreg.predict(X_val)
print(logreg.score(X_val, y_val))
print(classification_report(y_val, predictions))

#np.save('logreg_kings04_predictions.npy', predictions)

# Once the model is tuned for best performance, you can also evaluate the test set. 
# If the model performs well on training, but poorly on validation, you have overfit to the training model. 
# If the model performs well on training and validation, but poorly on test, you have overfit to the training and validation model.
# If the model performs similarly on training / val / test but all are poor, your model is not complex enough.
predictions_test = logreg.predict(X_test)
print(logreg.score(X_test, y_test))
print(classification_report(y_test, predictions_test))
