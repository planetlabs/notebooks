# Publish PlanetScope imagery to ArcGIS Online

These notebooks contain samples for publishing PlanetScope imagery as image services in ArcGIS Image for ArcGIS Online.  With Planet imagery published in ArcGIS Online, you are able to:

* Use the imagery in analytics workflows using raster functions or raster analytics
* Access full bit-depth imagery for custom stretching or band combinations performed on the fly
* Securely share imagery with your end-users using the ArcGIS identity, named users, in ArcGIS Online

These script specifically work with PlanetScope 8-band surface reflectance analytic assets, but could be modified to work with additional asset types and sensors.  For example, this could be extended to support Planet Basemaps or SkySat imagery.

### Prerequisites

* Access to the Planet API's (Don't have access? [Sign up for our Developer Trial to get access!](https://developers.planet.com/devtrial/))
* Access to ArcGIS Online with an [ArcGIS Image for ArcGIS Online license](https://www.esri.com/en-us/arcgis/products/arcgis-image/options/arcgis-online)
* A previously placed order for PlanetScope 8-band imagery, either through our [Order's API](https://developers.planet.com/docs/orders/), [ArcGIS Pro Integration](https://developers.planet.com/docs/integrations/arcgis/), or [Explorer](https://www.planet.com/explorer)
* Edit the config.py file in this notebooks folder which is used to store credentials for ArcGIS Online and Planet's platform.

### Multiple Notebook Versions

* Planet to ArcGIS Image using SDKv2 - This notebook uses Planet's new Python SDK for faster and easier access to our API's.  In order to use this, you need to install the SDK: [How to install the Planet SDK for Python v2](https://planet-sdk-for-python-v2.readthedocs.io/en/latest/v2_earlyaccess/).
* Planet to ArcGIS Image using Requests - This notebook uses the python library Requests to make the API calls to Planet's platform.  It will work when run inside of ArcGIS Notebooks, a host Jupyter notebook in ArcGIS Online.
