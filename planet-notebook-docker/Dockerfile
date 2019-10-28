FROM jupyter/minimal-notebook:1386e2046833

# updating and install apt packages as root including cmake that is essential for some pip 
# installs like h3
USER root
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
      libtiff-dev \
      libgeotiff-dev \
	  git \
	  cmake \
	  build-essential \
	  python3-rtree \
	  wget \
      && rm -rf /var/lib/apt/lists/*

# fix certs for rasterio
# https://stackoverflow.com/a/30154802/2344416
RUN mkdir -p /etc/pki/tls/certs
RUN cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt

# fix ncurses install
# ref: https://github.com/conda-forge/gdal-feedstock/issues/226
RUN conda install -y -c conda-forge ncurses

USER $NB_USER

# Install GDAL
# We use conda because it is the only way to get gdal working properly with ipython
# Installing from a precompiled binary (e.g. using ubuntugis) results in a
# mismatchedsqlite3 version between build and runtime.
# Downloading and building results in the gdal vsicurl driver not working
# (not sure why)

RUN conda install -c conda-forge cartopy
RUN conda install -y -c conda-forge gdal

# Add pip shortcut and install Python3 packages
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt 

# Enable Jupyter extentions
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter nbextension enable --py --sys-prefix ipyleaflet

WORKDIR work
USER $NB_USER
