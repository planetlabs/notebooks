# Ordering Basemaps Using SDK v2 Beta and Requests Library

## Preparing your Workspace 

Follow the set up instructions below to run the Jupyter Notebooks for this workshop.

### Option 1: (recommended) Run in Google Colab

Interact directly with this repo's Jupyter Notebooks by running them in Google Colab.

Each Notebook will have its own **"Open in Colab"** button: once running on Colab, you'll need to run a quick setup cell in each notebook (this will install prerequisites and download data into your Colab workspace). You can also choose to make a copy of the Notebook in your own Google Drive, if you want to save any changes you make (not required for this workshop).

### Option 2: Run local Jupyter instance

You can instead choose to open this Notebook in your own local Jupyter instance. In that case, you'll need to clone this repository and install/download prerequisites.

Clone this repo:
```bash
git clone git@github.com:planetlabs/notebooks.git
cd notebooks/jupyter-notebooks/orders_basemaps/
```

### About these notebooks


Method 1: The first [file](SDK_order_basemaps.ipynb)) demonstrates using the SDK v2 Beta to order Basemaps using both an AOI and quad ID. This is the way we recommend ordering Planet Basemaps. The SDK v2 Beta has functions ready-made to make working with the Planet Orders API more efficient and less prone to errors. This means less lines of code and less work for you. Check out the SDK v2 Beta docs [here](https://planet-sdk-for-python-v2.readthedocs.io/en/latest/python/sdk-guide/). 

Method 2: The second [file](requests_order_basemaps.ipynb) demonstrates using the Python Requests Library to order Basemaps using an AOI and quad IDs.

