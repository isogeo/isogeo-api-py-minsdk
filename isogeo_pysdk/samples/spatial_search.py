# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

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
import configparser  # to manage options.ini
import json
from os import path
from six.moves.urllib.parse import quote

# Isogeo
from isogeo_pysdk import Isogeo


# ############################################################################
# ######### Main program ###########
# ##################################

if __name__ == "__main__":
    """Standalone execution"""
    # specific imports
    import geojson
    from geomet import wkt

    # storing application parameters into an ini file
    settings_file = r"../isogeo_params.ini"

    # testing ini file
    if not path.isfile(path.realpath(settings_file)):
        print(
            "ERROR: to execute this script as standalone,"
            " you need to store your Isogeo application settings in a "
            "isogeo_params.ini file. You can use the template to set your own."
        )
        import sys

        sys.exit()
    else:
        pass

    # reading ini file
    config = configparser.SafeConfigParser()
    config.read(settings_file)

    share_id = config.get("auth", "app_id")
    share_token = config.get("auth", "app_secret")

    # ------------ Real start ----------------
    # instanciating the class
    isogeo = Isogeo(client_id=share_id, client_secret=share_token)

    token = isogeo.connect()

    # ------------ REAL START ----------------------------

    geo_relation = "within"

    # opening a geojson file
    gson_input = r"samples_boundingbox.geojson"
    with open(gson_input) as data_file:
        # data = json.load(data_file)
        data = data_file.read()
        data = geojson.loads(data)

    validation = geojson.is_valid(data)
    print(validation)

    # search & compare
    basic_search = isogeo.search(token, page_size=0, whole_share=0)

    print("Comparing count of results returned: ")
    print("\t- without any filter = ", basic_search.get("total"))

    for feature in data.get("features"):
        # just for VIPolygons
        if feature.get("geometry").get("type") != "Polygon":
            print("Geometry type must be a polygon")
            continue
        else:
            pass
        # get bounding box and convex hull
        bbox = ",".join(str(round(c, 3)) for c in feature.get("bbox"))
        poly = wkt.dumps(feature.get("geometry"), decimals=3)

        # print(quote(poly))

        # search & display results - with bounding box
        filtered_search_bbox = isogeo.search(
            token, page_size=0, whole_share=0, bbox=bbox, georel=geo_relation
        )
        print(
            str("\t- {} (BOX) = {}\t{}").format(
                feature.get("properties").get("name").encode("utf8"),
                filtered_search_bbox.get("total"),
                bbox,
            )
        )
        # search & display results - with convex hull
        filtered_search_geo = isogeo.search(
            token, page_size=0, whole_share=0, poly=poly, georel=geo_relation
        )
        print(
            str("\t- {} (GEO) = {}\t{}").format(
                feature.get("properties").get("name").encode("utf8"),
                filtered_search_geo.get("total"),
                poly,
            )
        )
