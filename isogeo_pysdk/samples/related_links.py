# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# -----------------------------------------------------------------------------
# Name:         Isogeo
# Purpose:      Sample using Python minimalist SDK of Isogeo API to get links
#               and related resources, including secondary links
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      01/09/2016
# Updated:      01/09/2016
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import ConfigParser     # to manage options.ini
from os import path

# Isogeo
from isogeo_pysdk import Isogeo

# #############################################################################
# ######## Main program ############
# ##################################

# storing application parameters into an ini file
settings_file = r"../isogeo_params.ini"

# testing ini file
if not path.isfile(path.realpath(settings_file)):
    print("ERROR: to execute this script as standalone,"
          " you need to store your Isogeo application "
          "settings in a isogeo_params.ini file. "
          "You can use the template to set your own.")
    import sys
    sys.exit()
else:
    pass

# reading ini file
config = ConfigParser.SafeConfigParser()
config.read(settings_file)

share_id = config.get('auth', 'app_id')
share_token = config.get('auth', 'app_secret')

# ------------ Real start ----------------
# instanciating the class
isogeo = Isogeo(client_id=share_id,
                client_secret=share_token)

# getting a token
jeton = isogeo.connect()

# let's search for metadatas!
search = isogeo.search(jeton,
                       page_size=10,
                       sub_resources=["links"])

# ------------ Parsing resources ----------------
kind_ogc = ('wfs', 'wms', 'wmts')
kind_esri = ('esriFeatureService', 'esriMapService', 'esriTileService')

li_ogc = []
li_esri = []
li_dl = []

for md in search.get('results'):
    rel_resources = md.get('links')
    if not rel_resources:
        continue
    else:
        pass
    for link in rel_resources:
        # only OGC
        if link.get('kind') in kind_ogc\
           or (link.get('type') == 'link' and link.get('link').get('kind') in kind_ogc):
            li_ogc.append((link.get('title'), link.get('url')))
            continue
        else:
            pass

        # only Esri
        if link.get('kind') in kind_esri\
           or (link.get('type') == 'link' and link.get('link').get('kind') in kind_esri):
            li_esri.append((link.get('title'), link.get('url')))
            continue
        else:
            pass

        # downloadable
        if link.get('kind') == 'data' and link.get('actions') == 'download'\
           or (link.get('type') == 'link' and link.get('link').get('kind') == 'data'):
            li_dl.append((link.get('title'), link.get('url')))
            continue
        else:
            pass

        # secondary
        if link.get('type') == 'link':
            # li_dl.append((link.get('title'), link.get('url')))
            # print(link.get('kind'))
            # print(link.get('link'), "\n")
            continue
        else:
            pass

        # others

print("\n\tOGC: ", li_ogc)
print("\n\tEsri: ", li_esri)
# print("\n\tDownload: ", li_dl)
