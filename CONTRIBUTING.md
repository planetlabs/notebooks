# Contributing to Notebooks

## Docker Image Validation

The docker image must be able to run all notebooks. Whenever a change is made to
the docker image, it must be validated. This can be accomplished by automatically
running all of the notebooks using the supplied test script. From the root
directory within the docker container, run:
```
$> pytest tests/test_notebooks.py
```
## Automated Running and Skipping

To enable validation of the Docker image, every notebook should run successfully
when run from the command line. For notebooks where that just is not possible, 
the notebooks can be excluded from automated running by adding a file named
`norun` to the notebook directory. Note that this results in the entire directory
of notebooks being skipped. Excluding a notebook from automated running
means that it is excluded from Docker Image validation. **If a notebook is
skipped, it will not be guaranteed to be supported by the Docker image.**
