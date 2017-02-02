# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Geographic search
# Purpose:      Filter results within an Isogeo share with spatial criteria, using
#               the Isogeo API Python minimalist SDK.
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      14/04/2016
# Updated:      18/05/2016
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import configparser     # to manage options.ini
import json
from os import path

# Isogeo
from isogeo_pysdk import Isogeo

# 3rd party
import geojson

# ############################################################################
# ######### Main program ###########
# ##################################

# storing application parameters into an ini file
settings_file = r"../isogeo_params.ini"

# testing ini file
if not path.isfile(path.realpath(settings_file)):
    print("ERROR: to execute this script as standalone, you need to store your Isogeo application settings in a isogeo_params.ini file. You can use the template to set your own.")
    import sys
    sys.exit()
else:
    pass

# reading ini file
config = configparser.SafeConfigParser()
config.read(settings_file)

share_id = config.get('auth', 'app_id')
share_token = config.get('auth', 'app_secret')

# ------------ Real start ----------------
# instanciating the class
isogeo = Isogeo(client_id=share_id,
                client_secret=share_token)

token = isogeo.connect()

# ------------ REAL START ----------------------------

# opening a geojson file
gson_input = r'samples_boundingbox.geojson'
with open(gson_input) as data_file:
    data = json.load(data_file)

# search & compare
basic_search = isogeo.search(token,
                             page_size=0,
                             whole_share=0)

print("Comparing count of results returned: ")
print("\t- without any filter = ", basic_search.get('total'))

for feature in data['features']:
    # just for VIPolygons
    if feature['geometry']['type'] != "Polygon":
        print("Geometry type must be a polygon")
        continue
    else:
        pass
    # search & display results
    bbox = str(feature['bbox'])[1:-1]
    filtered_search = isogeo.search(token,
                                    page_size=0,
                                    whole_share=0,
                                    bbox=bbox)
    print(str("\t- {} = {}\t({})")
          .format(feature['properties']['name'].encode("utf8"),
                  filtered_search.get('total'),
                  bbox
                  ),
          )
