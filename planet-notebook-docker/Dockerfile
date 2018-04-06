FROM jupyter/minimal-notebook

# Install the packages
USER root
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
        gcc \
        g++ \
        make \
        curl \
        libgeos-dev \
        libproj-dev \
        git \
        ssh \
        libffi-dev \
        libssl-dev \
        python-pip \
        python-cffi \
        python-lxml \
        python-pil \
        python-numpy \
        python-scipy \
        python-pandas \
        python-matplotlib \
        python-seaborn \
        python-concurrent.futures \
        cython \
        python-scikits-learn \
        python-scikits.statsmodels \
        python-skimage-lib \
        pkg-config

# Install GDAL from source
RUN curl -O http://download.osgeo.org/gdal/2.1.3/gdal-2.1.3.tar.gz && \
    tar -xzf gdal-2.1.3.tar.gz

WORKDIR gdal-2.1.3

RUN ./configure && \
    make -j$(nproc) && \
    make install && \
    ldconfig

WORKDIR ../

RUN rm -rf gdal-2.1.3.tar.gz && \
    rm -rf gdal-2.1.3

WORKDIR work

# # Create Python2 environment
USER $NB_USER
RUN conda create --yes -p $CONDA_DIR/envs/python2 python=2.7

# Add pip2.7 shortcut and install Python2 packages
RUN ln -s $CONDA_DIR/envs/python2/bin/pip $CONDA_DIR/bin/pip2.7 && \
    pip2.7 install --upgrade pip && \
    pip2.7 install \
        setuptools \
        matplotlib \
        scikit-image && \
    pip2.7 install \
        geojsonio \
        geopandas \
        ipykernel \
        ipyleaflet \
        ipywidgets \
        numpy \
        opencv-python==3.3.0.10 \
        planet \
        pygdal==2.1.3.3 \
        pyproj \
        shapely \
        scikit-learn \
        tqdm && \
     pip2.7 install --no-binary :all: rasterio==1.0a9

# Add pip shortcut and install Python3 packages
# rasterio requires no-binary, put in separate install cmd
RUN pip install --upgrade pip && \
    pip install matplotlib \
        scikit-image && \
    pip install \
        geojson \
        geopandas \
        ipyleaflet \
        ipywidgets \
        numpy \
        opencv-python==3.3.0.10 \
        planet \
        pygdal==2.1.3.3 \
        pyproj \
        shapely \
        tqdm && \
    pip install --no-binary :all: rasterio==1.0a9

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

USER root

RUN apt-get update && apt-get install -y \
    libsqlite3-dev zlib1g-dev # for tippecanoe

# Install label maker (depends on tippecanoe)

# install tippecanoe
# deps: libsqlite3-dev zlib1g-dev git
RUN git clone https://github.com/mapbox/tippecanoe.git
WORKDIR ./tippecanoe
RUN make && make install
WORKDIR ..

RUN apt-get update && apt-get install -y libcurl4-openssl-dev

USER $NB_USER
RUN pip install --upgrade pip && \
 pip install label-maker

USER root

RUN apt-get remove --yes g++ gcc ssh git make curl && \
    conda clean --yes --all && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

USER $NB_USER
