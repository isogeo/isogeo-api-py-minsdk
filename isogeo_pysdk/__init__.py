# -*- coding: utf-8 -*-
#! python3

"""
    This module is an abstraction class about the Isogeo REST API.
    https://www.isogeo.com/
"""

from .api_hooks import IsogeoHooks  # noqa: F401
from .checker import IsogeoChecker  # noqa: F401
from .exceptions import AlreadyExistError  # noqa: F401
from .isogeo import Isogeo  # noqa: F401
from .api import *  # noqa: F401
from .enums import *  # noqa: F401
from .models import *  # noqa: F401
from .translator import IsogeoTranslator  # noqa: F401
from .utils import IsogeoUtils  # noqa: F401
from .decorators import ApiDecorators

__version__ = "3.1.0"
VERSION = __version__
