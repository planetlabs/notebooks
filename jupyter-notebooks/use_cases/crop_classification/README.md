# Crop Classification

In these notebooks, we demonstrate  classification of crops using Planet imagery.

* **Crop Classification**
  - [Crop Type Classification: Prepare CDL Data](crop-classification/1-datasets-prepare-cdl.ipynb)
      - Prepare the data needed for this crop classification example.
  - [Crop Type Classification: CART](crop-classification/2-classify-cart.ipynb)
      - Pixels in a Planet PSScene image are classified as corn, soybean, or neither.
      - This notebook contains functionality for visualizing and processing a UDM into a mask, preparing classification features from the image bands (including NDVI) and training a CART Classifier.
  - [Crop Type Classification: CART L8 and PS](crop-classification/3-classify-cart-l8-ps.ipynb)
      - This notebook is a continuation of Crop Type Classification: CART in which we use Landsat8 as well as PSScene data to generate features for CART classification.