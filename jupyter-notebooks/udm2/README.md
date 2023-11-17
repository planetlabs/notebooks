# Working with the Unusable Data Mask (UDM) and Usable Data Mask (UDM2)

These notebooks demonstrates the basics of visualizing and working with the Unusable Data Mask (UDM) and Usable Data Mask (UDM2). Specifications for these can be found in the [Imagery Product Spec Sheet](https://assets.planet.com/docs/Planet_Combined_Imagery_Product_Specs_letter_screen.pdf).

If one is only interested in masking out pixels that may have quality issues (e.g. saturation or missing), then the UDM is the best product to use. If pixel content, such as haze, clouds, or cloud shadow, is also a concern, then the UDM2 is the best product to use. UDM2, which is the newer product, contains the UDM as band 8.

The [Usable Data Map (UDM2) Cloud Detection](udm2_clouds.ipynb) notebook demonstrates how to search for images based on cloud content and how to mask images by the cloud band. The [Usable Data Mask (UDM2) Visualization and Masking](udm2.ipynb) notebook demonstrates how to visualize the UDM2 bands and create binary masks based on different criteria. The [Usable Data Mask (UDM2) Cloud Detection within an AOI](udm2_clouds_aoi.ipynb) notebook demonstrates how to search for imagery matching a specific area of interest (AOI).
