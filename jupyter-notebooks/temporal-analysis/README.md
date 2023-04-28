# Temporal Analysis of Planet Imagery

Planet's daily PlanetScope coverage introduces great potential in temporal analysis.

In this tutorial, we look at the temporal signatures of corn and soybean crops in PlanetScope Orthotiles.
We take advantage of the Cloud-Optimized nature of all
GeoTiffs Planet provides to download only the pixels within the orthotile (and
orthotile unusable data mask). We mask all pixels that are identified as unusable,
then calculate summary statistics on each band.

Please see the [Crop Type Differentiation](croptypedifferentiation.pdf) presentation for a more detailed overview.

## How to Run

There are two python notebooks, `prepare` and `visualize`. These notebooks can be run in the planet docker image as described in the repo README. The processing of the COGs is performed in a script (`temporal2.py`), which is run outside of the docker image, within a virtual environment. The order of operations is:

1. Run `prepare` notebook
1. Run `temporal2.py` script
1. Run `visualize` notebook

### Running temporal2.py

Once your virtualenv is set up (we used [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)), install the dependencies with:

```bash
pip install -r requirements.txt
```

Then run temporal2 for each file that was created by `prepare` in `data/run2/fields/`:
```bash
python temporal2.py --limit 100 <FILENAME>
```

The calculated statistics will be in `data/run2/results/`
