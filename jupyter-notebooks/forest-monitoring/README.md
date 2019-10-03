# Forest Monitoring - Road Development

In a region in the Democratic Republic of Congo, road development caused loss
of forests between September and November 2017. In this notebook project,
we demonstrate an end-to-end use case where we have an Area Of Interest (AOI)
and want to detect the deforestation due to road development. 

Because this is a large use case, it is covered in multiple notebooks. Each
notebook is made to work stand-alone but some start with information obtained
and saved in previous notebooks.

The primary workflow for this use case utilizes PSOrthoTiles and is implemented
in the following notebooks, in order:
1. [drc_roads_download](drc_roads_download.ipynb): Find and prepare images that
overlap AOI
1. [drc_roads_classification](drc_roads_classification.ipynb): Classify an image
of the AOI into forest and non-forest regions
1. [drc_roads_temporal_analysis](drc_roads_temporal_analysis.ipynb): Identify
change in the AOI (new roads being built) using temporal analysis. 

The workflow above uses the Unusable Data Mask (UDM) to determine scene quality
and filter out bad pixels. Since that workflow was implemented, the Usable
Data Mask (UDM2) was released. This asset provides additional information on
pixel usability. To assess the impact of UDM2 on forest/non-forest classification,
the entire workflow has been implemented utilizing UDM2 in the following notebook:
* [drc_roads_udm2](drc_roads_udm2.ipynb)

Because UDM2 was just recently released, the notebook had to restrict it's search
to recent imagery, resulting in less useful imagery being found.

Additionally, the entire workflow has been implemented utilizing mosaics and
is implemented in the following notebook:
* [drc_roads_mosaic](drc_roads_mosaic.ipynb)

Change classification results for the PLOrthoTiles and mosaic data inputs are
very promising. With some clean up, we could have a pretty cut and dry change
classification. Classification of forest/non-forest regions was better with
mosaics than PSOrthoTiles. This is likely due to haze in the PSOrthoTiles that
isn't identified in the UDM. Unfortunately, UDM2 did not pick up the haze in the
few available images with UDM2, so classification quality was not improved.
Mosaic pre-processing removes the inconsistencies due to haze and other factors,
which did improve classification quality.


## Techniques Demonstrated

There are many different techniques demonstrated in these notebooks:
1. drc_roads_download: 
    * Identification of PSOrthoTile strips that significantly overlap the AOI
    * Activation and download of PSOrthoTiles as cloud-optimized geotiffs (COGs),
mosaicing into single strip images
    * Use of planet client downloader to activate, download, and mosaic multiple
scenes across multiple strips
1. drc_roads_classification:
    * Classification of an orthotile strip image into forest and non-forest
regions using unsupervised (KMeans) and supervised (Random Forests) techniques 
1. drc_roads_temporal_analysis:
    * Classification of pixels within AOI as change or no change based on
temporal analysis of the forest/non-forest classified imagery
1. drc_roads_mosaic:
    * Re-use of code from other notebooks
    * Activation and download of mosaics using GDAL with the PLMosaic driver
    * Georeferencing and projecting, resampling, and cropping a label image
to match the mosaic
    * Creating a training dataset from a mosaic and a label image
    * Classification of mosaic pixels into forest/non-forest using Random
Forests classifier
    * Classification of forest/non-forest images into change/no-change using
Random Forests classifier
