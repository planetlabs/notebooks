"""
Run each notebook in the jupyter-notebooks directory.

Notebooks are run using nbconvert.

pytest runs each test as a unit test.
"""
import os
import subprocess
import logging
import tempfile

import pytest

NOTEBOOK_EXT = '.ipynb'


def test_run_notebooks(notebook_path):
    '''Test that the notebook runs successfully'''
    with tempfile.NamedTemporaryFile(suffix=NOTEBOOK_EXT) as tmp_nb:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=600",
                notebook_path, "--output", tmp_nb.name]
        print(' '.join(args))
        subprocess.check_call(args)
