FROM jupyter/minimal-notebook:2c80cf3537ca
# c88678a1c7c9

# Create Python2 environment
RUN conda create --yes -p $CONDA_DIR/envs/python2 python=2.7

# Install GDAL
# We use conda because it is the only way to get gdal working properly with ipython
# Installing from a precompiled binary (e.g. using ubuntugis) results in a
# mismatchedsqlite3 version between build and runtime.
# Downloading and building results in the gdal vsicurl driver not working
# (not sure why)
RUN conda install -y -c conda-forge gdal=2.1.3
RUN conda install -y --name python2 -c conda-forge gdal=2.1.3

# Add pip2.7 shortcut and install Python2 packages
RUN ln -s $CONDA_DIR/envs/python2/bin/pip $CONDA_DIR/bin/pip2.7 && \
    pip2.7 install --upgrade pip && \
    pip2.7 install numpy>=1.13.1 && \
    pip2.7 install \
        geojsonio \
        geopandas \
        ipykernel \
        ipyleaflet \
        ipywidgets \
        matplotlib \
        numpy \
        opencv-python==3.3.0.10 \
        planet \
        pygdal==2.1.3.3 \
        pyproj \
        rasterio==1.0a12 \
        setuptools \
        scikit-image \
        shapely \
        scikit-learn \
        tqdm

# Install tippecanoe (required for label-maker)
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libsqlite3-dev \
    zlib1g-dev 

RUN git clone https://github.com/mapbox/tippecanoe.git
WORKDIR tippecanoe
RUN make && make install
WORKDIR ..


# Install dependencies for pycurl, a dependency of label-maker
RUN apt-get update && apt-get install -y libcurl4-openssl-dev

# Add pip shortcut and install Python3 packages
USER $NB_USER
RUN pip install --upgrade pip && \
    pip install numpy>=1.13.1 && \
    pip install \
        geojson \
        geopandas \
        ipyleaflet \
        ipywidgets \
        label-maker==0.3.1 \
        matplotlib \
        numpy \
        opencv-python==3.3.0.10 \
        planet \
        pygdal==2.1.3.3 \
        pyproj \
        rasterio==1.0a12 \
        scikit-image \
        shapely \
        tqdm

# Activate Python2 kernel globally and upon kernel launch.
USER root
RUN pip install kernda --no-cache && \
    $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
    kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json && \
    pip uninstall kernda -y

# Enable Jupyter extentions
USER $NB_USER
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter nbextension enable --py --sys-prefix ipyleaflet

# Clean up
USER root
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR work
USER $NB_USER
