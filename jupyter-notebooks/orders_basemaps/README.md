# Ordering Basemaps Using SDK and Requests Library

### About these notebooks

#### Method 1 (recommended): 

[SDK_order_basemaps](SDK_order_basemaps.ipynb) demonstrates using the [SDK](https://github.com/planetlabs/planet-client-python) to order [Planet Basemaps](https://developers.planet.com/docs/data/visual-basemaps/) using both an [AOI](https://developers.planet.com/apis/orders/basemaps/#order-basemaps-by-area-of-interest-aoi) and a [quad ID](https://developers.planet.com/apis/orders/basemaps/#order-basemaps-by-quad-ids-and-deliver-to-cloud). We recommend ordering Planet Basemaps using the SDK as it has ready-made functions to make working with the [Planet Orders API](https://developers.planet.com/apis/orders/) more efficient and less prone to errors. This means less lines of code and less work for you!

#### Method 2: 

[requests_order_basemaps](requests_order_basemaps.ipynb) demonstrates using the [Python Requests library](https://requests.readthedocs.io/en/latest/) to order Basemaps using an AOI and quad IDs.

