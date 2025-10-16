# Crop Segmentation

In these notebooks, we demonstrate segmentation of crops using Planet imagery.

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
