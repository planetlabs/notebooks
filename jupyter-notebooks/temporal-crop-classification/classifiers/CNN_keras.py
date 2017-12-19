# Implementation of a CNN using Keras

import numpy as np
import pdb
import os
import itertools
import matplotlib.pyplot as plt
import matplotlib

from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten
from keras import regularizers
from keras.utils import np_utils

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

np.random.seed(10)

def load_data():
    # Load train, validation, and test data
    X = np.load('../datasets/kings_04_rapideye/train_data_single.npy')
    X = X*1.0/np.max(X)
    X = np.expand_dims(X, axis=2)
    y = np.load('../datasets/kings_04_rapideye/train_lbl_sc.npy')
    y = np_utils.to_categorical(y)

    X_val = np.load('../datasets/kings_04_rapideye/val_data_single.npy')
    X_val = X_val*1.0/np.max(X_val)
    X_val = np.expand_dims(X_val, axis=2)
    y_val = np.load('../datasets/kings_04_rapideye/val_lbl_sc.npy')
    y_val = np_utils.to_categorical(y_val)

    X_test = np.load('../datasets/kings_04_rapideye/test_data_single.npy')
    X_test = X_test*1.0/np.max(X_test)
    X_test = np.expand_dims(X_test, axis=2)
    y_test = np.load('../datasets/kings_04_rapideye/test_lbl_sc.npy')
    y_test = np_utils.to_categorical(y_test)
    return X, y, X_val, y_val, X_test, y_test

def load_model(json_fname, h5_fname):
    # Loads model if stored as a json and h5 files
    json_file = open(json_fname, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # Load weights into the new model
    loaded_model.load_weights(h5_fname)
    print('Loaded model from disk.')
    return loaded_model

def evaluate_loaded_model(loaded_model, X_test, y_test):
    # Evaluate saved model
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    score = loaded_model.evaluate(X_test, y_test, verbose=0)
    print('%s: %.2f%%' % (loaded_model.metrics_names[1], score[1]*100))

def create_model(num_classes):
    # Define the model with the Keras Sequential modeling framework
    model = Sequential()
   
    #model.add(Conv1D(32, kernel_size=5, strides=1, activation='relu', input_shape=(105,1)))
    model.add(Conv1D(8, kernel_size=3, strides=1, activation='relu', input_shape=(5,1)))
    #model.add(MaxPooling1D(pool_size=2, strides=2))
    #model.add(Conv1D(64, 5, activation='relu'))
    model.add(Conv1D(16, 3, activation='relu'))
    #model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    #model.add(Dense(1000, activation='relu'))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    # Use sklearn to show the confusion matrix
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized Confusion Matrix")
    else:
        print("Confusion Matrix, Without Normalization")

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                horizontalalignment='center',
                color='white' if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def main():
    num_classes = 6
    X, y, X_val, y_val, X_test, y_test = load_data()
    model = create_model(num_classes)
    model.fit(X, y, batch_size=100, epochs=10, verbose=1) #, callbacks=[history])

    # Show results
    score_tr = model.evaluate(X, y, verbose=1)
    print('Train loss: ', score_tr[0])
    print('Train accuracy: ', score_tr[1])

    score_val = model.evaluate(X_val, y_val, verbose=1)
    print('Val loss: ', score_val[0])
    print('Val accuracy: ', score_val[1])

    score_test = model.evaluate(X_test, y_test, verbose=1)
    print('Val loss: ', score_test[0])
    print('Val accuracy: ', score_test[1])
    
    # Serialize to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")
    print("Saved model to disk")

def main_eval():
    json_fname = 'model_10epoch_kings04.json'
    h5_fname = 'model_10epoch_kings04.h5'

    #X_test = np.load('../datasets/kings_04_rapideye/test_data_single.npy')
    X_test = np.load('../datasets/kings_04_rapideye/TEST_SUB_data_kings04.npy')
    X_test = X_test * 1.0 / np.max(X_test)
    X_test = np.expand_dims(X_test, axis=2)
    #y_test_orig = np.load('../datasets/kings_04_rapideye/test_lbl_sc.npy')
    y_test_orig = np.load('../datasets/kings_04_rapideye/TEST_SUB_lbls_kings04.npy')
    y_test = np_utils.to_categorical(y_test_orig)
    y_test = np.append(y_test, np.zeros((1950000,1)), axis=1)

    # Load and evaluate model
    loaded_model = load_model(json_fname, h5_fname)
    evaluate_loaded_model(loaded_model, X_test, y_test)

    y_pred = loaded_model.predict(X_test)
    print('Y PRED SIZE: ')
    print(y_pred.shape)
    print(y_pred[1,:])
    classes = np.argmax(y_pred, 1)
    print(classes.shape)
    print(classes[0:10])
    print(y_test_orig[0:10])

    cnf_matrix = confusion_matrix(y_test_orig, classes)
    print(cnf_matrix)
    print('-----------------')
    print(classification_report(y_test_orig, classes))
    
    class_names = ['cotton', 'safflower', 'tomatoes', 'wintwheat', 'durwheat', 'idle']
    #class_names = ['wintwht/corn', 'alfalfa', 'almonds', 'pistachios', 'idle', 'corn', 'walnuts', 'cotton', 'wintwheat']
    plt.figure() #figsize=(8.5,7))
    #plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True, title='Scene #1 Multi-Temporal Confusion Matrix')
    #plt.show()
    matplotlib.rcParams.update({'font.size': 40})
    plt.savefig('Scene1_confmat_TESTBLOCK.png')

if __name__ == '__main__':
    #main()
    main_eval()
