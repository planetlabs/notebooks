# Forest Monitoring - Road Development

In a region in the Democratic Republic of Congo, road development caused loss
of forests between September and November 2017. The goal of these notebooks is
to demonstrate an end-to-end use case where we have an Area Of Interest (AOI)
and want to detect the deforestation due to road development.

Because this is a large use case, it is covered in multiple notebooks. Each
notebook is made to work stand-alone but starts with information obtained and saved
in previous notebooks.

There are many different techniques demonstrated in these notebooks:
1. drc-roads-download: 
    * Identification of Orthotile strips that significantly overlap the AOI
    * Activation and download of Orthotiles, mosaicing into single strip images
    * Use of planet client downloader to activate, download, and mosaic multiple
scenes across multiple strips
1. drc-roads-classification:
    * Analysis of an orthotile image to identify forest loss to road development
1. drs-roads-temporal-analysis:
    * Temporal analysis of multiple orthotile images to identify when road
development occurs 
