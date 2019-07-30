# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_thesauri
    # for specific
    python -m unittest tests.test_thesauri.TestThesauri.test_thesauri
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from random import sample
from pathlib import Path
from socket import gethostname
from sys import exit, _getframe
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Thesaurus


# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
app_script_id = environ.get("ISOGEO_API_USER_CLIENT_ID")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
platform = environ.get("ISOGEO_PLATFORM", "qa")
user_email = environ.get("ISOGEO_USER_NAME")
user_password = environ.get("ISOGEO_USER_PASSWORD")
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_PySDK - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestThesauri(unittest.TestCase):
    """Test Thesaurus model of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not app_script_id or not app_script_secret:
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        # API connection
        cls.isogeo = IsogeoSession(
            client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )
        # getting a token
        cls.isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )

    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(
            hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
        )

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- GET --
    def test_thesauri(self):
        """GET :thesauri}"""
        # retrieve  thesauri
        thesauri = self.isogeo.thesaurus.thesauri()
        self.assertIsInstance(thesauri, list)
        # parse and test object loader
        for i in thesauri:
            thesaurus = Thesaurus(**i)
            # tests attributes structure
            self.assertTrue(hasattr(thesaurus, "_abilities"))
            self.assertTrue(hasattr(thesaurus, "_id"))
            self.assertTrue(hasattr(thesaurus, "code"))
            self.assertTrue(hasattr(thesaurus, "name"))
            # tests attributes value
            self.assertEqual(thesaurus._id, i.get("_id"))
            self.assertEqual(thesaurus.code, i.get("code"))
            self.assertEqual(thesaurus.name, i.get("name"))

    def test_thesaurus_detailed(self):
        """GET :thesauri/{thesaurus_uuid}"""
        # retrieve workgroup thesauri
        if self.isogeo._thesauri_codes:
            thesauri = self.isogeo._thesauri_codes
        else:
            thesauri = self.isogeo.thesaurus.thesauri(caching=0)

        # pick two thesauri: one locked by Isogeo, one workgroup specific
        thesaurus_id = sample(thesauri, 1)[0]

        # get and check
        thesaurus = self.isogeo.thesaurus.thesaurus(thesaurus_id.get("_id"))

        self.assertIsInstance(thesaurus, Thesaurus)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
