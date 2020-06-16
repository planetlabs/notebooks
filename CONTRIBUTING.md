# Contributing to Notebooks

# Notebooks

## Names

Notebook filenames cannot have spaces. Use underscores instead. This is
because pytest does not like spaces in command line arguments.

## Style

For maximum portability, accessibility, and ease of use, Notebooks in this
repository should not use a custom style or theme. 


## Dependencies

When a new notebook has a dependency that is not yet supported by the Docker image,
a new Docker image must be built. Additionally, add the new dependency to the 
[imports_test notebook](dev/imports_test.ipynb).

## Planet Data

It is the intention of this notebook repository that a user be able to easily
determine the permissions needed within the Planet ecosystem to be able to run
all notebooks successfully. Therefore, we standardize and track Planet data 
that are used across all notebooks within this repository. Right now, this applies
to Planet Imagery in the form of Areas of Interest and to Planet 
Analytic Feeds in the form of suscription IDs.

### Imagery - Area of Interest

The first choice of area of interest (AOI) for any notebook is an AOI that is 
already used in this repository. The geojson description of these AOIs is given
in [aois.geojson](dev/imports_test.ipynb) (it is easy to visualize these
aois directly in GitHub or by copy/pasting into [geojson.io](geojson.io).
These AOIs are also given in the 
[repository_aois notebook](dev/repository_aois.ipynb). It is good practice
to add your notebook to the list of notebooks using each AOI.

If the AOI for a notebook cannot be satisfied by the the AOIs already in use
in the repository, then email <devrel@planet.com> so that we can consider
expanding our demo data coverage to include a new AOI. If the new AOI is included,
add the AOI to the 
[repository_aois notebook](dev/repository_aois.ipynb). Run that notebook
through to the end to update [aois.geojson](dev/imports_test.ipynb).

### Analytics Feed - Subscription ID

The fist choice of Analytics Feed subscription id for any notebooks is a 
subscription ID that is already used in this repository. The subscription IDs
used in this repository are maintained in the
[analygics_feeds notebook](analytics_feeds.ipynb). This notebook also helpfully
pulls the feed information from these subscription IDs. It is good practice
to add your notebook to the list of notebooks using each subscription ID.

Currently, subscription IDs are not being tracked in any demo permissions program.
However, this may change in the future. If the subscription ID for a notebook
cannot be satisfied by the subscription IDs already in the repository, add
the subscription ID to the notebook and email <devrel@planet.com> to notify us
of the change. (**NOTE**: this is likely to change to a request when demo 
permissions for the analytics feed are established).

## Notebook Validation

To enable validation of the Docker image, every notebook should run successfully
when run from the command line. For notebooks where that just is not possible, 
the notebooks can be excluded from automated running by adding its path to 
[tests/skip_notebooks](tests/skip_notebooks). Excluding a notebook from automated running
means that it is excluded from Docker Image validation. **If a notebook is
skipped, it will not be guaranteed to be supported by the Docker image.**

# Docker Image

## Validation

**Every time** the Docker image is changed, at the very least ensure that the 
python packages still import without error by running the
[imports_test notebook](dev/imports_test.ipynb).

It is also strongly recommended that you ensure the Docker image can run all
of the notebooks in the repository. This can be accomplished by automatically
running all of the notebooks using the supplied test script. To run the test script,
run the notebook in interactive mode, achieved by adding `/bin/bash` to 
the container run command, e.g.
```bash
docker run -it --rm -p 8888:8888 \
    -v $PWD:/home/jovyan/work \
    -e PL_API_KEY='[YOUR-API-KEY]' \
    planet-notebooks /bin/bash
```

From the root directory within the docker container, run one of the following:

1. To run all notebooks
    ```bash
    $> pytest tests/test_notebooks.py
    ```
1. run only notebooks in a subdirectory using
    ```bash
    $> pytest tests/test_notebooks.py --path <subdirectory>
    ```
1. run one or more notebooks (separated by spaces)
    ```bash
    $> pytest tests/test_notebooks.py --notebooks <notebook1> <notebook2> <...>
    ```
1. run only notebooks that have a given dependency, <package>
    ```bash
    $> pytest tests/test_notebooks.py --notebooks "$(grep -rl import <package> jupyter-notebooks/)"
   ```

## Skipping Notebooks

Some notebooks are purposefully skipped in the validation process because they
do not run successfully from the command line. These notebooks are specified in
[tests/skip_notebooks](tests/skip_notebooks). Skipping of notebooks within
`skip_notebooks` can be disabled by adding the `--no-skip` option to the pytest
command.
