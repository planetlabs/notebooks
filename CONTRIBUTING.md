# Contributing to Notebooks

Contributions are welcome to this repository. Please open a PR if you would like to contribute a notebook and we will review. Alternatively, if you have a request or an idea, you can [open an issue](https://github.com/planetlabs/notebooks/issues/new/choose).

## Notebook Style

If you are contributing a notebook, we've gathered these style guide requirements.

### Filemames

Notebook filenames should not have spaces. Please use underscores with `snake_case` instead for all files in the repository.

Your filename should align to the title of the notebook. For example, a notebook titled **Generate Agriculture Index Time Series** should be `generate_agriculture_index_time_series.ipynb`.

### HTML and Markdown

For maximum portability, accessibility, and ease of use, notebooks in this repository should not use a custom style or theme. Please stick to standard markdown features so that it works across all environments.

### Dependencies

When a new notebook has a dependency that is not yet supported by the Docker image, please add the dependency to the [Docker setup requirements file](planet-notebook-docker/requirements.txt).

Alternatively, you can choose to add package installation instructions in your Notebook, particularly if the notebook you are adding has any heavy, unique, or tricky dependencies. If you do this, make sure to include comments in the notebooks.

### Ordering Notebooks

If you are working on a multi-part guide that has several notebooks, prefix the notebooks with `1_`, `2_`, `3_`, and so on to indicate the order.

### Optimize Cell Outputs for Viewing in the Browser

If you have a cell that prints a very large json repsonse, consider alternative ways to view the data. Could it be viewed in a table or on a map? Very large json repsonses make notebooks difficult to read. 

### Use Colab

When possible, add the option to open the notebook in Colab. This should be added as the very first line in the first cell of the Jupyter Notebook file so that it appears at the very top. 

For example:

```
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github//planetlabs/notebooks/blob/master/jupyter-notebooks/workflows/planet_sandbox_data/agriculture-index-time-series/agriculture-index-time-series.ipynb)
```

If your notebook includes Colab link, make sure that the packages used within it are either a) default colab packages or b) imported using a magic command `%pip install planet`.

### Introduction

For a notebook, please make sure to include context and description at the top using this format:

```
<colab link>
# Notebook Title

Information about the notebook

## Requirements

Any special requirements, set up instructions, permissions, pre-steps, etc.
```

### Authentication

Most Notebooks will likely require authenticating with Planet APIs. In order to use consistent authentication and schemes across all of the notebooks, we've provided 3 authentication snippets that we recommend you use:

#### For Notebooks that use the Planet SDK for Python

```
import planet

# If you are not already logged in, this will prompt you to open a web browser to log in.
auth = planet.Auth.from_profile('planet-user', save_state_to_storage=True)
if not auth.is_initialized():
    auth.user_login(allow_open_browser=False, allow_tty_prompt=True)

session = planet.Session(auth)
pl = planet.Planet(session)
```

#### For Notebooks that use the Sentinel Hub Python SDK

```
from sentinelhub import SHConfig

# Authenticate with the Sentinel Hub Python SDK; See docs: https://sentinelhub-py.readthedocs.io/en/latest/configure.html and https://docs.planet.com/develop/authentication
# If no default configuration detected, enter a client ID and secret to authenticate. These can be obtained by creating an OAuth client here: https://insights.planet.com/account
config = SHConfig()
if not config.sh_client_id or not config.sh_client_secret:
    from getpass import getpass
    print('No credentials found, please provide the OAuth client ID and secret.')
    config.sh_client_id = getpass('Client ID: ')
    config.sh_client_secret = getpass('Client Secret: ')
    # config.save() ## Uncomment these lines to locally save your credentials to a configuration file
    # print(f'Credentials saved to {SHConfig.get_config_location()}')
else:
    print(f'Using credentials stored here: {SHConfig.get_config_location()}')
```

#### For Notebooks that use API key authentication

If a notebook is using `requests` instead of the SDK, you will need to use API key authentication.

```
import os
import requests

# Authenticate with the Planet SDK for Python using your API key; See docs: https://docs.planet.com/develop/authentication
# Check for PL_API_KEY environment variable, otherwise type in your API key.
pl_api_key = os.getenv('PL_API_KEY')
if not pl_api_key:
    import getpass
    pl_api_key = getpass.getpass('Planet API Key: ')
    os.environ['PL_API_KEY'] = pl_api_key

session = requests.Session()
session.auth = (pl_api_key, '')
```

And if in the same notebook, you also need to use the SDK, you can use the following:

```
import planet

## Authenticate with the Planet SDK for Python with your API key
auth = planet.Auth.from_key(key=pl_api_key)
pl_session = planet.Session(auth)
pl = planet.Planet(session)
```