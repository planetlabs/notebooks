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

# Create Python2 environment
USER $NB_USER
RUN conda create --yes -p $CONDA_DIR/envs/python2 python=2.7

# Add pip2.7 shortcut and install Python2 packages
RUN ln -s $CONDA_DIR/envs/python2/bin/pip $CONDA_DIR/bin/pip2.7 && \
    pip install --upgrade pip && \
    pip2.7 install \
        setuptools \
        matplotlib \
        scikit-image && \
    pip2.7 install \
        ipykernel \
        pyproj \
        ipywidgets \
        ipyleaflet \
        numpy \
        shapely \
        --no-binary :all: rasterio \
        geopandas \
        tqdm \
        planet \
        pygdal==2.1.3.3 \
        geojsonio \
        scikit-learn \
        opencv

# Add pip shortcut and install Python3 packages
RUN pip install --upgrade pip && \
    pip install matplotlib && \
    pip install scikit-image && \
    pip install \
        pyproj \
        ipywidgets \
        ipyleaflet \
        numpy \
        shapely \
        --no-binary :all: rasterio \
        geopandas \
        tqdm \
        planet \
        pygdal==2.1.3.3 \
        geojsonio

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
RUN apt-get remove --yes g++ gcc ssh git make curl && \
    conda clean --yes --all && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

USER $NB_USER
