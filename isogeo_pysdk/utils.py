# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, unicode_literals)
# ----------------------------------------------------------------------------

"""
    Complementary set of utils to use with Isogeo API.
"""

# ---------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# 3rd party
import requests

# modules
try:
    from . import checker
except (ImportError, ValueError, SystemError):
    import checker

# ##############################################################################
# ########## Globals ###############
# ##################################

checker = checker.IsogeoChecker()

# ##############################################################################
# ########## Classes ###############
# ##################################


class IsogeoUtils(object):
    """Makes easier the translation of Isogeo API specific strings."""
    API_URLS = {"prod": "api",
                "qa": "api.qa"
                }

    def __init__(self):
        """Set text dictionary depending on language passed."""
        self.platform, self.base_url = self.set_base_url()
        super(IsogeoUtils, self).__init__()

    def get_isogeo_version(self, component="api", prot="https"):
        """
            Get Isogeo components versions.
            Authentication is no required.

            :param str component: one of api [default] | db | app
        """
        # which component
        if component == "api":
            version_url = "{}://v1.{}.isogeo.com/about"\
                          .format(prot,
                                  self.base_url
                                  )
        elif component == "db":
            version_url = "{}://v1.{}.isogeo.com/about/database"\
                          .format(prot,
                                  self.base_url
                                  )
        elif component == "app" and self.platform == "prod":
            version_url = "https://app.isogeo.com/about"
        elif component == "app" and self.platform == "qa":
            version_url = "https://qa-isogeo-app.azurewebsites.net/about"
        elif component == "app" and self.platform == "int":
            version_url = "{}://v1.api.int.hq.isogeo.fr/about"\
                          .format(prot)
        else:
            raise ValueError("Component value is one theses values:"
                             "api [default], db, app.")

        # send request
        try:
            version_req = requests.get(version_url,
                                       proxies=self.proxies
                                       )
        except requests.exceptions.SSLError as e:
            logging.error(e)
            version_req = requests.get(version_url,
                                       proxies=self.proxies,
                                       verify=False
                                       )
        # checking response
        checker.check_api_response(version_req)

        # end of method
        return version_req.json().get("version")

    def set_base_url(self, platform="prod"):
        """
            TO DO
        """
        platform = platform.lower()
        if platform == "prod":
            base_url = self.API_URLS.get(platform)
            logging.debug("Using production platform.")
        elif platform == "qa":
            base_url = self.API_URLS.get(platform)
            logging.debug("Using Quality Assurance platform (reduced perfs).")
        else:
            logging.error("Platform must be one of: {}"
                          .format(" | ".join(self.API_URLS.keys())))
            raise ValueError(3, "Platform must be one of: {}"
                                .format(" | ".join(self.API_URLS.keys())))
        # method ending
        return platform.lower(), base_url


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    """Standalone execution."""
    utils = IsogeoUtils()
    print(utils.set_base_url("prod"))
    print(utils.get_isogeo_version())
