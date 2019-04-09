# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

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
import configparser  # to manage options.ini
from os import path

# Isogeo
from isogeo_pysdk import Isogeo

# ############################################################################
# ######### Main program ###########
# ##################################

if __name__ == "__main__":
    """Standalone execution"""
    # specific import
    from dateutil.parser import parse as dtparse

    # storing application parameters into an ini file
    settings_file = r"../isogeo_params.ini"

    # testing ini file
    if not path.isfile(path.realpath(settings_file)):
        print(
            "ERROR: to execute this script as standalone,"
            " you need to store your Isogeo application settings"
            " in a isogeo_params.ini file."
            " You can use the template to set your own."
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
    latest_data_modified = isogeo.search(
        token, page_size=10, order_by="modified", whole_share=0, include=["events"]
    )

    print("Last 10 data updated \nTitle | datetime\n\t description")
    for md in latest_data_modified.get("results"):
        title = md.get("title")
        evt_description = md.get("events")[0].get("description")
        print(
            str("___________________\n\n{} | {} \n\t {}").format(
                title.encode("utf8"),
                dtparse(md.get("modified")[:19]).strftime("%a %d %B %Y"),
                evt_description.encode("utf8"),
            )
        )
