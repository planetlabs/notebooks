FROM planet-notebooks

USER root
RUN apt-get install git
RUN git clone https://github.com/jreiberkyle/label-maker.git
WORKDIR label-maker
RUN git checkout geotiff-download-80
RUN pip install .
WORKDIR ..
USER $NB_USER
