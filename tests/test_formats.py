# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_formats
# for specific
python -m unittest tests.test_formats.TestFormats.test_formats_listing
```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import unittest
from os import environ
from pathlib import Path
from random import sample
from socket import gethostname
from string import ascii_lowercase
from sys import _getframe, exit
from time import gmtime, sleep, strftime

import urllib3

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import Format, Isogeo


# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
METADATA_TEST_FIXTURE_UUID = "c6989e8b406845b5a86261bd5ef57b60"
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name."""
    return "TEST_UNIT_PySDK_Formats_{}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestFormats(unittest.TestCase):
    """Test Format model of Isogeo API."""

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

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

        # API connection
        cls.isogeo = Isogeo(
            auth_mode="user_legacy",
            client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
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
        sleep(0.5)
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.formats.delete(frmt=i)
                pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_formats_create_basic(self):
        """POST :/formats/}"""
        # get a random string
        frmt_code = "".join(sample(ascii_lowercase, 10))
        frmt_name = "Format created by an unit"
        # create local object
        format_new = Format(code=frmt_code, name=frmt_name, type="vectorDataset")

        # create it online
        format_new = self.isogeo.formats.create(frmt=format_new)

        # checks
        self.assertEqual(format_new.name, frmt_name)

        # add created format to deletion
        self.li_fixtures_to_delete.append(format_new)

    # -- GET --
    def test_formats_listing(self):
        """GET :/formats/}"""
        # retrieve metadata formats
        formats = self.isogeo.formats.listing()
        # parse and test object loader
        for i in formats:
            # load it
            frmt = Format(**i)
            # tests attributes structure
            self.assertTrue(hasattr(frmt, "_id"))
            self.assertTrue(hasattr(frmt, "_tag"))
            self.assertTrue(hasattr(frmt, "aliases"))
            self.assertTrue(hasattr(frmt, "code"))
            self.assertTrue(hasattr(frmt, "name"))
            self.assertTrue(hasattr(frmt, "type"))
            self.assertTrue(hasattr(frmt, "versions"))
            # tests attributes value
            self.assertEqual(frmt._id, i.get("_id"))
            self.assertEqual(frmt._tag, i.get("_tag"))
            self.assertEqual(frmt.aliases, i.get("aliases"))
            self.assertEqual(frmt.code, i.get("code"))
            self.assertEqual(frmt.name, i.get("name"))
            self.assertEqual(frmt.type, i.get("type"))
            self.assertEqual(frmt.versions, i.get("versions"))

    def test_formats_detailed(self):
        """GET :/formats/{code}"""
        # pick a random srs
        if len(self.isogeo._formats_geo):
            formats = self.isogeo._formats_geo
        else:
            formats = self.isogeo.formats.listing()

        frmt_code = sample(formats, 1)[0].get("code")
        # retrieve coordinate system with his EPSG code
        frmt_detailed = self.isogeo.formats.get(frmt_code)
        # check result
        self.assertIsInstance(frmt_detailed, Format)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
