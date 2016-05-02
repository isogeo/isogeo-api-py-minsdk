#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from setuptools import setup, find_packages

# custom module
import isogeo_pysdk

# SETUP ######################################################################

setup(
    name="Isogeo API Minimalist SDK",
    version=isogeo_pysdk.__version__,
    packages=find_packages(),
    author="GeoJulien",
    author_email="julien.moura at isogeo.com",
    description="Abstraction class that makes easier using the Isogeo REST API",
    long_description=open("README.rst").read(),
    install_requires=[ "requests>=2.9.1", "arrow>=0.7.0", "pytz>=2015.7" ] ,
    include_package_data=True,
    url="https://github.com/Guts/isogeo-api-py-minsdk",
    keywords = ["GIS", "metadata", "INSPIRE", "Isogeo"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 1 - Planning",
        "License :: GPL3",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Topic :: Data and metadata management",
    ],
)


