# This image is focused on supporting Python2.7 although
# the base image supports Python 2 and 3.
FROM jupyter/scipy-notebook

# Install the notebook dependencies using conda.
# Since the notebooks use Python2, most of the
# depencendies are installed into the python2
# environment. Ipyleaflet is installed into the root
# environment because because otherwise the widget
# doesn't work.
COPY root.yml python2.yml /tmp/
RUN conda env update -n python2 -f /tmp/python2.yml
RUN conda env update -n root -f /tmp/root.yml
