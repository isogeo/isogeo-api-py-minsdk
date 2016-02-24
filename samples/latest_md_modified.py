# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Latest modified datasets
# Purpose:      Get the latest modified datasets from an Isogeo share, using
#               the Isogeo API Python minimalist SDK.
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      14/02/2016
# Updated:      18/02/2016
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from ConfigParser import SafeConfigParser   # to manage .ini files
from os import path

# 3rd party library
from dateutil.parser import parse as dtparse

# Custom modules
from ..isogeo_sdk import Isogeo

# ############################################################################
# ######### Main program ###########
# ##################################

# ------------ Settings from ini file ----------------
if not path.isfile(path.realpath(r"..\isogeo_params.ini")):
    print("ERROR: to execute this script as standalone, you need to store your\n\
          Isogeo application settings in a isogeo_params.ini file.\n\
          You can use the template to set your own.")
    import sys
    sys.exit()
else:
    pass

config = SafeConfigParser()
config.read(r"..\isogeo_params.ini")

settings = {s: dict(config.items(s)) for s in config.sections()}

app_id = settings.get('auth').get('app_id')
app_secret = settings.get('auth').get('app_secret')
client_lang = settings.get('basics').get('def_codelang')

# ------------ Connecting to Isogeo API ----------------
# instanciating the class
isogeo = Isogeo(client_id=app_id,
                client_secret=app_secret,
                lang="fr")

token = isogeo.connect()

# ------------ REAL START ----------------------------
latest_data_modified = isogeo.search(token,
                                     page_size=10,
                                     order_by="modified",
                                     whole_share=0,
                                     sub_resources=["events"]
                                     )

for md in latest_data_modified:
    print("\n\t" + md.get('title'))
    print("Last data update: " +
          dtparse(md.get("modified")).strftime("%a %d %B %Y"))
