# This script uses the Sequential model within Keras to implement 
# a simple one-hidden-layer neural network. Tune parameters for best performance. 

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import regularizers
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from keras.constraints import maxnorm
from sklearn.model_selection import GridSearchCV
import numpy as np
import pdb

np.random.seed(10) # for reproducability

def load_data():
    # Load train, validation, and test data
    X = np.load('../datasets/kings_05_rapideye/train_data_single.npy')
    X = X*1.0/np.max(X)
    y = np.load('../datasets/kings_05_rapideye/train_lbl_sc.npy')
    y = np_utils.to_categorical(y)

    X_dev = np.load('../datasets/kings_05_rapideye/val_data_single.npy')
    X_dev = X_dev*1.0/np.max(X_dev)
    y_dev = np.load('../datasets/kings_05_rapideye/val_lbl_sc.npy')
    y_dev = np_utils.to_categorical(y_dev)

    X_test = np.load('../datasets/kings_05_rapideye/test_data_single.npy')
    X_test = X_test*1.0/np.max(X_test)
    y_test = np.load('../datasets/kings_05_rapideye/test_lbl_sc.npy')
    y_test = np_utils.to_categorical(y_test)
    return X, y, X_dev, y_dev, X_test, y_test

def create_model(units, activation, loss, optimizer, metrics, reg, dropout_rate, weight_constraint):
    # Define model as a sequence of layers; Dense models are fully-connected models
    model = Sequential()
    # Mono-temporal has 5 features (1 timestamp x 5 spectral bands)
    model.add(Dense(units=units, input_dim=5, activation=activation, kernel_regularizer=regularizers.l2(reg), kernel_constraint=maxnorm(weight_constraint)))
    # Scene 1 has 75 features (15 timestamps x 5 spectral bands)
    #model.add(Dense(units=units, input_dim=75, activation=activation, kernel_regularizer=regularizers.l2(reg), kernel_constraint=maxnorm(weight_constraint)))
    # Scene 2 has 105 features (21 timestamps x 5 spectral bands)
    #model.add(Dense(units=units, input_dim=105, activation=activation, kernel_regularizer=regularizers.l2(reg), kernel_constraint=maxnorm(weight_constraint)))
    model.add(Dropout(dropout_rate))
    # Scene 1 has 6 output classes
    #model.add(Dense(6, activation='softmax'))
    # Scene 2 has 9 output classes
    model.add(Dense(9, activation='softmax'))
    model.compile(optimizer, loss, metrics)
    return model

def fit_model(model, X, y, epochs=30, batch_size=1000):
    # Fit the model
    return model.fit(X, y, epochs, batch_size)

def evaluate_model(model, X, y, X_dev, y_dev, X_test, y_test):
    # Evaluate the model
    scores = model.evaluate(X, y)
    print('\n%s: %.2f%%' % (model.metrics_names[1], scores[1]*100))
    val_scores = model.evaluate(X_dev, y_dev)
    print('\n%s: %.2f%%' % (model.metrics_names[1], val_scores[1]*100))
    test_scores = model.evaluate(X_test, y_test)
    print('\n%s: %.2f%%' % (model.metrics_names[1], test_scores[1]*100))
    return scores, val_scores, test_scores

def predict(model, X, y, X_dev, y_dev, X_test, y_test):
    # Make predictions
    pred_y = model.predict(X)
    pred_y_dev = model.predict(X_dev)
    pred_y_test = model.predict(X_test)
    return pred_y, pred_y_dev, pred_y_test

def main():
    X, y, X_dev, y_dev, X_test, y_test = load_data()
    
    for units in [200]:
        model = create_model(units=units, activation='relu', loss='categorical_crossentropy', optimizer='Adadelta', 
            metrics=['accuracy'], reg=0.00001, dropout_rate=0.1, weight_constraint=5) #, verbose=0)
        print('------------------------')
        for epoch in [50, 100]:
            for batch in [1000]:
                print('batch: %s' % (batch))
                print('epoch: %s' % (epoch))
                model.fit(X, y, batch, epoch)
                scores, val_scores, test_score = evaluate_model(model, X, y, X_dev, y_dev, X_test, y_test)

if __name__ == '__main__':
    main()
