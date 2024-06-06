# Temporal Analysis of Planet Imagery

Planet's daily PlanetScope coverage introduces great potential in temporal analysis.

In this tutorial, we look at the temporal signatures of corn and soybean crops.
We first define areas of interest for each crop in a group of corn and soybean
crops. Then, for each crop, we search for the PSScene imagery that covers
that area of interest. We take advantage of the Cloud-Optimized nature of all
GeoTiffs Planet provides to download only the pixels within the image (and
the unusable data mask). We mask all pixels that are identified as unusable,
then calculate summary statistics on each band.

For each crop region, we will have 4 sets of summary statistics for each image,
multiplied by the number of images per region.
