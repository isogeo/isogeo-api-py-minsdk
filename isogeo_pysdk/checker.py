# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, unicode_literals)
# ----------------------------------------------------------------------------

"""
    Complementary set of tools to make some checks on requests to Isogeo API.
"""

# Created:      18/08/2017
# ---------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from collections import Counter
import logging
from six import string_types
import socket
from uuid import UUID

# ##############################################################################
# ########## Globals ###############
# ##################################

FILTER_KEYS = {"action": [],
               "catalog": [],
               "contact:group": [],
               "contact:isogeo": [],
               "coordinate-system": [],
               "data-source": [],
               "format": [],
               "has-no": [],
               "keyword:isogeo": [],
               "keyword:inspire-theme": [],
               "license:group": [],
               "license:isogeo": [],
               "owner": [],
               "provider": [],
               "text": [],
               "type": []}

FILTER_ACTIONS = ("download",
                  "other",
                  "view"
                  )

FILTER_PROVIDERS = ("manual",
                    "auto"
                    )

FILTER_TYPES = ("dataset",
                "raster-dataset",
                "vector-dataset",
                "resource",
                "service"
                )

WG_KEYWORDS_CASING = ("capitalized",
                      "lowercase",
                      "mixedCase",
                      "uppercase",
                      )

EDIT_TABS = {"identification": ",".join(FILTER_TYPES),
             "history": ",".join(FILTER_TYPES),
             "geography": "dataset, raster-dataset, vector-dataset, service",
             "quality": "dataset, raster-dataset, vector-dataset, service",
             "attributes": "vector-dataset, series",
             "constraints": ",".join(FILTER_TYPES),
             "resources": ",".join(FILTER_TYPES),
             "contacts": ",".join(FILTER_TYPES),
             "advanced": ",".join(FILTER_TYPES),
             "metadata": ",".join(FILTER_TYPES),
             }

# ##############################################################################
# ########## Classes ###############
# ##################################


class IsogeoChecker(object):
    """Makes easier the translation of Isogeo API specific strings."""

    def __init__(self, lang="FR"):
        """Set text dictionary depending on language passed."""
        super(IsogeoChecker, self).__init__()

    def check_internet_connection(self, remote_server="www.isogeo.com"):
        """
            Test if an internet connection is operational.

            source: http://stackoverflow.com/a/20913928/2556577
        """
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(remote_server)
            # connect to the host -- tells us if it's reachable
            sock = socket.create_connection((host, 80), 2)
            sock.close()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def check_bearer_validity(self, token, connect_mtd):
        """Check API Bearer token validity.

        Isogeo ID delivers authentication bearers which are valid during
        24h, so this method checks the validity of the token (token in French)
        with a 30 mn anticipation limit, and renews it if necessary.

        token = must be a tuple like (bearer, expiration_date)

        see: http://tools.ietf.org/html/rfc6750#section-2
        FI: 24h = 86400 seconds, 30 mn = 1800, 5 mn = 300
        """
        if token[1] < 60:
            token = connect_mtd
            logging.debug("Token was about to expire, so has been renewed.")
        else:
            logging.debug("Token is still valid.")
            pass

        # end of method
        return token

    def check_api_response(self, response):
        """Check API response and raise exceptions if needed."""
        if response.status_code == 200:
            logging.debug("Everything is OK dude, just go on!")
            pass
        elif response.status_code >= 400:
            logging.error("Something's wrong Houston, check settings again!")
            # logging.error(dir(response.request))
            logging.error("{}: {} - {} - URL: {}"
                          .format(response.status_code,
                                  response.reason,
                                  response.json().get("error"),
                                  response.request.url))
            # logging.error(dir(response))
            return 0, response.status_code
        else:
            pass

        # end of method
        return 1

    def check_request_parameters(self, parameters={}):
        """Check parameters passed to avoid errors and help debug."""
        # FILTERS
        li_args = parameters.get("q").split()
        logging.debug(li_args)
        # li_values = [i.split(":")[1:] for i in li_args]

        # Unicity
        li_filters = [i.split(":")[0] for i in li_args]
        filters_count = Counter(li_filters)
        li_filters_must_be_unique = ("coordinate-system",
                                     "format",
                                     "owner",
                                     "type")

        for i in filters_count:
            if i in li_filters_must_be_unique and filters_count.get(i) > 1:
                raise ValueError("This query filter must be unique: {}"
                                 " and it occured {} times."
                                 .format(i, filters_count.get(i)))

        # dict
        dico_query = FILTER_KEYS.copy()
        for i in li_args:
            if i.startswith("action"):
                dico_query["action"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("catalog"):
                dico_query["catalog"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("contact") and i.split(":")[1] == "group":
                dico_query["contact:group"].append(i.split(":")[1:][1])
                continue
            elif i.startswith("contact"):
                dico_query["contact:isogeo"].append(i.split(":", 1)[1])
                continue
            elif i.startswith("coordinate-system"):
                dico_query["coordinate-system"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("data-source"):
                dico_query["data-source"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("format"):
                dico_query["format"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("has-no"):
                dico_query["has-no"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("keyword:isogeo"):
                dico_query["keyword:isogeo"].append(i.split(":")[1:][1])
                continue
            elif i.startswith("keyword:inspire-theme"):
                dico_query["keyword:inspire-theme"].append(i.split(":")[1:][1])
                continue
            elif i.startswith("license:isogeo"):
                dico_query["license:isogeo"].append(i.split(":")[1:][1:])
                continue
            elif i.startswith("license"):
                dico_query["license:group"].append(i.split(":", 1)[1:][0:])
                continue
            elif i.startswith("owner"):
                dico_query["owner"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("provider"):
                dico_query["provider"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("type"):
                dico_query["type"].append(i.split(":")[1:][0])
                continue
            else:
                logging.debug(i.split(":")[1], i.split(":")[1].isdigit())
                dico_query["text"].append(i)
                pass

        # Values
        dico_filters = {i.split(":")[0]: i.split(":")[1:] for i in li_args}
        if dico_filters.get("type", ("dataset",))[0].lower() not in FILTER_TYPES:
            raise ValueError("type value must be one of: {}"
                             .format(" | ".join(FILTER_TYPES)))
        elif dico_filters.get("action", ("download",))[0].lower() not in FILTER_ACTIONS:
            raise ValueError("action value must be one of: {}"
                             .format(" | ".join(FILTER_ACTIONS)))
        elif dico_filters.get("provider", ("manual",))[0].lower() not in FILTER_PROVIDERS:
            raise ValueError("provider value must be one of: {}"
                             .format(" | ".join(FILTER_PROVIDERS)))
        else:
            logging.debug(dico_filters)

    def check_is_uuid(self, uuid_str):
        """
            Check if it's an Isogeo UUID.

            :param str uuid_str: UUID string to check
        """
        # handle Isogeo specific UUID in XML exports
        if "isogeo:metadata" in uuid_str:
            uuid_str = "urn:uuid:{}".format(uuid_str.split(":")[-1])
        else:
            pass
        # test it
        try:
            uid = UUID(uuid_str)
            return uid.hex == uuid_str.replace('-', '')\
                                      .replace('urn:uuid:', '')
        except ValueError as e:
            logging.error("uuid ValueError. {} ({})  -- {}"
                          .format(type(uuid_str), uuid_str, e))
            return False
        except TypeError:
            logging.error("uuid must be a string. Not: {} ({})"
                          .format(type(uuid_str), uuid_str))
            return False

    def check_edit_tab(self, tab, md_type):
        """
           Check if asked tab is part of Isogeo web form.
           Can also apply a strict mode to filter depending on metadata type.

           :param str tab: tab to check
           :param bool md_type: option to apply the strict mode
        """
        # check parameters types
        if not isinstance(tab, string_types):
            raise TypeError("'tab' expected a str value.")
        else:
            pass
        if not isinstance(md_type, string_types):
            raise TypeError("'md_type' expected a str value.")
        else:
            pass
        # check parameters values
        if tab not in EDIT_TABS:
            raise ValueError("'{}' isn't a valid edition tab. "
                             "Available values: {}"
                             .format(tab, " | ".join(EDIT_TABS))
                             )
        else:
            pass
        if md_type not in FILTER_TYPES:
            raise ValueError("'{}' isn't a valid metadata type. "
                             "Available values: {}"
                             .format(tab, " | ".join(FILTER_TYPES))
                             )
        else:
            pass
        # check adequation tab/md_type
        if md_type not in EDIT_TABS.get(tab):
            raise ValueError("'{}'  isn't a valid tab for a '{}'' metadata."
                             " Only for these types: {}."
                             .format(tab, md_type, EDIT_TABS.get(tab))
                             )
            return False
        else:
            pass
        return True


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    """Standalone execution."""
    checker = IsogeoChecker()
