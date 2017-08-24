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
import logging
from collections import Counter

# ##############################################################################
# ########## Globals ###############
# ##################################

FILTER_KEYS = {"action": [],
               "catalog": [],
               "contact:group": [],
               "contact:isogeo": [],
               "coordinate-system": [],
               "format": [],
               "has-no": [],
               "keyword:isogeo": [],
               "keyword:inspire-theme": [],
               "license:group": [],
               "license:isogeo": [],
               "owner": [],
               "text": [],
               "type": []}

FILTER_TYPES = ("dataset",
                "raster-dataset",
                "vector-dataset",
                "resource",
                "service"
                )


# ##############################################################################
# ########## Classes ###############
# ##################################


class IsogeoChecker(object):
    """Makes easier the translation of Isogeo API specific strings."""

    def __init__(self, lang="FR"):
        """Set text dictionary depending on language passed."""
        super(IsogeoChecker, self).__init__()

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
        dico_query = self.FILTER_KEYS.copy()
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
            elif i.startswith("type"):
                dico_query["type"].append(i.split(":")[1:][0])
                continue
            else:
                print(i.split(":")[1], i.split(":")[1].isdigit())
                dico_query["text"].append(i)
                pass

        # Values
        dico_filters = {i.split(":")[0]: i.split(":")[1:] for i in li_args}
        if dico_filters.get("type", ("dataset",))[0].lower() not in self.FILTER_TYPES:
            raise ValueError("type value must be one of: {}"
                             .format(" | ".join(self.FILTER_TYPES)))
        logging.debug(dico_filters)

# ##############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == '__main__':
    """Standalone execution."""
