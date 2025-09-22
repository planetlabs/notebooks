## Planet Interactive Guides

In this repository, you'll find a collection of [Jupyter notebooks](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html) from the software developers, data scientists, and developer advocates at [Planet](https://www.planet.com/). These interactive, open-source ([APLv2](LICENSE)) guides are designed to help you work with our APIs and tools, explore Planet data, and learn how to extract information from our massive archive of high-cadence satellite imagery. We hope these guides will inspire you to ask interesting questions of Planet data. Need help? Find a bug? Please [file an issue](https://github.com/planetlabs/notebooks/issues/new) and we'll get back to you.

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

## Authentication

## Access your Planet API Key in Python

Authentication with Planet's API Key can be achieved by using a valid Planet API Key.

You can export your API Key as an environment variable on your system:

```bash
export PL_API_KEY="YOUR-API-KEY"
```

If you wish to have your API Key be persistent (forever stored as ```PL_API_KEY```), then you may enter this ```export``` command in your ```~/.bashrc``` or ```~/.zshrc``` file. If you are using our Docker environment, as is defined below, it will already be set.

In Python, we set up an API Key variable, ```PLANET_API_KEY```, from an environment variable to use with our API requests:

```python
# Import the os module in order to access environment variables
import os

# Set up the API Key from the `PL_API_KEY` environment variable
PLANET_API_KEY = os.getenv('PL_API_KEY')
```

Now, your Planet API Key is stored in the variable ```PLANET_API_KEY``` and is ready to use in your Python code.

### Sentinel Hub Python SDK
Some Notebooks in this repository use the [Sentinel Hub Python SDK](https://sentinelhub-py.readthedocs.io/en/latest/index.html).  Currently, this SDK uses a different method of authenticating than what is used with the Planet APIs and SDK for Python. 

For the Sentinel Hub Python SDK, you must provide a ```client_id``` and a ```client_secret``` which can be obtained from the [Dashboard](https://apps.sentinel-hub.com/dashboard/) app. You can find full instructions on setting up the client credentials in this SDK from the [SDK documentation](https://sentinelhub-py.readthedocs.io/en/latest/configure.html).

```python
from sentinelhub import SHConfig 
import getpass

config = SHConfig()

if not config.sh_client_id or not config.sh_client_secret:
    print("No credentials found, please provide the OAuth client ID and secret.")
    config.sh_client_id = getpass.getpass("sh_client_id: ")
    config.sh_client_secret = getpass.getpass("sh_client_secret: ")
    config.save()
    print(f"Credentials saved to {SHConfig.get_config_location()}")
else:
    print(f"Using credentials stored here: {SHConfig.get_config_location()}")
```

## Run Planet Notebooks in Docker
Planet Notebooks rely on a complex stack of technologies that are not always easy to install and properly 
configure. To ease this complexity we provide a docker container for running the notebook on docker compatible 
systems. To install docker on your system please see docker's [documentation](https://docs.docker.com/engine/installation/)
for your operating system.

### Build the Docker image

First you must build the docker image. Note, this only has to be done the first time you use it. After checking out the
repository, you run:
```bash
docker build -t planet-notebooks planet-notebook-docker/
```

This will build and install the Docker image on your system, making it available to run. This may take some 
time (from 10 minutes to an hour) depending on your network connection and how long Anaconda takes to configure
its environment.

### Run the container
To run the container (after building or downloading it), add your Planet API key below and issue the following command from the git repository root directory:

```bash
docker run -it --rm -p 8888:8888 -v "$(pwd)/jupyter-notebooks:/home/jovyan/work" -e PL_API_KEY='your-key' planet-notebooks

# If you get a permissions error running the above, you should add sudo to the front:
# sudo docker run -it --rm -p 8888:8888 -v $PWD:/home/jovyan/work -e PL_API_KEY='[YOUR-API-KEY]' planet-notebooks
```

This does several things:  

1. **Maps port 8888** - Makes the container accessible at http://localhost:8888
2. **Mounts your notebooks** - Maps `jupyter-notebooks/` folder to `/home/jovyan/work` so your work persists and notebooks are accessible to Jupyter
3. **Sets your API key** - Replace `your-key` with your actual Planet API key for API authentication
4. **Starts interactive terminal** - Accessible through the web browser
5. **Auto-cleanup** - Removes container when you exit (`--rm`)

### Open Jupyter notebooks
Once the Docker container is running, the CLI output will display a URL that you will use to access Jupyter notebooks
with your browser.
```
http://localhost:8888/?token=<UNIQUE-TOKEN>
```

NOTE: This security token will change every time you start your Docker container.