# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_conformity
# for licific
python -m unittest tests.test_conformity.TestConformity.test_conformity_listing
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
from isogeo_pysdk import Isogeo, Conformity, Specification, Metadata


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
    """Returns the function name."""
    return "TEST_PySDK - Conformitys - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestConformity(unittest.TestCase):
    """Test Conformity model of Isogeo API."""

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
            METADATA_TEST_FIXTURE_UUID, include=("specifications",)
        )

        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.fixture_metadata = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md
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
    def test_conformity_create(self):
        """POST :metadata/{metadata_uuid}/conformity}"""
        # retrieve workgroup specifications
        workgroup_specifications = self.isogeo.specification.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID
        )

        # create object locally
        conformity = Conformity(
            conformant=1, specification=sample(workgroup_specifications, 1)[0]
        )

        # add it to a metadata
        conformity_created = self.isogeo.metadata.conformity.create(
            metadata=self.fixture_metadata, conformity=conformity
        )

        self.assertIsInstance(conformity_created, Conformity)

        # remove it from a metadata
        conformity_removed = self.isogeo.metadata.conformity.delete(
            metadata=self.fixture_metadata, conformity=conformity_created
        )

        self.assertEqual(conformity_removed.status_code, 204)

    # -- GET --
    def test_conformity_listing(self):
        """GET :metadata/{metadata_uuid}/conformity}"""
        # retrieve metadata conformity
        metadata_conformity = self.isogeo.metadata.conformity.listing(
            self.fixture_metadata_existing._id
        )
        self.assertIsInstance(metadata_conformity, list)
        # parse and test object loader
        for i in metadata_conformity:
            conformity = Conformity(**i)
            # tests attributes structure
            self.assertTrue(hasattr(conformity, "conformant"))
            self.assertTrue(hasattr(conformity, "specification"))
            # test attributes instances
            self.assertIsInstance(conformity.specification, Specification)
            # tests attributes value
            self.assertEqual(conformity.conformant, i.get("conformant"))


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if get_test_marker() == "__main__":
    unittest.main()
