# Working with Usable Data Mask (UDM2)

These notebooks demonstrate the basics of visualizing and working with the Usable Data Mask (UDM2). Specifications for the UDM2 can be found in the [Imagery Product Spec Sheet](https://assets.planet.com/docs/combined-imagery-product-spec-april-2019.pdf).

The [Usable Data Map (UDM2) Cloud Detection](udm2_clouds.ipynb) notebook demonstrates how to search for images based on cloud content and how to mask images by the cloud band. The [Usable Data Mask (UDM2) Visualization and Masking](udm2.ipynb) notebook demonstrates how to visualize the UDM2 bands and create binary masks based on different criteria.

UDM2 contains the UDM as band 8. If one is only interested in masking out pixels that may have quality issues (e.g. saturation or missing), then the UDM is the best product to use. If pixel content, such as haze, clouds, or cloud shadow, is also a concern, then the UDM2 is the best product to use. More information on the UDM can be found in the [udm folder](../udm/).
