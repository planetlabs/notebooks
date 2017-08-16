# Crop Segmentation and Classification

In this notebook project, we demonstrate and compare techniques for segmentation and classification of crops using Planet imagery. A metric will be established to quantify accuracy of crop classification and will be used to compare technique results.

The notebooks, in order of operations, are:
1. [Identify Datasets](datasets-identify.ipynb): Identify and store ground truth data, area of interest, and Planet scene.
1. [Prepare Datasets](datasets-prepare.ipynb): Crop ground truth data and image to aoi.
2. [KNN Segmentation](segment-knn.ipynb): Segment image into crop/non-crop regions. 

## Usage Notes

This notebook project was developed in a Docker container. This [Dockerfile](Dockerfile) was used to build the image. Alternatively, anaconda environments can be used, to install the dependencies and build the environments using [`root.yml`](root.yml) and [`python2.yml`](python2.yml) (see Dockerfile for an example).
