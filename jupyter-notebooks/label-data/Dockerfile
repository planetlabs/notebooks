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
USER $NB_USER
RUN pip install --upgrade pip && \
    pip install label-maker==0.3.1


