# 2025-09-15 build
# https://github.com/jupyter/docker-stacks/wiki/minimal-notebook-414b5d749704
FROM quay.io/jupyter/minimal-notebook:8515ad39f045

# install dependencies
COPY requirements.txt /tmp/requirements.txt

# libgl Required for opencv
# https://github.com/conda-forge/pygridgen-feedstock/issues/10#issuecomment-365914605
USER root
RUN apt-get update && apt-get install -yq --no-install-recommends \
    libgl1 libglx-mesa0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
USER $NB_UID

# without channel set to strict, a conflicting version of gdal
# is sometimes installed from the default channel
RUN conda config --set channel_priority strict && \
    conda install -y -c conda-forge --file /tmp/requirements.txt

# install the following libraries w/ pip to support analytics/user-guide nb's
# build fails due to long conda solves when these dependencies are added to requirements.txt
# see https://github.com/planetlabs/notebooks/issues/135 for more details
# python -m pip as per https://github.com/pypa/pip/issues/5599
RUN python -m pip install descartes geoviews

# Attempts to avoid having to hardcode this failed.
# ref: https://github.com/planetlabs/notebooks/issues/101
ENV PROJ_LIB=/opt/conda/share/proj

WORKDIR work
