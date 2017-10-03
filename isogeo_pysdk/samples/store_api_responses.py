# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Batch export to XML ISO19139
# Purpose:      Exports each of 10 last updated metadata into an XML ISO19139
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      14/11/2016
# Updated:      21/04/2017
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

# ############################################################################
# ######### Main program ###########
# ##################################

# storing application parameters into an ini file
settings_file = r"../isogeo_params.ini"

# testing ini file
if not path.isfile(path.realpath(settings_file)):
    print("ERROR: to execute this script as standalone, you need to store "
          "your Isogeo application settings in a isogeo_params.ini file."
          " You can use the template to set your own.")
    import sys
    sys.exit()
else:
    pass

# reading ini file
config = configparser.SafeConfigParser()
config.read(settings_file)

share_id = config.get('auth', 'app_id')
share_token = config.get('auth', 'app_secret')

# instanciating the class
isogeo = Isogeo(client_id=share_id,
                client_secret=share_token,
                lang="fr")

token = isogeo.connect()

# ------------ REAL START ----------------------------------------------------

# empty search
request = isogeo.search(token, page_size=0, whole_share=0)
with open("out_api_search_empty.json", "w") as json_basic:
    json.dump(request,
              json_basic,
              sort_keys=True,
              indent=4,
              )

# basic search
request = isogeo.search(token, page_size=10, whole_share=0)
with open("out_api_search_basic.json", "w") as json_basic:
    json.dump(request,
              json_basic,
              sort_keys=True,
              indent=4,
              )

# complete search
request = isogeo.search(token, whole_share=1, page_size=10, sub_resources="all")
with open("out_api_search_complete.json", "w") as json_basic:
    json.dump(request,
              json_basic,
              sort_keys=True,
              indent=4,
              )

# shares informations
request = isogeo.shares(token)
with open("out_api_shares.json", "w") as json_basic:
    json.dump(request,
              json_basic,
              sort_keys=True,
              indent=4,
              )
