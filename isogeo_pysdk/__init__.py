#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module is an abstraction class about the Isogeo REST API.
    https://www.isogeo.com/
"""

from .api_hooks import IsogeoHooks  # noqa: F401
from .checker import IsogeoChecker  # noqa: F401
from .isogeo_sdk import Isogeo, version  # noqa: F401
from .isogeo_sdk_oauth import IsogeoSession  # noqa: F401
from .models import *  # noqa: F401
from .translator import IsogeoTranslator  # noqa: F401
from .utils import IsogeoUtils  # noqa: F401

__version__ = version
VERSION = __version__
