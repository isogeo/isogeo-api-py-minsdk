# Metadata bout the package to easily retrieve informations about it.
# see: https://packaging.python.org/guides/single-sourcing-package-version/

import os.path

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None


__title__ = "Isogeo Python SDK"
__summary__ = "API wrapper for the Isogeo REST API"
__uri__ = "https://pypi.org/project/isogeo-pysdk/"

__version__ = "3.1.0"

__author__ = "Isogeo"
__email__ = "contact@isogeo.com"

__license__ = "GNU Lesser General Public License v3.0"
__copyright__ = "2016 %s" % __author__
