# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Offline parser
# Purpose:      Exports each of 10 last updated metadata into an XML ISO19139
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      02/11/2017
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
from os import path
import sys

# ############################################################################
# ########## Functions #############
# ##################################


def search_tags_as_filters(tags):
    """Get different tags as dicts ready to use as dropdown lists."""
    # set dicts
    actions = {}
    contacts = {}
    formats = {}
    inspire = {}
    keywords = {}
    licenses = {}
    md_types = {}
    owners = {}
    srs = {}
    unused = {}
    # looking for a global type:dataset
    type_dataset = 0
    # parsing tags
    for tag in sorted(tags.keys()):
        # actions
        if tag.startswith('action'):
            actions[tags.get(tag, tag)] = tag
            continue
        # contacts
        elif tag.startswith('contact'):
            contacts[tags.get(tag)] = tag
            continue
        # formats
        elif tag.startswith('format'):
            formats[tags.get(tag)] = tag
            continue
        # INSPIRE themes
        elif tag.startswith('keyword:in'):
            inspire[tags.get(tag)] = tag
            continue
        # keywords
        elif tag.startswith('keyword:is'):
            keywords[tags.get(tag)] = tag
            continue
        # licenses
        elif tag.startswith('license'):
            licenses[tags.get(tag)] = tag
            continue
        # owners
        elif tag.startswith('owner'):
            owners[tags.get(tag)] = tag
            continue
        # SRS
        elif tag.startswith('coordinate-system'):
            srs[tags.get(tag)] = tag
            # print(tag)
            continue
        # types
        elif tag.startswith('type'):
            md_types[tags.get(tag)] = tag
            if tag in ("type:vector-dataset", "type:raster-dataset"):
                type_dataset += 1
            continue
        # ignored tags
        else:
            unused[tags.get(tag, tag)] = tag
            continue

    # override API tags to allow all datasets filter - see #
    if type_dataset == 2:
        md_types["Donnée"] = "type:dataset"
    else:
        pass

    # storing dicts
    tags_parsed = {}
    tags_parsed["actions"] = sorted(actions)
    tags_parsed["contacts"] = sorted(contacts)
    tags_parsed["formats"] = sorted(formats)
    tags_parsed["inspire"] = sorted(inspire)
    tags_parsed["keywords"] = sorted(keywords)
    tags_parsed["licenses"] = sorted(licenses)
    tags_parsed["owners"] = sorted(owners)
    tags_parsed["srs"] = sorted(srs)
    tags_parsed["types"] = sorted(md_types)
    tags_parsed["unused"] = sorted(unused)

    # method ending
    return tags_parsed

# ############################################################################
# ######### Main program ###########
# ##################################

# check file presence
if not path.isfile("out_api_search_empty.json"):
    print("Input file not found."
          "You should first execute store_api_responses.py")
    sys.exit()
else:
    pass

# open and read JSON
with open("out_api_search_empty.json") as data_file:
    data = json.load(data_file)

# check data type
if not type(data) == dict:
    print("Bad file type.")
    print(type(data))
    sys.exit()
else:
    pass

# TAGS
tags = data.get("tags")
filters = search_tags_as_filters(tags)

print(filters.keys())
print("\n".join(filters.get("types")))
