# 2020-01-24 build
# https://github.com/jupyter/docker-stacks/wiki/minimal-notebook-414b5d749704
FROM jupyter/minimal-notebook:414b5d749704

# install dependencies
COPY requirements.txt /tmp/requirements.txt

# Required for opencv
# https://github.com/conda-forge/pygridgen-feedstock/issues/10#issuecomment-365914605
USER root
RUN apt-get update && apt-get install -yq --no-install-recommends \
    libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
USER $NB_UID

# without channel set to strict, a conflicting version of gdal
# is sometimes installed from the default channel
RUN conda config --set channel_priority strict && \
    conda install -y -c conda-forge --file /tmp/requirements.txt

# install the following libraries w/ pip to support analytics/user-guide nb's
# build fails when these dependencies are added to requirements/ installed with conda
# python -m pip as per https://github.com/pypa/pip/issues/5599
RUN python -m pip install descartes holoviews geoviews xarray datashader

# Enable Jupyter extentions
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter nbextension enable --py --sys-prefix ipyleaflet

# Attempts to avoid having to hardcode this failed.
# ref: https://github.com/planetlabs/notebooks/issues/101
ENV PROJ_LIB=/opt/conda/share/proj

WORKDIR work
