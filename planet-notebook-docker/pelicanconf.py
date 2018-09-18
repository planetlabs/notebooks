#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# while messing with settings
LOAD_CONTENT_CACHE = False

AUTHOR = 'A Planeteer'
SITENAME = 'Notebooks'
SITESUBTITLE = 'Notebooks written by the Planet team and our users.'
SITEURL = ''
APIDOCS_URL = 'https://docs.planet.com'
NOW = datetime.today()

PATH = 'content'
OUTPUT_PATH = 'public'

TIMEZONE = 'America/Los_Angeles'
DEFAULT_DATE = 'fs'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 6

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'simple'


PLUGIN_PATHS=['./plugins']
# ASSET_CONFIG = (('less_bin', '{}/node_modules/less/bin/lessc'.format(dir_path)), )
PLUGINS = ['ipynb.markup']

# For Notebooks plugin
MARKUP = ('md', 'ipynb')

# notebooks plugin settings
IGNORE_FILES = ['.ipynb_checkpoints']

