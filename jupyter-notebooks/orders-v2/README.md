## Orders V2 API Examples

In September of 2018, Planet released the Orers V2 API. The official documentation can be found [here](https://planet-platform.readme.io/docs/overview). The new Planet API ordering service (Orders v2 API) makes it easier to create pipelines to continuously ingest imagery for processing and analysis. Previously, it would take at least 10,000 API calls and continuous monitoring to activate and download 10,000 images. Now that same download can be achieved with only a few API calls. It is recommended best practice to use the Orders API to download and pre-process Planet imagery.

The Orders v2 API has some significant capabilities to the Planet API, including:

**Data management capabilities:**

* *Clip*: clip a raster to a specified AOI

* *TOAR*: convert radiance products to top of atmospheric reflectance

* *Tile*: split an input file into a regular set of tiles based on a user described tiling system

* *Composite*: composite a set of raster files into one output

* *Reproject*: reproject, resample and rescale raster products to a new projected coordinate system, and resolution

* *Image Co-registration*: Co-register a stack of PlanetScope imagery

**Delivery capabilities:**

* Direct delivery to cloud storage such as Amazon S3, Azure, and GCP

* Support for webhook notifications

* Bulk activation and download

**Analysis capabilities**

* *Band math*: apply arbitrary band math to produce derived raster products


**Some of the benefits of migrating to Orders V2:**

* No need to build and maintain infrastructure to support processing Planet imagery;

* Faster bulk activation and delivery;

* Support of cloud-to-cloud workflows; and

* Reduced cloud costs -- computation, storage, development, and maintenance.
