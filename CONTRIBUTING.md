# Contributing to Notebooks

# Notebooks

## Names

Notebook filenames cannot have spaces. Use underscores instead. This is
because pytest does not like spaces in command line arguments.

## Dependencies

When a new notebook has a dependency that is not yet supported by the Docker image,
a new Docker image must be built. Additionally, add the new dependency to the 
[imports_test notebook](dev/imports_test.ipynb).

## Area of Interest

The first choice of area of interest (AOI) for any notebook is an AOI that is 
already used in this repository. The geojson description of these AOIs is given
in [aois.geojson](dev/imports_test.ipynb) (it is easy to visualize these
aois directly in GitHub or by copy/pasting into [geojson.io](geojson.io).
These AOIs are also given in the 
[repository_aois notebook](dev/repository_aois.ipynb). It is good practice
to add your notebook to the list of notebooks using each AOI.

If the AOI for a notebook cannot be satisfied by the the AOIs already in use
in the repository, then email <devrel@planet.com> to request that the demo
data coverage be expanded to include the new AOI. Once approved, add the AOI to the 
[repository_aois notebook](dev/repository_aois.ipynb). Run that notebook
through to the end to update [aois.geojson](dev/imports_test.ipynb).

## Skipping Validation

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
