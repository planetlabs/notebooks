# Crop Segmentation and Classification

In these notebooks, we demonstrate segmentation and classification of crops using Planet imagery.

* **Crop Segmentation**
  - [Identify Datasets](crop-segmentation/1-datasets-identify.ipynb)
      - Ground truth data, area of interest, and Planet scene are identified and stored.
  - [Prepare Datasets](crop-segmentation/2-datasets-prepare.ipynb)
      - Ground truth and image are cropped to the area of interest.
  - [KNN Segmentation](crop-segmentation/3-segment-knn.ipynb)
      - A Planet scene is segmented into crop/non-crop regions. 
      - The input data and result are georegistered vector features. 
      - This notebook contains functionality for converting between vector and raster features, as well as KNN Classification.
  - [KNN Segmentation](crop-segmentation/4-segment-knn-tuning.ipynb)
      - The KNN Segmentation Parameters are tuned.
      
* **Crop Classification**
  - [Crop Type Classification: Prepare CDL Data](crop-classification/1-datasets-prepare-cdl.ipynb)
      - Pixels in a Planet PSScene image are classified as corn, soybean, or neither.
      - This notebook contains functionality for visualizing and processing a UDM into a mask, preparing classification features from the image bands (including NDVI) and training a CART Classifier.
  - [Crop Type Classification: CART](crop-classification/2-classify-cart.ipynb)
      - Pixels in a Planet PSScene image are classified as corn, soybean, or neither.
      - This notebook contains functionality for visualizing and processing a UDM into a mask, preparing classification features from the image bands (including NDVI) and training a CART Classifier.
  - [Crop Type Classification: CART L8 and PS](crop-classification/3-classify-cart-l8-ps.ipynb)
      - This notebook is a continuation of Crop Type Classification: CART in which we use Landsat8 as well as PSScene data to generate features for CART classification.