#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Setup script to package Isogeo PySDK Python module

    see: https://github.com/Guts/isogeo-api-py-minsdk/
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from codecs import open
from os import path
from setuptools import setup, find_packages

# package (to get version)
import isogeo_pysdk

# SETUP ######################################################################

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# intentionally *not* adding an encoding option to open, See:
#   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

# setup metadata
setup(
    # meta
    name="isogeo-pysdk",
    version=isogeo_pysdk.__version__,
    author="Isogeo",
    author_email="support@isogeo.com",
    description="Abstraction class to use Isogeo REST API",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords="GIS metadata INSPIRE Isogeo API REST geographical data ISO19139",
    license='GPL3',
    url="https://github.com/Guts/isogeo-api-py-minsdk",
    project_urls={
        'Bug Reports': 'https://github.com/Guts/isogeo-api-py-minsdk/issues',
        'Source': 'https://github.com/Guts/isogeo-api-py-minsdk',
        'Docs - Isogeo API': 'https://www.gitbook.com/book/isogeo/api/details',
    },
    # dependencies
    install_requires=["requests>=2.9.1",
                      "future",
                      "six"
                      ],
    extras_require={
        "dev": ["configparser"],
        "test": ["coverage", "pycodestyle", "python-dateutil"],
    },
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    # packaging
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
