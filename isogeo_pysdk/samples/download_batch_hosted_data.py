# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Batch export to XML ISO19139
# Purpose:      Exports hosted data of 10 last updated metadata into an XML ISO19139
# Author:       Julien Moura (@geojulien)
#
# Python:       3.6.x
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import configparser  # to manage options.ini
from os import path
import re

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
            "ERROR: to execute this script as standalone, you need to store "
            "your Isogeo application settings in a isogeo_params.ini file. "
            "You can use the template to set your own."
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

    # instanciating the class
    isogeo = Isogeo(client_id=share_id, client_secret=share_token, lang="fr")

    token = isogeo.connect()

    # ------------ REAL START ------------------------------------------------
    latest_data_modified = isogeo.search(
        token,
        page_size=10,
        order_by="modified",
        whole_share=0,
        query="action:download",
        include=["links"],
    )

    # parse and download
    for md in latest_data_modified.get("results"):
        for link in filter(lambda x: x.get("type") == "hosted", md.get("links")):
            dl_stream = isogeo.dl_hosted(token, resource_link=link)
            with open(dl_stream[1], "wb") as fd:
                for block in dl_stream[0].iter_content(1024):
                    fd.write(block)
