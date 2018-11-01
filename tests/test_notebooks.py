"""
Run each notebook in the jupyter-notebooks directory.

Notebooks are run using nbconvert.

pytest runs each test as a unit test.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile

import pytest

SKIP_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'skip_notebooks')

ROOT_DIR = 'jupyter-notebooks'
NOTEBOOK_EXT = '.ipynb'


def is_skipped_path(notebook_path):
    is_skipped = False
    for skipped_path in get_skipped_paths():
        skipped_path_parts = [ROOT_DIR] + list(Path(skipped_path).parts)
        notebook_path_parts = list(Path(notebook_path).parts)

        # determine if skipped path is a parent dir of notebook path
        # https://stackoverflow.com/a/32149245/2344416
        if notebook_path_parts[:len(skipped_path_parts)] == skipped_path_parts:
            is_skipped = True
            break

    return is_skipped


def get_skipped_paths():
    with open(SKIP_FILE, 'r') as f:
        lines = f.readlines()

    # remove comments and whitespace characters
    def _strip_comments(line):
        return re.sub(r'(?m) *#.*\n?', '', line)
    lines = [_strip_comments(l).strip() for l in lines]

    # remove empty lines
    lines = [l for l in lines if l]
    return lines 


def test_run_notebooks(notebook_path, do_skip):
    '''Test that the notebook runs successfully'''
    if is_skipped_path(notebook_path) and do_skip:
        pytest.skip('Notebook skipped as specified in {}'.format(SKIP_FILE))

    with tempfile.NamedTemporaryFile(suffix=NOTEBOOK_EXT) as tmp_nb:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=600",
                notebook_path, "--output", tmp_nb.name]
        print(' '.join(args))
        subprocess.check_call(args)
