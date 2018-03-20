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
import uuid

# 3rd party
import requests
from six import string_types

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
                "qa": "api.qa",
                # "int": "api.int.hq.isogeo.fr"
                }

    def __init__(self, proxies=dict()):
        """Set text dictionary depending on language passed."""
        self.platform, self.base_url = self.set_base_url()
        self.proxies = proxies
        super(IsogeoUtils, self).__init__()

    def convert_uuid(self, in_uuid=str, mode=0):
        """
           Convert a metadata UUID to its URI equivalent. And conversely.

           :param str in_uuid: UUID or URI to convert
           :param int mode: 0 from UUID to URN\
                             1 from URN to UUID
        """
        # quick parameters check
        if not isinstance(in_uuid, string_types):
            raise TypeError("'in_uuid' expected a str value.")
        else:
            pass
        if not checker.check_is_uuid(in_uuid):
            raise ValueError("{} is not a correct UUID".format(in_uuid))
        else:
            pass
        if not isinstance(mode, int) or mode not in (0, 1):
            raise TypeError("'mode' expected an integer value: 0 or 1")
        else:
            pass
        # handle Isogeo specific UUID in XML exports
        if "isogeo:metadata" in in_uuid:
            in_uuid = "urn:uuid:{}".format(in_uuid.split(":")[-1])
            logging.debug(in_uuid)
        else:
            pass
        # operate
        if mode:
            return uuid.UUID(in_uuid).urn
        else:
            return uuid.UUID(in_uuid).hex

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
            Set API base URLs according to platform.

            :param str platform: one of prod | qa | int
        """
        platform = platform.lower()
        self.platform = platform
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
    print(utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b", mode=1))
    print(utils.convert_uuid(in_uuid="urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=0))
    print(utils.convert_uuid(in_uuid="urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=0))
