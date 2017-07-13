# This image is focused on supporting Python2.7 although
# the base image supports Python 2 and 3
FROM jupyter/scipy-notebook

# Install gdal into python2 environment
RUN conda install --yes --name python2 gdal

# Install and enable ipyleaflet extension
# installation into root environment required for extensions to work
# properly
RUN conda install --yes --name python2 -c conda-forge ipyleaflet
RUN conda install --yes -c conda-forge ipyleaflet

# Install planet api and other geo packages
RUN conda install --yes --name python2 -c conda-forge \
    rasterio \
    shapely \
    fiona \
    pyproj \
    opencv && \
    conda clean -tipsy

RUN pip2 install --upgrade pip && \
    pip2 install planet
