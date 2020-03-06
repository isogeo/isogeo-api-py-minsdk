# -*- coding: UTF-8 -*-
#! python3  # noqa E265


"""
    Name:         Isogeo sample - Edit formats list in the API
    Purpose:      Used to update formats list, for example to add a new version
    Author:       Julien Moura (@geojulien)

    Made on December 2019 to comply with the CD 14 request
"""


# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from timeit import default_timer

# 3rd party
from dotenv import load_dotenv

# Isogeo
from isogeo_pysdk import Isogeo

# #############################################################################
# ######## Globals #################
# ##################################

# environment vars
load_dotenv("prod.env", override=True)

# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    # chronometer
    START_TIME = default_timer()

    # handle warnings
    if environ.get("ISOGEO_PLATFORM").lower() == "qa":
        import urllib3

        urllib3.disable_warnings()

    # -- Authentication and connection ---------------------------------
    # Isogeo client
    isogeo = Isogeo(
        auth_mode="user_legacy",
        client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
        client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
        auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
        platform=environ.get("ISOGEO_PLATFORM", "qa"),
    )

    # getting a token
    isogeo.connect(
        username=environ.get("ISOGEO_USER_NAME"),
        password=environ.get("ISOGEO_USER_PASSWORD"),
    )

    # get a format
    fmt_postgis = isogeo.formats.get("postgis")
    fmt_postgis.versions.extend(["3.1", "3.0", "2.5", "2.4", "2.3"])
    fmt_postgis_updted = isogeo.formats.update(fmt_postgis)

    # properly closing connection
    isogeo.close()
