#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Setup script to package isogeo PySDK Python module

    see: https://github.com/Guts/isogeo-api-py-minsdk/
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from codecs import open
from os import path
from setuptools import setup, find_packages

# custom module
import isogeo_pysdk

# SETUP ######################################################################

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # meta
    name="isogeo-pysdk",
    version=isogeo_pysdk.__version__,
    author="GeoJulien for Isogeo",
    author_email="julien.moura@isogeo.com",
    description="Abstraction class to use Isogeo REST API",
    long_description=long_description,
    keywords=["GIS", "metadata", "INSPIRE", "Isogeo",
              "API", "REST", "geographical data"],
    license='GPL3',
    url="https://github.com/Guts/isogeo-api-py-minsdk",
    # dependencies
    install_requires=["requests>=2.9.1",
                      "future",
                      "six"
                      ],
    extras_require={
        ":python_version == '2.7'": [
            "configparser",
            "six"
        ],
    },
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
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
