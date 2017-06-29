## Planet Interactive Guides

In this repository, you'll find a collection of [Jupyter notebooks](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html) from the software developers, data scientists, and developer advocates at [Planet](https://www.planet.com/). These interactive, open-source (APLv2) guides are designed to help our users explore Planet's data archive, start using our APIs and tools, and learn more about extracting information from Planet's massive archive of high-cadence satellite imagery.

### Developer tools
* [Introduction to Planet's Data API](https://github.com/planetlabs/notebooks/blob/master/data-api-tutorials/planet_data_api_introduction.ipynb)
* [Using Planet's Python Client](https://github.com/planetlabs/notebooks/blob/master/data-api-tutorials/planet_cli_introduction.ipynb)

### Data processing
* [Creating a composite image from multiple PlanetScope scenes](https://github.com/planetlabs/notebooks/blob/master/mosaicing/basic_compositing_demo.ipynb)
* [Calculating a vegetation index from 4-band satellite imagery](https://github.com/planetlabs/notebooks/blob/master/ndvi/ndvi_planetscope.ipynb)

### Other notebooks from Planeteers
* [Python examples for remote sensing](https://github.com/kscottz/PythonFromSpace)
* [Exploring geospatial data with open source tools](https://github.com/kjordahl/SciPy-Tutorial-2015)

Soon we hope to add notebooks from the researchers, technologists, geographers, and entrepreneurs who are already using Planet data to ask interesting and innovative questions about our changing Earth. If you're working with our imagery and have a notebook (or just an idea for a notebook) that you'd like to share, please [file an issue](https://github.com/planetlabs/notebooks/issues) or send a message to [danabauer](https://github.com/danabauer) at <dana@planet.com>.

## Installation

### System Prerequisites
* [Docker](https://store.docker.com/search?type=edition&offering=community)
* [Planet Account](https://www.planet.com/explorer/?signup=1)
* [Planet API Key](https://www.planet.com/account/#/)

### Clone the repo:
```bash
git clone git@github.com:planetlabs/notebooks.git
cd notebooks
```

## Running Planet Notebooks in Docker
Planet Notebooks relies on a complex stack of technologies that are not always easy to install and properly 
configure. To ease this complexity we provide a docker container for running the notebook on docker compatible 
systems. To install docker on your system please see docker's [documentation](https://docs.docker.com/engine/installation/)
for your operating system.

### Build the Docker image
First you must build the docker image. Note, this only has to be done the first time you use it. After checking out the
this repository, you run:
```bash
docker build --rm -t planet-notebooks .
```

This will build and install the Docker image on your system, making it available to run. This may take some 
time (between 10 and 20 minutes) depending on your network connection.

### Run the container
To run the container (after building it), add your Planet API key below and issue the following command:
```bash
docker run -it --rm -p 8888:8888 -v $PWD/jupyter-notebooks:/home/jovyan/work -e PL_API_KEY='[YOUR-API-KEY]' planet-notebooks
```

This does several things:  

1. Maps the docker container's ```8888``` port to your system's ```8888``` port.  This makes the 
container available to your host systems web browser.

1. Maps a host system path ```$PWD\jupyter-notebooks``` to the docker containers working 
directory.  This ensures that the notebooks you create, edit, and save are available on your host system,
and are not *destroyed* when the you exit the container.

1. Starts in an interactive terminal and is accessible through http://localhost:8888.

1. Sets an environment variable with your unique Planet API key for authenticating against the API.

1. Include the ```--rm``` option to clean up the notebook after you exit the process.

### Open Jupyter notebooks
Once the Docker container is running, the CLI output will display a URL that you will use to access Jupyter notebooks
with your browser.
```
http://localhost:8888/?token=<UNIQUE-TOKEN>
```

NOTE: This security token will change every time you start your Docker container.
