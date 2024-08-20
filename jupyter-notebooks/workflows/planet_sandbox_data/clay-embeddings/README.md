# Create Clay Embeddings for Planetscope using PIP

First clone the clay model repository:

```
git clone https://github.com/Clay-foundation/model.git
```

Then install mamba, micromamba or conda. I'll show how to do it with [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html), but everything should work the same:

```
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
micromamba create -n clay -f model/conda-lock.yml
micromamba activate clay
micromamba install -c conda-forge xcube sentinelhub
pip install git+https://github.com/jonasViehweger/xcube-sh.git
```

(The last step needs to be replaced with the official installation once [!116](https://github.com/xcube-dev/xcube-sh/pull/116) is merged)

This should set up the environment so that the notebook can be run.
