#!/usr/bin/env python3

# based on https://github.com/kennethreitz/setup.py/blob/master/setup.py

import io
import os

from setuptools import setup, find_packages

NAME = 'SysrepoLibrary'
DESCRIPTION = 'A testing library for Robot Framework that utilizes the Sysrepo tool internally.'
URL = 'https://lab.sartura.hr/dt/robotframework-sysrepolibrary'
EMAIL = 'juraj.vijtiuk@sartura.hr'
AUTHOR = 'Juraj Vijtiuk'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None  # read __version__.py, a single canonical place for version information

REQUIRED = [
    'robotframework',
    'sysrepo',
]

here = os.path.abspath(os.path.dirname(__file__))

# README.md must be present in MANIFEST.in
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace('-', '_').replace(' ', '_')
    with open(os.path.join(here, 'src', '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=REQUIRED,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    license='None',
)
