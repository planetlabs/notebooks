# Crop Segmentation and Classification

In these notebooks, we demonstrate segmentation and classification of crops using Planet imagery. 

In [KNN Segmentation](segment-knn.ipynb) a Planet scene is segmented into crop/non-crop regions. The input data and result are georegistered vector features. This notebook contains functionality for converting between vector and raster features, as well as KNN Classification. The data used in KNN Segmentation is prepared in [Identify Datasets](datasets-identify.ipynb), in which the ground truth data, area of interest, and Planet scene are identified and stored, and [Prepare Datasets](datasets-prepare.ipynb), in which the ground truth and image are cropped to the area of interest.

In [Crop Type Classification: CART](classify-cart.ipynb), pixels in a Planet Orthotile are classified as corn, soybean, or neither. This notebook contains functionality for visualizing and processing a UDM into a mask, preparing classification features from the image bands (including NDVI) and training a CART Classifier.
