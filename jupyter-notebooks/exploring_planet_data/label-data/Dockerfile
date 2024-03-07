FROM planet-notebooks

# libsqlite3-dev and zlib1g-dev are dependencies of tippicanoe
# libcurl4-openssl-dev is a dependency for pycurl
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libcurl4-openssl-dev \
    libsqlite3-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install tippecanoe (required for label-maker)
RUN git clone https://github.com/mapbox/tippecanoe.git
WORKDIR tippecanoe
RUN make && make install
WORKDIR ..

# Install label-maker
# Currently label-maker does not recognize planet COG files
# because they do not end in `.tif`. For now, we install
# label-maker from the fixed version in a fork
# ref: https://github.com/developmentseed/label-maker/pull/82

# USER $NB_USER
# RUN pip install --upgrade pip && \
#     pip install label-maker==0.3.1

USER root
RUN apt-get install git
RUN git clone https://github.com/jreiberkyle/label-maker.git
WORKDIR label-maker
RUN git checkout geotiff-download-80
USER $NB_USER
RUN pip install .
WORKDIR ..
USER $NB_USER
