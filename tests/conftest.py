import os
from pathlib import Path, PurePath

import pytest

NOTEBOOK_EXT = '.ipynb'
ROOT_DIR = 'jupyter-notebooks'

# do not run notebooks in these directories or sub-directories
SKIP_DIRECTORIES = set(['.ipynb_checkpoints'])

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
            notebook_paths = [Path(n) for n in notebooks]
        else:
            root_path = normalize_path(option_path)
            notebook_paths = get_all_paths(root_path)

        notebook_paths = valid_notebooks(notebook_paths)
        metafunc.parametrize(['notebook_path', 'do_skip'],
                             zip([str(p) for p in notebook_paths],
                                 [do_skip] * len(notebook_paths)))


def normalize_path(path):
    '''If specified path is relative to the ROOT_DIR, then make absolute.'''
    path_parts = list(Path(path).parts)
    if path_parts[0] != ROOT_DIR:
        path_parts = [ROOT_DIR] + path_parts

    return os.path.join(*path_parts)


def get_all_paths(root_dir):
    paths = []
    for path, _, files in os.walk(root_dir):
        for name in files:
            paths.append(PurePath(path, name))
    return paths  


def valid_notebooks(paths):
    '''Filters a list of paths to only include valid notebooks.
    
    Removes paths that include skip directories and paths that do not end
    in notebook extension, .ipynb'''
    valid_paths = [p for p in paths if not _in_skip_dir(p) and _is_notebook(p)]
    print(' {} out of {} paths are valid'.format(len(valid_paths), len(paths)))
    return valid_paths


def _in_skip_dir(path):
    '''path is a Path object'''
    return len(SKIP_DIRECTORIES.intersection(path.parts)) > 0


def _is_notebook(path):
    '''path is a Path object'''
    return path.suffix == NOTEBOOK_EXT
