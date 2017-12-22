Documentation for Crop Classification with Multi-Temporal Satellite Imagery
Author: Rose Rustowicz
21 December 2017

Directories:
classifiers -- contains code for classifiers used (softmax regression, SVMs, Neural Network, Convolutional Neural Network)
dataset_construction -- used to download and construct dataset 
evaluation -- used to evaluate further results (most evaluation is done within classifiers)
geojsons -- contains example geojsons

1.) To get the data, use 'dataset_construction/get_crop_data.ipynb'. This is heavily based on 'TheBasics' notebook from Kat Scott's 'Python From Space.' Given an area of interest (AOI) (specified in a .geojson file), this notebook will take you through querying the Planet API, activating and downloading scenes, and clipping downloaded scenes to an AOI.

2.) To download the Crop Data Layer labels, go to 'https://nassgeodata.gmu.edu/CropScape/'. In the top bar, select the US map icon (filled with the US flag pattern), or the icon to the right of that, which you can use to manually select an area of interest. Select a region on that map, making sure that your AOI is within the specified region. Click on the right-most icon (the folder with a green arrow) on the top bar. Download the selected AOI. 

3.) Now that you have downloaded data from CropScape, you need to clip it to the same AOI as in the imagery (from step 1). Open either 'dataset_construction/Crop_CDL_AOIs.ipynb' or 'dataset_construction/clip_CDL.py'. Specify the path to the downloaded CDL labels (from step 2) as 'CDL_fname' in the first line of the notebook. Specify the AOI filename in the second line of the notebook. This should be the same AOI used in step 1. This clipped CDL labels should be saved to the current directory.

4.) You will now create data from the clipped imagery. Open 'dataset_construction/clips_to_datacube.py'. Make sure that all of the clipped imagery from step 1 is saved to a folder, and input that folder as 'imgs_dir' under the first line of the 'main()' function. Specify the filename of the clipped data labels from step 3 as 'labels_fname'. The output will be five files, one datacube for each spectral band: 'b_time.npy', 'g_time.npy', 'r_time.npy', 're_time.npy', and 'nir_time.npy'.

5.) From the large selected scene, we will select the dataset. This step requires some small investigation in order to select the classes for your classification problem. You will be using 'dataset_construction/mk_dataset.py'. Open up this file. Starting in the first line of the 'main' function, specify the filenames (and necessary relative paths) of the files created in step 4. The 'sort_crops' function will print out the top 20 crops in the dataset. It is your decision on which crops to keep. The crop types corresponding to the 'sorted_crops' values can be found in the CDL database, for example here: https://www.nass.usda.gov/Research_and_Science/Cropland/metadata/metadata_ca16.htm, where the values correspond to the 'Attribute Code' column. Select which indices of the top 20 crops you want to keep, and specify those indices within the 'get_masks' function when defining the 'final_mask_xl' variable. Within the 'concat_features' function, you will also need to change the indices of the masks for each crop type. And within 'get_labels', you will need to change the label numbers from Attribute Codes into integer values starting from 0. 'crop_dataset' takes 100000 examples from each class and adds them to the dataset. Feel free to change this number. You now have data and labels for training, validation, and testing.

6.) Now that your data is ready, you can run the classifiers! Go to the 'classifiers/' directory. You will find code for multiclass logistic regression ('softmax_sklearn.py'), support vector machines ('svms_sklearn.py'), a simple neural network ('NN_keras.py'), and a simple Convolutional neural network ('CNN_keras.py'). Make sure that you have the ability to use both scikit learn and keras on the computer you are using. You may need to tune the parameters in each of the classification methods.

A report ('Rustowicz_report.pdf') and poster ('Rustowicz_poster.pdf') for the project are in this repo. A presentation given at Planet can be found here: https://docs.google.com/presentation/d/1T1Z9oj8tk-oCuTmWsDfmd2UGVbT9TlrncC2Mm6dd_O0/edit?usp=sharing
