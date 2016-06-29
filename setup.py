#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    name="isogeo-pysdk",
    version=isogeo_pysdk.__version__,
    packages=find_packages(),
    author="GeoJulien",
    author_email="julien.moura at isogeo.com",
    description="Abstraction class to use Isogeo REST API",
    install_requires=["requests>=2.9.1", "arrow>=0.7.0", "pytz>=2015.7"],
    include_package_data=True,
    url="https://github.com/Guts/isogeo-api-py-minsdk",
    keywords=["GIS", "metadata", "INSPIRE", "Isogeo"],
    license='GPL3',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=long_description,
)
