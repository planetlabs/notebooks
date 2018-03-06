import os
import subprocess

# import nbformat
# from nbconvert.preprocessors import ExecutePreprocessor
import pytest

ROOT_DIR = '.'


def find_notebooks(root_dir):
    print(os.listdir(root_dir))
    notebook_ext = '.ipynb'

    notebooks = []
    for (dirpath, dirnames, filenames) in os.walk(root_dir):
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
            if ext == notebook_ext:
                # convert to string so test displays the path
                notebook_name = str(os.path.join(dirpath, name))
                print(notebook_name)
                print(type(notebook_name))
                notebooks.append(notebook_name)

    return notebooks


@pytest.mark.parametrize("notebook", find_notebooks(ROOT_DIR))
def test_run_notebooks(notebook):
    args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
            "--ExecutePreprocessor.timeout=600",
            notebook]
    subprocess.check_call(args)
