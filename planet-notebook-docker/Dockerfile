# 2019-12-02 build
# FROM jupyter/minimal-notebook:7a0c7325e470

# 2020-01-24 build
# https://github.com/jupyter/docker-stacks/wiki/minimal-notebook-414b5d749704
FROM jupyter/minimal-notebook:414b5d749704

# install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN conda install -y -c conda-forge --file /tmp/requirements.txt
    # jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # jupyter nbextension enable --py --sys-prefix ipyleaflet && \
    # conda clean --all -f -y && \
    # fix-permissions $CONDA_DIR && \
    # fix-permissions /home/$NB_USER

# Enable Jupyter extentions
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter nbextension enable --py --sys-prefix ipyleaflet

# Attempts to avoid having to hardcode this failed.
# ref: https://github.com/planetlabs/notebooks/issues/101
ENV PROJ_LIB=/opt/conda/share/proj

WORKDIR work
