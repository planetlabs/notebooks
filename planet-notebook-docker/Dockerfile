# pin to latest image on Oct 6, 2017
FROM jupyter/minimal-notebook:e1677043235c

USER $NB_USER

# gdal is the basis of all GIS libraries, so is installed first
# conda takes care of installing gdal C and python libraries
RUN conda install -y -c conda-forge gdal=2.1.3

# Install and enable Jupyter extentions
RUN pip install --upgrade pip && \
    pip install ipywidgets==7.0.1 ipyleaflet==0.4.0 && \
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter nbextension enable --py --sys-prefix ipyleaflet

# Install additional packages
# install numpy first as it is a prerequirement for rasterio
RUN pip install --upgrade pip && \
    pip install numpy==1.13.1 && \
    pip install \
        geojsonio \
        geopandas \
        opencv-python==3.3.0.10 \
        planet \
        pyproj==1.9.5.1 \
        rasterio==1.0a9 \
        scikit-image \
        scikit-learn==0.19.0 \
        shapely==1.6.1 \
        tqdm

