"""
Run each notebook in the jupyter-notebooks directory.

Notebooks are run using nbconvert.

pytest runs each test as a unit test.
"""
import os
import subprocess
import tempfile

import pytest

NOTEBOOK_EXT = '.ipynb'
ROOT_DIR = 'jupyter-notebooks'


def find_notebooks(root_dir):
    print('finding notebooks...')
    notebooks = []
    for (dirpath, dirnames, filenames) in os.walk(root_dir):
        print('{}'.format(dirpath))

        # look for 'norun' file, if present, do not look for notebooks in this dir
        if 'norun' in filenames:
            # do not look into subdirectories, modify in-place for walk()
            dirnames[:] = []

            # clear filenames
            filenames = []

        # modify in place to filter subdirectories in walk()
        # https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
        dirnames[:] = [n for n in dirnames if n != '.ipynb_checkpoints']

        for name in filenames:
            ext = os.path.splitext(name)[1]
            if ext == NOTEBOOK_EXT:
                # convert to string so test displays the path
                notebook_name = str(os.path.join(dirpath, name))
                notebooks.append(notebook_name)
    print('found {} notebooks'.format(len(notebooks)))
    return notebooks


@pytest.mark.parametrize("notebook", find_notebooks(ROOT_DIR))
def test_run_notebooks(notebook):
    with tempfile.NamedTemporaryFile(suffix=NOTEBOOK_EXT) as tmp_nb:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=600",
                notebook, "--output", tmp_nb.name]
        print(' '.join(args))
        subprocess.check_call(args)
