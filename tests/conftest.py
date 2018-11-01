import os
from pathlib import Path

import pytest

NOTEBOOK_EXT = '.ipynb'
ROOT_DIR = 'jupyter-notebooks'

# do not look for notebooks in .ipynb_checkpoints dir
SKIP_DIRECTORIES = ['.ipynb_checkpoints']

def pytest_addoption(parser):
    parser.addoption("--path", action="store",
                     default=ROOT_DIR,
                     help="root directory of notebooks to test")
    parser.addoption("--notebooks",
                     default=None,
                     nargs='*',
                     help="notebook(s) to run. overrides --path command.")
    parser.addoption("--no-skip", action="store_true",
                     default=False,
                     help="avoid skipping notebooks")


def pytest_generate_tests(metafunc):
    '''Generate a test for every notebook found within the root directory.'''
    option_path = metafunc.config.option.path
    notebooks = metafunc.config.option.notebooks
    do_skip = not metafunc.config.option.no_skip

    if 'notebook_path' in metafunc.fixturenames:
        if notebooks:
            notebook_paths = notebooks
        else:
            root_path = normalize_path(option_path)
            notebook_paths = find_notebooks(root_path)

        metafunc.parametrize(['notebook_path', 'do_skip'],
                             zip(notebook_paths, [do_skip] * len(notebook_paths)))


def normalize_path(path):
    '''If specified path is relative to the ROOT_DIR, then make absolute.'''
    path_parts = list(Path(path).parts)
    if path_parts[0] != ROOT_DIR:
        path_parts = [ROOT_DIR] + path_parts

    return os.path.join(*path_parts)


def find_notebooks(root_dir):
    '''Find all of the notebooks within the root directory.

    Skip notebooks and subdirectories of any directory with 'norun' file
    '''
    print('finding notebooks in {}...'.format(root_dir))
    notebooks = []

    for (dirpath, dirnames, filenames) in os.walk(root_dir):
        # modify in place to filter subdirectories in walk()
        # https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
        dirnames[:] = [n for n in dirnames if n not in SKIP_DIRECTORIES]

        for name in filenames:
            ext = os.path.splitext(name)[1]
            if ext == NOTEBOOK_EXT:
                # convert to string so test displays the path
                notebook_name = str(os.path.join(dirpath, name))
                notebooks.append(notebook_name)
    print('found {} notebooks'.format(len(notebooks)))
    return notebooks
