## Planet Interactive Guides

[![Join the chat at https://gitter.im/planetlabs/notebooks](https://badges.gitter.im/planetlabs/notebooks.svg)](https://gitter.im/planetlabs/notebooks?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

In this repository, you'll find a collection of [Jupyter notebooks](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html) from the software developers, data scientists, and developer advocates at [Planet](https://www.planet.com/). These interactive, open-source ([APLv2](LICENSE)) guides are designed to help you explore Planet data, work with our APIs and tools, and learn how to extract information from our massive archive of high-cadence satellite imagery. We hope these guides will inspire you to ask interesting questions of Planet data. Need help? Find a bug? Please [file an issue](https://github.com/planetlabs/notebooks/issues/new) and we'll get back to you.

## Install and use these notebooks

### System Prerequisites
* [Docker](https://store.docker.com/search?type=edition&offering=community)
* [Planet Account](https://www.planet.com/explorer/?signup=1)
* [Planet API Key](https://www.planet.com/account/)

NOTE: After installing Docker, Windows users should install WSL2 Backend when prompted.

### Clone or update repo:

If you've never cloned the Planet notebooks repo, run the following:

```bash
git clone https://github.com/planetlabs/notebooks.git
cd notebooks
```

If you have previously cloned the Planet notebooks repo in the past, make sure to update to pull any changes locally that might have happened since you last interacted with the Planet notebooks:

```bash
cd notebooks
git pull
``` 

## Run Planet Notebooks in Docker
Planet Notebooks rely on a complex stack of technologies that are not always easy to install and properly 
configure. To ease this complexity we provide a docker container for running the notebook on docker compatible 
systems. To install docker on your system please see docker's [documentation](https://docs.docker.com/engine/installation/)
for your operating system.

### Download prebuilt Docker image (recommended)
The Docker image for these notebooks is hosted in the [planetlabs/notebooks](https://hub.docker.com/r/planetlabs/notebooks) repo on DockerHub. To download and prepare the image for use, run:

```bash
cd notebooks
docker pull planetlabs/notebooks
docker tag planetlabs/notebooks planet-notebooks

# If you get errors running the above, you might have to add sudo to the beginning:
#sudo docker pull planetlabs/notebooks
#sudo docker tag planetlabs/notebooks planet-notebooks
```

If you want to re-build the Docker image yourself, this is documented below in the "Appendix: Build the Docker image" section.

### Run the container
To run the container (after building or downloading it), add your Planet API key below and issue the following command from the git repository root directory:

```bash
docker run -it --rm -p 8888:8888 -v $PWD:/home/jovyan/work -e PL_API_KEY='[YOUR-API-KEY]' planet-notebooks

# If you get a permissions error running the above, you should add sudo to the front:
# sudo docker run -it --rm -p 8888:8888 -v $PWD:/home/jovyan/work -e PL_API_KEY='[YOUR-API-KEY]' planet-notebooks
# Windows users run: winpty docker run -it --rm -p 8888:8888 -v "/$PWD":/home/joyvan/work -e PL_API_KEY='[YOUR-API-KEY]' planet-notebooks

```

This does several things:  

1. Maps the docker container's ```8888``` port to your system's ```8888``` port.  This makes the 
container available to your host systems web browser.

1. Maps a host system path ```$PWD``` to the docker container's working directory.
This ensures that the notebooks you create, edit, and save are available on your host system under the
`jupyter-notebooks` sub-directory and are not *destroyed* when you exit the container.
This also allows for running tests in the `tests` sub-directory.

1. Ensures that the directory in the Docker container named `/home/jovyan/work` that has the notebooks
in them is accessible to the Jupyter notebook server.

1. Starts an interactive terminal that is accessible through http://localhost:8888.

1. Sets an environment variable with your unique Planet API key for authenticating against the API.

1. Includes the ```--rm``` option to clean up the notebook after you exit the process.

### Open Jupyter notebooks
Once the Docker container is running, the CLI output will display a URL that you will use to access Jupyter notebooks
with your browser.
```
http://localhost:8888/?token=<UNIQUE-TOKEN>
```

NOTE: This security token will change every time you start your Docker container.

### Available notebooks

#### Search, activate, download with the Data API   
* [Explore the Planet Data API with Python](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/data-api-tutorials/planet_data_api_introduction.ipynb)
* [Search, activate, and download imagery with the Planet Python Client](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/data-api-tutorials/planet_cli_introduction.ipynb)
* [Planet Data API reference](https://docs.planet.com/v1/reference)

#### Ordering, delivery, and tools with the Orders API
* [Ordering and Delivery](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/orders/ordering_and_delivery.ipynb)
* [Tools and Toolchains](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/orders/tools_and_toolchains.ipynb)
* [Planet Orders API reference](https://developers.planet.com/docs/orders/)

#### Feeds, Subscriptions, and Results with the Analytics API
* [Inspecting Available Feeds](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/01_checking_available_feeds_and_subscriptions.ipynb)
* [Getting Feed Results](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/02_fetching_feed_results.ipynb)
* [Visualizing Raster Results](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/03_visualizing_raster_results.ipynb)
* [Converting Raster Results to Vector Features](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics-snippets/README.md)
* [Creating a Heatmap of Vector Results](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/change_detection_heatmap.ipynb)

### Process Planet data
* [Create a mosaic from multiple PlanetScope scenes](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/mosaicing/basic_compositing_demo.ipynb)
* [Calculate a vegetation index from 4-band satellite imagery](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/ndvi/ndvi_planetscope.ipynb)
* [Convert PlanetScope metadata from radiance to reflectance](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/toar/toar_planetscope.ipynb)
* [Visualize and convert a UDM to a binary mask](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/udm/udm.ipynb)
* [Work with the Usable Data Mask (UDM2)](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/udm2)

### Analyze and visualize Planet data

* Analytics quickstart:
    1. [Summarizing Feeds and Subscriptions](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/quickstart/01_checking_available_feeds_and_subscriptions.ipynb)
    2. [Getting Analytic Feed Results](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/quickstart/02_fetching_feed_results.ipynb)
    3. [Visualizing Raster Results](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/quickstart/03_visualizing_raster_results.ipynb)
* Analytics user guide:
    1. [Getting Started with Planet Analytics API](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/user-guide/01_getting_started_with_the_planet_analytics_api.ipynb)
    2. [Planet Analytic Feeds Results](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/user-guide/02_analytic_feeds_results.ipynb)
    3. [Change Detection](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/user-guide/03_change_detection.ipynb)
    4. [Summary Statistics - Buildings](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/user-guide/04_summary_statistics_buildings.ipynb)
    5. [Summary Statistics - Ships and Clouds](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/analytics/user-guide/05_summary_statistics_ships_and_clouds.ipynb)
* Other analytics notebooks:
    * [Detect, count, and visualize ships in Planet imagery](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/ship-detector/01_ship_detector.ipynb)
    * [Python examples for remote sensing](https://github.com/kscottz/PythonFromSpace)
    * [Pixel-by-pixel comparison of PlanetScope and Landsat Scenes](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/landsat-ps-comparison/landsat-ps-comparison.ipynb)
    * [Calculate Coverage for a Search Query](https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/coverage/calculate_coverage.ipynb)
    * [Segment and Classify Crops](https://github.com/planetlabs/notebooks/tree/master/jupyter-notebooks/crop-classification)
    * [Identify Forest Degradation](https://github.com/planetlabs/notebooks/tree/master/jupyter-notebooks/forest-monitoring)
    * [Identify the Temporal Signature of Crops](https://github.com/planetlabs/notebooks/tree/master/jupyter-notebooks/temporal-analysis)

Soon we hope to add notebooks from the researchers, technologists, geographers, and entrepreneurs who are already using Planet data to ask interesting and innovative questions about our changing Earth. If you're working with our imagery and have a notebook (or just an idea for a notebook) that you'd like to share, please [file an issue](https://github.com/planetlabs/notebooks/issues) and let us know.

### Appendix: Build the Docker image

This documents how to build the docker image yourself, rather than using the recommended step of downloading pre-built Docker images. This is useful if you are a developer adding dependencies or a new Jupyter notebook to this repo, for example.

First you must build the docker image. Note, this only has to be done the first time you use it. After checking out the
repository, you run:
```bash
cd planet-notebook-docker
docker build --rm -t planet-notebooks .
cd ..
```

This will build and install the Docker image on your system, making it available to run. This may take some 
time (from 10 minutes to an hour) depending on your network connection and how long Anaconda takes to configure
its environment.
