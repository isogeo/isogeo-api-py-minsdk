# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Get OpenCatalog if exists in shares
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
import configparser  # to manage options.ini
from os import path

# 3rd party library
import requests

# Isogeo
from isogeo_pysdk import Isogeo

# ############################################################################
# ######### Main program ###########
# ##################################

if __name__ == "__main__":
    """Standalone execution"""
    # storing application parameters into an ini file
    settings_file = r"../isogeo_params.ini"

    # testing ini file
    if not path.isfile(path.realpath(settings_file)):
        print(
            "ERROR: to execute this script as standalone, you need to store your Isogeo application settings in a isogeo_params.ini file. You can use the template to set your own."
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
    isogeo = Isogeo(client_id=share_id, client_secret=share_token, lang="fr")

    token = isogeo.connect()

    # ------------ REAL START ----------------------------
    shares = isogeo.shares(token)
    print("This application is supplied by {} shares: ".format(len(shares)))

    for share in shares:
        # Share caracteristics
        name = share.get("name").encode("utf8")
        creator_name = share.get("_creator").get("contact").get("name")
        creator_id = share.get("_creator").get("_tag")[6:]
        print("\nShare name: ", name, " owned by workgroup ", creator_name)

        # OpenCatalog URL construction
        share_details = isogeo.share(token, share_id=share.get("_id"))
        url_OC = "http://open.isogeo.com/s/{}/{}".format(
            share.get("_id"), share_details.get("urlToken")
        )

        # Testing URL
        request = requests.get(url_OC)
        if request.status_code == 200:
            print("OpenCatalog available at: ", url_OC)
        else:
            print(
                "OpenCatalog is not set for this share."
                "\nGo and add it: https://app.isogeo.com/groups/{}/admin/shares/{}".format(
                    creator_id, share.get("_id")
                )
            )
