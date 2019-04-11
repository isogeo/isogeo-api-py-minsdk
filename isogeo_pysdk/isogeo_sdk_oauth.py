# -*- coding: UTF-8 -*-
#! python3

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
import locale
import logging
from math import ceil
import re
from sys import platform as opersys

# 3rd party library
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

# modules
try:
    from . import checker
    from . import utils
except (ImportError, ValueError, SystemError):
    import checker
    import utils

# ##############################################################################
# ########## Globals ###############
# ##################################

checker = checker.IsogeoChecker()
utils = utils.IsogeoUtils()

# #############################################################################
# ########## Classes ###############
# ##################################


class IsogeoSession(OAuth2Session):
    def __init__(
        self,
        client_id=None,
        client=None,
        auto_refresh_url=None,
        auto_refresh_kwargs=None,
        scope=None,
        redirect_uri=None,
        token=None,
        state=None,
        token_updater=None,
        # custom
        client_secret=None,
        platform: str = "prod",
        lang: str = "en",
        # additional
        **kwargs,
    ):

        self.client_secret = client_secret

        return super().__init__(
            client_id=client_id,
            client=client,
            auto_refresh_url=auto_refresh_url,
            auto_refresh_kwargs=auto_refresh_kwargs,
            scope=scope,
            redirect_uri=redirect_uri,
            token=token,
            state=state,
            token_updater=token_updater,
            **kwargs,
        )

    def connect(self, username, password):

        return self.fetch_token(
            token_url=self.auto_refresh_url,
            username=username,
            password=password,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    # ------------ Specific imports ----------------
    from os import environ
    from dotenv import load_dotenv

    # ------------ Log & debug ----------------
    logger = logging.getLogger()
    logging.captureWarnings(True)
    logger.setLevel(logging.INFO)

    # ------------ Real start ----------------
    # load application credentials from downloaded file
    credentials = utils.credentials_loader("client_secrets_scripts.json")

    # get user ID as environment variables
    load_dotenv("dev.env", verbose=1)

    # instanciate
    isogeo = IsogeoSession(
        client=LegacyApplicationClient(client_id=credentials.get("client_id")),
        auto_refresh_url="https://id.api.isogeo.com/oauth/token",
        client_secret=credentials.get("client_secret"),
    )

    # getting a token
    token = isogeo.connect(username=environ.get("ISOGEO_USER_NAME"),
                           password=environ.get("ISOGEO_USER_PASSWORD"))
    print(token)