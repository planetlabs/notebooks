FROM jupyter/minimal-notebook:2c80cf3537ca

# Install GDAL
# We use conda because it is the only way to get gdal working properly with ipython
# Installing from a precompiled binary (e.g. using ubuntugis) results in a
# mismatchedsqlite3 version between build and runtime.
# Downloading and building results in the gdal vsicurl driver not working
# (not sure why)
RUN conda install -y -c conda-forge gdal=2.4.0

# Add pip shortcut and install Python3 packages
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt 

# Enable Jupyter extentions
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter nbextension enable --py --sys-prefix ipyleaflet

# fix certs for rasterio
# https://stackoverflow.com/a/30154802/2344416
USER root
RUN mkdir -p /etc/pki/tls/certs
RUN cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt

# fix ncurses install
# ref: https://github.com/conda-forge/gdal-feedstock/issues/226
USER root
RUN conda install -y -c conda-forge ncurses

WORKDIR work
USER $NB_USER
