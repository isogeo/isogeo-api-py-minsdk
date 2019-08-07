# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_feature_attributes
    # for specific
    python -m unittest tests.test_feature_attributes.TestFeatureAttributes.test_featureAttributes_create_basic
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import urllib3
import unittest
from os import environ
from pathlib import Path
from random import sample
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import (
    IsogeoSession,
    __version__ as pysdk_version,
    FeatureAttribute,
    Metadata,
)


# #############################################################################
# ######## Globals #################
# ##################################


if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
METADATA_TEST_FIXTURE_UUID = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE")
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_PySDK - FeatureAttributes {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestFeatureAttributes(unittest.TestCase):
    """Test FeatureAttribute model of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_USER_CLIENT_ID") or not environ.get(
            "ISOGEO_API_USER_CLIENT_SECRET"
        ):
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

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

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.metadata_fixture_created = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md, check_exists=0
        )
        cls.metadata_fixture_existing = cls.isogeo.metadata.get(
            metadata_id=METADATA_TEST_FIXTURE_UUID
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

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created metadata
        cls.isogeo.metadata.delete(cls.metadata_fixture_created._id)
        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.featureAttributes.delete(featureAttribute=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- GET --
    def test_featureAttributes_listing(self):
        """GET :resources/{metadata_uuid}/featureAttributes/}"""
        # retrieve workgroup featureAttributes
        md_featureAttributes = self.isogeo.metadata.attributes.listing(
            self.metadata_fixture_existing
        )
        # parse and test object loader
        for i in md_featureAttributes:
            # load it
            attribute = FeatureAttribute(**i)
            # tests attributes structure
            self.assertTrue(hasattr(attribute, "_id"))
            self.assertTrue(hasattr(attribute, "alias"))
            self.assertTrue(hasattr(attribute, "dataType"))
            self.assertTrue(hasattr(attribute, "description"))
            self.assertTrue(hasattr(attribute, "language"))
            self.assertTrue(hasattr(attribute, "name"))
            self.assertTrue(hasattr(attribute, "parent_resource"))
            # tests attributes value
            self.assertEqual(attribute._id, i.get("_id"))
            self.assertEqual(attribute.alias, i.get("alias"))
            self.assertEqual(attribute.dataType, i.get("dataType"))
            self.assertEqual(attribute.description, i.get("description"))
            self.assertEqual(attribute.name, i.get("name"))
            self.assertEqual(attribute.parent_resource, i.get("parent_resource"))


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
