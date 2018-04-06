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
    """Complementary set of utilitary methods and functions to make it easier
    using Isogeo API.
    """
    API_URLS = {"prod": "api",
                "qa": "api.qa",
                }

    APP_URLS = {"prod": "https://app.isogeo.com",
                "qa": "https://qa-isogeo-app.azurewebsites.net",
                }

    CSW_URLS = {"prod": "https://app.isogeo.com",
                "qa": "http://services.api.qa.isogeo.com",
                }

    MNG_URLS = {"prod": "https://manage.isogeo.com",
                "qa": "https://qa-isogeo-manage.azurewebsites.net",
                }

    OC_URLS = {"prod": "https://open.isogeo.com",
               "qa": "https://qa-isogeo-open.azurewebsites.net",
               }

    WEBAPPS = {"csw_getcap": {"args": ("share_id", "share_token"),
                              "url": "https://services.api.isogeo.com/ows/s/"
                                     "{share_id}/{share_token}?service=CSW"
                                     "&version=2.0.2&request=GetCapabilities"
                              },
               "csw_getrec": {"args": ("md_uuid_urn",
                                       "share_id",
                                       "share_token"),
                              "url": "https://services.api.isogeo.com/ows/s/"
                                     "{share_id}/{share_token}?service=CSW"
                                     "&version=2.0.2&request=GetRecordById"
                                     "&id={md_uuid_urn}&elementsetname=full"
                                     "&outputSchema=http://www.isotc211.org/2005/gmd"
                              },
               "oc": {"args": ("md_id", "share_id", "share_token"),
                      "url": "https://open.isogeo.com/s/{share_id}"
                             "/{share_token}/r/{md_id}"
                      },
               "pixup_portal": {"args": ("md_id", "portal_url", ),
                                "url": "http://{portal_url}/?muid={md_id}"
                                },
               }

    def __init__(self, proxies=dict()):
        """Instanciate IsogeoUtils module.

        :param dict proxies: dictionary of proxy settings as described in
         requests. See: http://docs.python-requests.org/en/master/user/advanced/#proxies
        """
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url,\
            self.oc_url, self.ssl = self.set_base_url()
        self.proxies = proxies
        super(IsogeoUtils, self).__init__()

    def set_base_url(self, platform="prod"):
        """Set Isogeo base URLs according to platform.

        :param str platform: platform to use. Available values:
           * prod [DEFAULT]
           * qa
           * int

        """
        platform = platform.lower()
        self.platform = platform
        if platform == "prod":
            ssl = True
            logging.debug("Using production platform.")
        elif platform == "qa":
            ssl = False
            logging.debug("Using Quality Assurance platform (reduced perfs).")
        else:
            logging.error("Platform must be one of: {}"
                          .format(" | ".join(self.API_URLS.keys())))
            raise ValueError(3, "Platform must be one of: {}"
                                .format(" | ".join(self.API_URLS.keys())))
        # method ending
        return platform.lower(),\
            self.API_URLS.get(platform),\
            self.APP_URLS.get(platform),\
            self.CSW_URLS.get(platform),\
            self.MNG_URLS.get(platform),\
            self.OC_URLS.get(platform),\
            ssl

    def convert_uuid(self, in_uuid=str, mode=0):
        """Convert a metadata UUID to its URI equivalent. And conversely.

        :param str in_uuid: UUID or URI to convert
        :param int mode: options:
          * 0 to HEX
          * 1 to URN (RFC4122)\
          * 2 to URN (Isogeo specific style)

        """
        # parameters check
        if not isinstance(in_uuid, string_types):
            raise TypeError("'in_uuid' expected a str value.")
        else:
            pass
        if not checker.check_is_uuid(in_uuid):
            raise ValueError("{} is not a correct UUID".format(in_uuid))
        else:
            pass
        if not isinstance(mode, int):
            raise TypeError("'mode' expects an integer value")
        else:
            pass
        # handle Isogeo specific UUID in XML exports
        if "isogeo:metadata" in in_uuid:
            in_uuid = "urn:uuid:{}".format(in_uuid.split(":")[-1])
            logging.debug("Isogeo UUUID URN spotted: {}".format(in_uuid))
        else:
            pass
        # operate
        if mode == 0:
            return uuid.UUID(in_uuid).hex
        elif mode == 1:
            return uuid.UUID(in_uuid).urn
        elif mode == 2:
            urn = uuid.UUID(in_uuid).urn
            return "urn:isogeo:metadata:uuid:{}".format(urn.split(":")[2])
        else:
            raise ValueError("'mode' must be  one of: 0 | 1 | 2")

    def get_isogeo_version(self, component="api", prot="https"):
        """Get Isogeo components versions.
        Authentication is no required.

        :param str component: options:
          * api [default]
          * db
          * app

        """
        # which component
        if component == "api":
            version_url = "{}://v1.{}.isogeo.com/about"\
                          .format(prot,
                                  self.api_url
                                  )
        elif component == "db":
            version_url = "{}://v1.{}.isogeo.com/about/database"\
                          .format(prot,
                                  self.api_url
                                  )
        elif component == "app" and self.platform == "prod":
            version_url = "https://app.isogeo.com/about"
        elif component == "app" and self.platform == "qa":
            version_url = "https://qa-isogeo-app.azurewebsites.net/about"
        else:
            raise ValueError("Component value must be one of: "
                             "api [default], db, app.")

        # send request
        version_req = requests.get(version_url,
                                   proxies=self.proxies,
                                   verify=self.ssl
                                   )

        # checking response
        checker.check_api_response(version_req)

        # end of method
        return version_req.json().get("version")

    # -- URLs builders -------------------------------------------------------
    def get_edit_url(self, md_id=str, md_type=str, owner_id=str, tab="identification"):
        """Constructs the edition URL of a metadata.

        :param str md_id: metadata/resource UUID
        :param str owner_id: owner UUID
        :param str tab: target tab in the web form
        """
        # checks inputs
        if not checker.check_is_uuid(md_id)\
           or not checker.check_is_uuid(owner_id):
            raise ValueError("One of md_id or owner_id is not a correct UUID.")
        else:
            pass
        if checker.check_edit_tab(tab, md_type=md_type):
            pass
        # construct URL
        return "{}" \
               "/groups/{}" \
               "/resources/{}" \
               "/{}".format(self.APP_URLS.get(self.platform),
                            owner_id,
                            md_id, tab)

    def get_view_url(self, webapp="oc", **kwargs):
        """Constructs the view URL of a metadata.

        :param str webapp: web app destination.
        :param dict \**kwargs: web app specific parameters.
         For example see WEBAPPS
        """
        # build wbeapp URL depending on choosen webapp
        if webapp in self.WEBAPPS:
            webapp_args = self.WEBAPPS.get(webapp).get("args")
            # check kwargs parameters
            if set(webapp_args) <= set(kwargs):
                # construct and return url
                url = self.WEBAPPS.get(webapp).get("url")

                return url.format(**kwargs)
            else:
                raise TypeError("'{}' webapp expects {} argument(s): {}."
                                " Args passed: {}"
                                .format(webapp,
                                        len(webapp_args),
                                        webapp_args,
                                        kwargs))
        else:
            raise ValueError("'{}' is not a recognized webapp among: {}."
                             " Try to register it."
                             .format(self.WEBAPPS.keys(), webapp))

    def register_webapp(self, webapp_name, webapp_args, webapp_url):
        """Register a new WEBAPP to use with the view URL builder.

        :param str webapp_name: name of the web app to register
        :param list webapp_args: dynamic arguments to complete the URL.
         Typically 'md_id'.
        :param str webapp_url: URL of the web app to register with
         args tags to replace. Example:
         'https://www.ppige-npdc.fr/portail/geocatalogue?uuid={md_id}'
        """
        # check parameters
        for arg in webapp_args:
            if arg not in webapp_url:
                raise ValueError("Inconsistent web app arguments and URL."
                                 " It should contain arguments to replace"
                                 " dynamically. Example: 'http://webapp.com"
                                 "/isogeo?metadata={md_id}'")
        # register
        self.WEBAPPS[webapp_name] = {"args": webapp_args,
                                     "url": webapp_url}

    # -- SHARES MANAGEMENT ----------------------------------------------------
    def share_extender(self, share, results_filtered):
        """Extend share model with additional informations.

        :param dict share: share returned by API
        """
        # add share administration URL
        creator_id = share.get("_creator").get("_tag")[6:]
        share["admin_url"] = "{}/groups/{}/admin/shares/{}"\
                             .format(self.app_url,
                                     creator_id,
                                     share.get("_id"))
        # check if OpenCatalog is activated
        opencat_url = "{}/s/{}/{}"\
                      .format(self.oc_url,
                              share.get("_id"),
                              share.get("urlToken"))
        if requests.head(opencat_url):
            share["oc_url"] = opencat_url
        else:
            pass
        # add metadata ids list
        share["mds_ids"] = (i.get("_id") for i in results_filtered)

        return share

    # -- API AUTH ------------------------------------------------------------
    # def credentials_loader(self, f_json, f_ini, e_vars):
    #     """Loads API credentials from a file or environment variables.

    #     :param str f_json: path to the credentials JSON file:
    #     :param str f_ini: path to the credentials INI file
    #     :param dict e_vars: dict of environment variables names
    #     """
    #     if f_ini:
    #         with open('client_secrets.json', "r") as j:
    #             api = json.loads(j.read()).get("installed")
    #         return api
    #     elif f_json:
    #         with open('client_secrets.json', "r") as j:
    #             api = json.loads(j.read()).get("installed")
    #         return api
    #     elif e_vars:
    #         with open('client_secrets.json', "r") as j:
    #             api = json.loads(j.read()).get("installed")
    #         return api
    #     else:
    #         raise ValueError()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    """Standalone execution."""
    utils = IsogeoUtils()
    # from HEX
    print("hex to hex - " + utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b", mode=0))
    print("hex to urn (RFC4122) - " + utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b", mode=1))
    print("hex to urn (isogeo style) - " + utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b", mode=2))
    # from URN (RFC4122)
    print("\nurn (RFC4122) to hex - " + utils.convert_uuid(in_uuid="urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=0))
    print("urn (RFC4122) to urn (RFC4122) - " + utils.convert_uuid(in_uuid="urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=1))
    print("urn (RFC4122) to urn (Isogeo style) - " + utils.convert_uuid(in_uuid="urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=2))
    # from URN (Isogeo style)
    print("\nurn (Isogeo style) to hex - " + utils.convert_uuid(in_uuid="urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=0))
    print("urn (Isogeo style) to urn (RFC4122) - " + utils.convert_uuid(in_uuid="urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=1))
    print("urn (Isogeo style) to urn (Isogeo style) - " + utils.convert_uuid(in_uuid="urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b", mode=2))
