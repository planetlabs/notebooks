# Eroding Coastlines: A GeoSpatial and Computer Vision Analysis

## Preparing your Workspace 

Follow the set up instructions below to run the Jupyter Notebooks for this workshop.

### Option 1: (recommended) Run in Google Colab

Interact directly with this repo's Jupyter Notebooks by running them in [Google Colab](http://colab.research.google.com/).

Each Notebook will have its own **"Open in Colab"** button: once running on Colab, you'll need to run a quick setup cell in each notebook (this will install prerequisites and download data into your Colab workspace). You can also choose to make a copy of the Notebook in your own Google Drive, if you want to save any changes you make (not required for this workshop).

### Option 2: Run local Jupyter instance

You can instead choose to open this Notebook in your own local Jupyter instance. In that case, you'll need to clone this repository and install/download prerequisites.

Clone this repo:
```bash
git clone git@github.com:planetlabs/notebooks.git
git checkout scipy-2022
cd jupyter-notebooks/scipy-2022-workshop/
```

**Prerequisites**
- Install: [rasterio](https://pypi.org/project/rasterio) library
- Download data: [20170831_172754_101c_3B_AnalyticMS.tif](https://storage.googleapis.com/pdd-stac/disasters/hurricane-harvey/0831/20170831_172754_101c_3B_AnalyticMS.tif) & [20170831_172754_101c_3b_Visual.tif](https://storage.googleapis.com/pdd-stac/disasters/hurricane-harvey/0831/20170831_172754_101c_3b_Visual.tif)

You may need to move the data from your download directory to the `content` directory, or else modify file paths within the Notebooks as needed.
