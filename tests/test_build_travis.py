# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# -----------------------------------------------------------------------------
# Name:         Isogeo
# Purpose:      Python minimalist SDK to use Isogeo API
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      22/12/2015
# Updated:      21/04/2017
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
from random import randrange

# Isogeo
from isogeo_pysdk import Isogeo
from isogeo_pysdk import IsogeoTranslator


# #############################################################################
# ######## Main program ############
# ##################################

# API access
share_id = environ.get('ISOGEO_API_DEV_ID')
share_token = environ.get('ISOGEO_API_DEV_SECRET')

# instanciating the class
isogeo = Isogeo(client_id=share_id,
                client_secret=share_token)

print("Available _include values: ", isogeo.SUBRESOURCES)

# API Version
print("Current Isogeo public API version: ",
      isogeo.get_isogeo_version(),
      isogeo.platform.upper())
# DB version
print("Current Isogeo public database version: ",
      isogeo.get_isogeo_version(component="db"),
      isogeo.platform.upper())
# APP version
print("Current Isogeo web application version: ",
      isogeo.get_isogeo_version(component="app"),
      isogeo.platform.upper())

# getting a token
token = isogeo.connect()

# -- BASIC SEARCH ------------------------------------------------------------
search = isogeo.search(token)
print("\nAPI response keys for a generic search: ", sorted(search.keys()))
print("Sent query parameters: ", search.get("query"))
print("Count of metadatas shared: ", search.get("total"))
print("Count of resources got by request: {}\n"
      .format(len(search.get("results"))))

assert(type(search.get("results")) == list)

# -- FULL SPECIFIC METADATA --------------------------------------------------
# get one random resource
hatnumber = randrange(0, len(search.get("results")))
my_resource = isogeo.resource(token,
                              search.get("results")[hatnumber].get("_id"),
                              sub_resources=isogeo.SUBRESOURCES,
                              prot="https"
                              )

print("\nAPI response keys for a specific metadata search: ",
      sorted(my_resource.keys()))

# -- ADVANCED SEARCHES -------------------------------------------------------
# get 10 last data modified
latest_data_modified = isogeo.search(token,
                                     page_size=10,
                                     order_by="modified",
                                     whole_share=0,
                                     sub_resources=["events"])

for md in latest_data_modified.get("results"):
    title = md.get('title')
    evt_description = md.get("events")[0].get("description")

# filter on IDs list
specific_ids = isogeo.search(token,
                             specific_md=md.get("_id"),
                             page_size=10,
                             sub_resources="all")

# print(specific_ids.get("results"))

# -- SHARES -----------------------------------------------------------
# shares information
shares = isogeo.shares(token)
share = shares[0]
search_share_segregated = isogeo.search(token, share=share.get("_id"))
print("Count of resources got by request: {}\n"
      .format(len(search_share_segregated.get("results"))))

# -- MISCELLANEOUS -----------------------------------------------------------
# use integrated translator
tr = IsogeoTranslator("FR")
if my_resource.get("contacts"):
    ct = my_resource.get("contacts")[0]
    print("\nRaw contact role: " + ct.get("role"))
    # English
    tr = IsogeoTranslator("EN")
    print("English contact role: " + tr.tr("roles", ct.get("role")))
    # French
    tr = IsogeoTranslator("FR")
    print("Rôle du contact en français: " + tr.tr("roles", ct.get("role")))
else:
    print("This resource doesn't have any contact. Try again!")
