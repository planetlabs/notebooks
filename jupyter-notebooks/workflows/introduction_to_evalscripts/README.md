# Interactive Intro to Evalscripts

The notebooks in this repository give a solid intro to evalscripts.

To be able to follow along well in these notebooks a few requirements are necessary:

- [Basic Knowledge of Remote Sensing](https://university.planet.com/introduction-to-remote-sensing)
  - Sensors
  - Spectral Bands
  - Indices
- [Basic Familiarity with Sentinel Hub](https://www.sentinel-hub.com/explore/education/webinars/)
  - Collections
  - Processing API
  - Statistical API
- Basic knowledge of programming concepts
  - [functions](https://www.w3schools.com/js/js_functions.asp)
  - [variables](https://www.w3schools.com/js/js_variables.asp)
  - [arrays](https://www.w3schools.com/js/js_arrays.asp)
  - [objects](https://www.w3schools.com/js/js_objects.asp)

The two notebooks cover the following topics:

### 1. Basic evalscripts

[Link to notebook](./1_basic_evalscripts.ipynb)

- How to construct basic non-temporal evalscripts using the `setup` and `evaluatePixel` function.
- Covering `sampleType`s and when to use which sample Type
- Format requirements when streaming data to a web application vs. downloading data for analytical use
- How Sentinel Hub deals with missing data (using the `dataMask` output) and how to assign no data values to the output when doing analytic work or set pixels transparent when streaming data visualizations
- Common issues to check when evalscripts don't return the expected output and how to throw errors to help with debugging

### 2. Multi temporal evalscripts

[Link to notebook](./2_multi_temporal_evalscripts.ipynb)

- Covering the mosaicking options `SIMPLE`, `TILE` and `ORBIT` and what their differences are
- How to access the `samples` object in `evaluatePixel` when doing multi-temporal analysis
- Analysis:
  - cloud-free mosaics
  - maximum and mean NDVI composites
  - temporal NDVI differences
