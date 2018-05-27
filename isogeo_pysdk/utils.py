# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# ----------------------------------------------------------------------------

"""
    Complementary set of utils to use with Isogeo API.
"""

# ---------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from __future__ import (absolute_import, unicode_literals)
from configparser import SafeConfigParser
import logging
import json
from os import path
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
          * 1 to URN (RFC4122)
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
        """Get Isogeo components versions. Authentication not required.

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

        :param str webapp: web app destination
        :param dict kwargs: web app specific parameters. For example see WEBAPPS
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

    # -- SEARCH  --------------------------------------------------------------
    def tags_to_dict(self, tags=dict):
        """Reverse search tags dictionary to values as keys.
        Useful to populate filters combobex for example.

        :param dict tags: tags dictionary from a search request
        """
        # tags dicts
        tags_as_dicts = {"actions": {},
                         "catalogs": {},
                         "contacts": {},
                         "data-sources": {},
                         "formats": {},
                         "inspires": {},
                         "keywords": {},
                         "licenses": {},
                         "owners": {},
                         "providers": {},
                         "shares": {},
                         "srs": {},
                         "types": {},
                         }

        # parsing tags and storing each one in a dict
        i = 0
        for k, v in sorted(tags.items()):
            i += 1
            if k.startswith("action"):
                tags_as_dicts.get("actions")[v] = k
                continue
            elif k.startswith("catalog"):
                tags_as_dicts.get("catalogs")[v] = k
                continue
            elif k.startswith("contact"):
                if v not in tags_as_dicts.get("contacts"):
                    tags_as_dicts.get("contacts")[v] = k
                else:
                    logging.warning("Duplicated contact name: {}.".format(v))
                    tags_as_dicts.get("contacts")[v] += "|" + k
                continue
            elif k.startswith("coordinate-system"):
                tags_as_dicts.get("srs")[v] = k
                continue
            elif k.startswith("data-source"):
                tags_as_dicts.get("data-sources")[v] = k
                continue
            elif k.startswith("format"):
                tags_as_dicts.get("formats")[v] = k
                continue
            elif k.startswith("keyword:in"):
                tags_as_dicts.get("inspires")[v] = k
                continue
            elif k.startswith("keyword:is"):
                tags_as_dicts.get("keywords")[v] = k
                continue
            elif k.startswith("license"):
                if v not in tags_as_dicts.get("licenses"):
                    tags_as_dicts.get("licenses")[v] = k
                else:
                    logging.warning("Duplicated contact name: {}.".format(v))
                    tags_as_dicts.get("licenses")[v] += "|" + k
                continue
            elif k.startswith("owner"):
                tags_as_dicts.get("owners")[v] = k
                continue
            elif k.startswith("provider"):
                tags_as_dicts.get("providers")[v] = k
                continue
            elif k.startswith("share"):
                tags_as_dicts.get("shares")[v] = k
                continue
            elif k.startswith("type"):
                tags_as_dicts.get("types")[v] = k
                continue
            # ignored tags
            else:
                logging.warning("Tags have been ignored during parsing: {}"
                                .format(k))
        print(len(tags), i)

        # return the output
        return tags_as_dicts

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
    def credentials_loader(self, in_credentials="client_secrets.json"):
        """Loads API credentials from a file, JSON or INI.

        :param str in_credentials: path to the credentials file. By default,
          look for a client_secrets.json file.
        """
        accepted_extensions = (".ini", ".json")
        # checks
        if not path.isfile(in_credentials):
            raise IOError("Credentials file doesn't exist: {}"
                          .format(in_credentials))
        else:
            in_credentials = path.normpath(in_credentials)
        if path.splitext(in_credentials)[1] not in accepted_extensions:
            raise ValueError("Extension of credentials file must be one of {}"
                             .format(accepted_extensions))
        else:
            kind = path.splitext(in_credentials)[1]
        # load, check and set
        if kind == ".json":
            with open(in_credentials, "r") as f:
                in_auth = json.loads(f.read())
            # check structure
            heads = ("installed", "web")
            if not set(in_auth).intersection(set(heads)):
                raise ValueError("Input JSON structure is not as expected."
                                 " First key must be one of: {}".format(heads))
            # set
            if "web" in in_auth:
                # json structure for group application
                auth_settings = in_auth.get("web")
                out_auth = {
                    "auth_mode": "group",
                    "client_id": auth_settings.get("client_id"),
                    "client_secret": auth_settings.get("client_secret"),
                    "uri_auth": auth_settings.get("auth_uri"),
                    "uri_token": auth_settings.get("token_uri"),
                    "uri_redirect": None,
                }
            else:
                # assuming in_auth == 'installed'
                auth_settings = in_auth.get("installed")
                out_auth = {
                    "auth_mode": "user",
                    "client_id": auth_settings.get("client_id"),
                    "client_secret": auth_settings.get("client_secret"),
                    "uri_auth": auth_settings.get("auth_uri"),
                    "uri_token": auth_settings.get("token_uri"),
                    "uri_redirect": auth_settings.get("redirect_uris"),
                }
        else:
            # assuming file is an .ini
            ini_parser = SafeConfigParser()
            ini_parser.read(in_credentials)
            # check structure
            if 'auth' in ini_parser._sections:
                in_auth = ini_parser['auth']
            else:
                raise ValueError("Input INI structure is not as expected."
                                 " Section of credentials must be named: auth")
            # set
            out_auth = {
                "auth_mode": in_auth.get("CLIENT_TYPE"),
                "client_id": in_auth.get("CLIENT_ID"),
                "client_secret": in_auth.get("CLIENT_SECRET"),
                "uri_auth": in_auth.get("URI_AUTH"),
                "uri_token": in_auth.get("URI_TOKEN"),
                "uri_redirect": in_auth.get("URI_REDIRECT"),
            }
        # method ending
        return out_auth


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    """Standalone execution."""
    utils = IsogeoUtils()
    in_search = path.normpath(r"samples/out_api_search_basic.json")
    with open(in_search, "r") as f:
        search = json.loads(f.read())
    tags = search.get("tags")
    cts = [i for i in tags if i.startswith("contact")]
    t = utils.tags_to_dict(tags)
    print(len(cts))
    print(len(t.get("contacts")))
    print(t.get("contacts").keys(), sep="\n")
    print(t.get("contacts").get("BRGM"))
