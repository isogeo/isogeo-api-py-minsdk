# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_conditions
    # for licific
    python -m unittest tests.test_conditions.TestConditions.test_conditions_create_basic
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import unittest
import urllib3
from os import environ
from pathlib import Path
from random import sample
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import Isogeo, Condition, License, Metadata


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
    return "TEST_PySDK - Conditions - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestConditions(unittest.TestCase):
    """Test Condition model of Isogeo API."""

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

        # fixture metadata
        cls.fixture_metadata_existing = cls.isogeo.metadata.get(
            METADATA_TEST_FIXTURE_UUID, include=["conditions"]
        )

        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.fixture_metadata = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md, check_exists=0
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
        cls.isogeo.metadata.delete(cls.fixture_metadata._id)

        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_conditions_create(self):
        """POST :metadata/{metadata_uuid}/conditions}"""
        # retrieve workgroup licenses
        workgroup_licenses = self.isogeo.license.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID
        )

        # create object locally
        condition = Condition(
            description="bonjour", license=sample(workgroup_licenses, 1)[0]
        )

        # add it to a metadata
        condition_created = self.isogeo.metadata.conditions.create(
            metadata=self.fixture_metadata, condition=condition
        )

        # remove it from a metadata
        condition_removed = self.isogeo.metadata.conditions.delete(
            metadata=self.fixture_metadata, condition=condition_created
        )

        self.assertEqual(condition_removed.status_code, 204)

    # -- GET --
    def test_conditions_listing(self):
        """GET :metadata/{metadata_uuid}/conditions}"""
        # retrieve metadata conditions
        metadata_conditions = self.isogeo.metadata.conditions.listing(
            self.fixture_metadata_existing._id
        )
        self.assertIsInstance(metadata_conditions, list)
        # parse and test object loader
        for i in metadata_conditions:
            condition = Condition(**i)
            # tests attributes structure
            self.assertTrue(hasattr(condition, "_id"))
            self.assertTrue(hasattr(condition, "description"))
            self.assertTrue(hasattr(condition, "license"))
            # test attributes instances
            if "license" in i:
                self.assertIsInstance(condition.license, License)
            # tests attributes value
            self.assertEqual(condition._id, i.get("_id"))
            self.assertEqual(condition.description, i.get("description"))

    def test_conditions_get_detailed(self):
        """GET :metadata/{metadata_uuid}/conditions/{conditions_uuid}"""
        # retrieve workgroup licenses
        workgroup_licenses = self.isogeo.license.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID
        )
        # filter on licenses which have been already associated
        license_associated = sample(
            [lic for lic in workgroup_licenses if lic.get("count") > 0], 1
        )[0]
        # search metadata using this license as condition
        search_filtered_license = self.isogeo.search(
            query=license_associated.get("_tag"), include=("conditions",), page_size=5
        )
        # parse results
        for md in search_filtered_license.results:
            metadata = Metadata.clean_attributes(md)
            # parse conditions
            for cond in metadata.conditions:
                condition = Condition(**cond)

        # returns a detailed condition
        condition_detailed = self.isogeo.metadata.conditions.get(
            metadata_id=metadata._id, condition_id=condition._id
        )

        self.assertIsInstance(condition_detailed, Condition)
        # print(condition_detailed)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if get_test_marker() == "__main__":
    unittest.main()
