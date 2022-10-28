# Temporal Analysis of Planet Imagery

Planet's daily PlanetScope coverage introduces great potential in temporal analysis.

In this tutorial, we look at the temporal signatures of corn and soybean crops in PlanetScope Orthotiles.
We take advantage of the Cloud-Optimized nature of all
GeoTiffs Planet provides to download only the pixels within the orthotile (and
orthotile unusable data mask). We mask all pixels that are identified as unusable,
then calculate summary statistics on each band.

Please see the [Crop Type Differentiation](croptypedifferentiation.pdf) presentation for a more detailed introduction.
