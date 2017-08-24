#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module is an abstraction calls about the Isogeo REST API.
    http://www.isogeo.com/
"""

from .isogeo_sdk import Isogeo
from .checker import IsogeoChecker
from .translator import IsogeoTranslator

__version__ = "2.18.1.2"
VERSION = __version__
