# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

    :Example:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_token
        # for specific
        python -m unittest tests.test_token.TestToken

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import unittest
import urllib3
from datetime import datetime
from os import environ
from pathlib import Path
from socket import gethostname
from sys import exit

# 3rd party
from dotenv import load_dotenv

# Isogeo
from isogeo_pysdk import Isogeo, IsogeoChecker

# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

checker = IsogeoChecker()

# #############################################################################
# ######## Classes #################
# ##################################


class TestToken(unittest.TestCase):
    """Test token management process."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID") or not environ.get(
            "ISOGEO_API_USER_LEGACY_CLIENT_SECRET"
        ):
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

        # API credentials settings
        cls.client_id = environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID")
        cls.client_secret = environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET")

    # standard methods
    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # close sessions
        pass

    # -- TESTS ---------------------------------------------------------
    def test_token_structure_legacy(self):
        """Test token structure"""
        isogeo = Isogeo(
            auth_mode="user_legacy",
            client_id=self.client_id,
            client_secret=self.client_secret,
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform="qa",
        )
        isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )

        # check token dict
        self.assertIsInstance(isogeo.token, dict)
        self.assertEqual(len(isogeo.token), 5)
        self.assertIn("access_token", isogeo.token)
        self.assertIn("token_type", isogeo.token)
        self.assertIn("expires_in", isogeo.token)
        self.assertIn("refresh_token", isogeo.token)
        self.assertIn("expires_at", isogeo.token)

        # check expires_at
        print(datetime.utcfromtimestamp(isogeo.token.get("expires_at")))
        print(datetime.utcnow())

        daetime.uctnow()
        # close
        isogeo.close()


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    unittest.main()
