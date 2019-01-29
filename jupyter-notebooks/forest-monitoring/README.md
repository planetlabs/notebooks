# Forest Monitoring - Road Development

In a region in the Democratic Republic of Congo, road development caused loss
of forests between September and November 2017. The goal of these notebooks is
to demonstrate an end-to-end use case where we have an Area Of Interest (AOI)
and want to detect the deforestation due to road development.

Because this is a large use case, it is covered in multiple notebooks. Each
notebook is made to work stand-alone but some start with information obtained
and saved in previous notebooks.

The primary workflow for this use case, in terms of notebooks, is
1. [drc_roads_download](drc_roads_download.ipynb): Find and prepare images that
overlap AOI
1. [drc_roads_classification](drc_roads_classification.ipynb): Classify an image
of the AOI into forest and non-forest regions
1. [drc_roads_temporal_analysis](drc_roads_temporal_analysis.ipnb): Identify
change in the AOI (new roads being built) using temporal analysis. 
 
There are many different techniques demonstrated in these notebooks:
1. drc-roads-download: 
    * Identification of Orthotile strips that significantly overlap the AOI
    * Activation and download of Orthotiles as cloud-optimized geotiffs (COGs),
mosaicing into single strip images
    * Use of planet client downloader to activate, download, and mosaic multiple
scenes across multiple strips
1. drc-roads-classification:
    * Classification of an orthotile strip image into forest and non-forest
regions using unsupervised (KMeans) and supervised (Random Forests) techniques 
1. drs-roads-temporal-analysis:
    * Classification of pixels within AOI as change or no change based on
temporal analysis of the forest/non-forest classified imagery
