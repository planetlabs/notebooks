# Visualize predicted v. ground truth labels
# This was created to view results from 'main_eval()' output of '../classifiers/CNN_keras.py'
# when applied to the entire dataset, created in 'make_full()' of '../dataset_construction/mk_dataset.py'


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pred_fname = 'classes_ALL_kings04.npy'
truth_fname = '../data/datasets/kings_04_rapideye/ALL_lbls.npy'
data_r = 6306 # 6306 for kings04, 3982 for kings05
data_c = 5512 # 5512 for kings04, 3151 for kings05

# load in predictions and truth labels -- current shape is [data_r*data_c x 1]
preds = np.load(pred_fname)
truth = np.load(truth_fname)

# reshape labels to be the size of the original scene image
preds = np.reshape(preds, newshape=(data_r, data_c))
truth = np.reshape(truth, newshape=(data_r, data_c))

# plot the predictions and truth labels
plt.figure()
plt.imshow(preds)
#plt.savefig('predictions.png')
plt.show()

plt.figure()
plt.imshow(truth)
#plt.savefig('truth.png')
plt.show()
