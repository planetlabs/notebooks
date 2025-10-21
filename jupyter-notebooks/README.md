# Planet Jupyter Notebooks Examples

This repository contains a collection Jupyter notebooks that teach you how to use Planet Insights Platform. They are divided into three folders:

1. `api_guides` - Here, you will find notebooks that introduce you to the essential functionality of different APIs with quickstarts to guides focused on specific functionality.
2. `use_cases` - In the use cases section, we've built notebooks around common applications of satellite data to demonstrate how to answer questions or create insights from Earth observation data.
3. `workflows` - Here we cover foundational workflows of how to use Planet Insights Platform as well as common patterns of analyzing, processing, or integrating data with other software. Workflows are typically building blocks that you might use to accomplish different tasks you are working on.

## Table of Contents

### API Guides

| Folder | Description |
| ------ | ----------- |
| [Analytics API](api_guides/analytics_api) | Use Planet Analytics API to map flood and displacement in Syria. |
| [Analytics API - Quickstart](api_guides/analytics_api/quickstart) | Describes available Analytics Feeds and Subscriptions with the Planet Analytics API. |
| [Analytics API - User-Guide](api_guides/analytics_api/user-guide) | Accessing Planet Analytics API to build applications. |
| [Basemaps API](api_guides/basemaps_api) | Utilize the Basemaps API to access and download basemap data and metadata. |
| [Batch Processing API](api_guides/batch_processing_api) | BatchV2 API Demo for Planet Labs |
| [Data API](api_guides/data_api) | Access sub-regions of interest within Planet assets. |
| [Features API](api_guides/features_api) | Introduces Planet Features API for creating and using AOI references across Planet APIs. |
| [Orders API](api_guides/orders_api) | Uses Planet's Orders API with the official Python client. |
| [Orders API - Orders Basemaps](api_guides/orders_api/orders_basemaps) | Order Planet Basemaps using SDK and Requests Library. |
| [Statistical API](api_guides/statistical_api) | Use Statistical API to analyze satellite imagery and derived statistics. |
| [Subscriptions API](api_guides/subscriptions_api) | Uses Subscriptions API to deliver PlanetScope imagery to a data collection for NDVI time series analysis. |
| [Subscriptions API - Crop Biomass](api_guides/subscriptions_api/crop_biomass) | Use Subscriptions API to retrieve and analyze Crop Biomass data for agricultural insights. |
| [Tasking API](api_guides/tasking_api) | Use Tasking API to create, manage, and monitor tasking orders. |
| [Tile Services](api_guides/tile_services) | Render Planet Basemaps via XYZ Tile Services with Bokeh or Leaflet. |

### Use Cases

| Folder | Description |
| ------ | ----------- |
| [Agriculture Index Time Series](use_cases/agriculture_index_time_series) | Generate, process, and analyze agricultural index time series data. |
| [Bare Soil Detector](use_cases/bare_soil_detector) | Uses satellite data to identify bare soil periods in agricultural fields. |
| [Burned Area Delineation](use_cases/burned_area_delineation) | Uses Planet basemaps to map the extent of the Park Fire (2024) burn scar via NDVI and BAI differences. |
| [Calculate Water Extent Analysis Ready Planetscope](use_cases/calculate_water_extent_analysis_ready_planetscope) | Use Analysis-Ready PlanetScope (ARPS) to observe changing water levels in a reservoir. |
| [Coastal Erosion Example](use_cases/coastal_erosion_example) | Use Rasterio to read satellite data. |
| [Crop Classification](use_cases/crop_classification) | Classify crop type with PlanetScope 4-band Orthotiles using CART. |
| [Crop Phenometrics](use_cases/crop_phenometrics) | Uses Planetary Variables to analyze agricultural fields over time. |
| [Crop Segmentation](use_cases/crop_segmentation) | Use KNN classification to identify crops in Planet imagery for georeferenced geojson features. |
| [Forest Carbon Dilligence](use_cases/forest_carbon_dilligence) | Maps forest cover changes between two dates using the Forest Carbon Diligence product. |
| [Forest Monitoring](use_cases/forest_monitoring) | Demonstrates an end-to-end use case to detect deforestation due to road development. |
| [Growing Degree Days](use_cases/growing_degree_days) | Calculates Growing Degree Days (GDD) from Land Surface Temperature using Planet's Statistical API and Sandbox Data. |
| [Land Surface Temperature](use_cases/land_surface_temperature) | Analyze heat waves and urban heat island intensity using Land Surface Temperature data. |
| [Ship Detector](use_cases/ship_detector) | Use scikit-image to detect and count ships in satellite imagery. |
| [Yield Forecasting](use_cases/yield_forecasting) | Use Planetary Variables to forecast hay yield in North Dakota. |

### Workflows

| Folder | Description |
| ------ | ----------- |
| [Analysis Ready Data](workflows/analysis_ready_data) | Use Planet APIs to create Analysis Ready Data (ARD) for time-series analysis. |
| [Analytics Snippets](workflows/analytics_snippets) | Convert Analytics Feed building footprint rasters to vector datasets. |
| [Band Math Generate NDVI](workflows/band_math_generate_ndvi) | Derives a vegetation index from 4-band satellite data. |
| [Band Math Generate NDVI - NDVI](workflows/band_math_generate_ndvi/ndvi) | Uses NDVI to measure vegetation from PlanetScope imagery. |
| [Band Math Generate NDVI - NDVI From Surfance Reflectance](workflows/band_math_generate_ndvi/ndvi_from_sr) | Uses NDVI to measure vegetation for environmental monitoring. |
| [Cloud Native Geospatial - Intro To COGS](workflows/cloud_native_geospatial/intro_to_cogs) | Convert GeoTIFFs to COGs and upload to Google Cloud Storage. |
| [Cloud Native Geospatial - Intro To STAC](workflows/cloud_native_geospatial/intro_to_stac) | Overview of STAC specification and components. |
| [Convert Radiance To Reflectance](workflows/convert_radiance_to_reflectance) | Convert PlanetScope imagery from radiance to reflectance using provided coefficients. |
| [Coverage](workflows/coverage) | Calculate AOI coverage using UTM or WGS84. |
| [Crossovers](workflows/crossovers) | Uses a Python notebook to find crossovers between PSScene and Landsat 8 images, filtering for time difference and cloudiness. |
| [Getting To Know Satellite Imagery](workflows/getting_to_know_satellite_imagery) | Use Rasterio to inspect and Matplotlib to visualize satellite imagery. |
| [Google Earth Engine Integration](workflows/google_earth_engine_integration) | Use Orders API to deliver data to Google Earth Engine. |
| [Introduction To Analysis APIs](workflows/introduction_to_analysis_apis) | Access satellite imagery and perform analysis using Sentinel Hub APIs. |
| [Introduction To Evalscripts](workflows/introduction_to_evalscripts) | Use evalscripts for interactive overview of various analysis. |
| [Landsat Planetscope Comparison](workflows/landsat_planetscope_comparison) | Compares Landsat and PlanetScope scenes for crop type differentiation. |
| [Mosaicking And Masking](workflows/mosaicking_and_masking) | Uses rasterio and fiona to create a composite image from multiple PlanetScope scenes. |
| [Publish To ArcGIS Online](workflows/publish_to_arcgis_online) | Publish PlanetScope imagery as image services in ArcGIS Image for ArcGIS Online. |
| [Working With Usable Data Mask](workflows/working_with_usable_data_mask) | Use UDM to identify and mask pixels with quality issues in satellite imagery. |
