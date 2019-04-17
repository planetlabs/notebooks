FROM jupyter/minimal-notebook:2c80cf3537ca

# For binder to work, it needs to be able to lanunch jupyter notebook as a specified user.
# User specs can be passed via docker build args as NB_UID/NB_USER
# https://mybinder.readthedocs.io/en/latest/sample_repos.html
# Create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}

# Configure and Install stuff as root
USER root
# This chown is required because Docker will by default set the owner to root, which would prevent users from editing files.
RUN chown -R ${NB_UID} ${HOME}
WORKDIR ${HOME}

# Install GDAL
# We use conda because it is the only way to get gdal working properly with ipython
# Installing from a precompiled binary (e.g. using ubuntugis) results in a
# mismatchedsqlite3 version between build and runtime.
# Downloading and building results in the gdal vsicurl driver not working
# (not sure why)
RUN conda install -y -c conda-forge gdal=2.4.0

# pyviz and descartes also need to be conda installed
RUN conda install -y -c pyviz/label/dev pyviz
RUN conda install -y -c conda-forge descartes

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

# Fix notebook version to address traitlets issue
# https://github.com/jupyter/notebook/issues/3946#issuecomment-423035232
RUN conda install notebook==5.6.0

WORKDIR work
USER $NB_USER
