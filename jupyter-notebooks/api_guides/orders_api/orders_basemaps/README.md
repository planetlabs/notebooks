# Ordering Mosaics Using SDK and Requests Library

### About these notebooks

#### Method 1 (recommended): 

[SDK_order_basemaps](SDK_order_basemaps.ipynb) demonstrates using the [SDK](https://github.com/planetlabs/planet-client-python) to order [PlanetScope Mosaics](https://docs.planet.com/data/imagery/basemaps/visual/) using both an [AOI](https://docs.planet.com/develop/apis/orders/sources/#by-geometry) and a [quad ID](https://docs.planet.com/develop/apis/orders/sources/#by-quad-id). We recommend ordering PlanetScope Mosaics using the SDK as it has ready-made functions to make working with the [Planet Orders API](https://docs.planet.com/develop/apis/orders/) more efficient and less prone to errors. This means less lines of code and less work for you!

#### Method 2: 

[requests_order_basemaps](requests_order_basemaps.ipynb) demonstrates using the [Python Requests library](https://requests.readthedocs.io/en/latest/) to order Mosaics using an AOI and quad IDs.

