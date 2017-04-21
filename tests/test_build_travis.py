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
# Updated:      10/01/2016
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
from random import randrange    # to get a random resource

# Isogeo
from isogeo_pysdk import Isogeo
from isogeo_pysdk import IsogeoTranslator

# #############################################################################
# ######## Main program ############
# ##################################


# API access
share_id = environ.get('ISOGEO_API_DEV_ID')
share_token = environ.get('ISOGEO_API_DEV_SECRET')

# ------------ Real start ----------------
# instanciating the class
isogeo = Isogeo(client_id=share_id,
                client_secret=share_token)

# check which sub resources are available
print(isogeo.SUBRESOURCES)

# getting a token
jeton = isogeo.connect()

# let's search for metadatas!
print(dir(isogeo))
search = isogeo.search(jeton)

print(sorted(search.keys()))
print(search.get('query'))
print("Total count of metadatas shared: ", search.get("total"))
print("Count of resources got by request: {}\n".format(len(search.get("results"))))

# get one random resource
hatnumber = randrange(0, len(search.get("results")))
my_resource = isogeo.resource(jeton,
                              search.get("results")[hatnumber].get("_id"),
                              sub_resources=isogeo.SUBRESOURCES,
                              prot="https"
                              )

print(sorted(my_resource.keys()))


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
