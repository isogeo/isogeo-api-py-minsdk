# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_coordinate_systems
    # for specific
    python -m unittest tests.test_coordinate_systems.TestCoordinateSystems.test_coordinate_systems_listing
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
from sys import _getframe, exit
from time import gmtime, sleep, strftime

import urllib3

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import CoordinateSystem, Metadata, Workgroup, IsogeoSession
from isogeo_pysdk import __version__ as pysdk_version

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
    return "TEST_PySDK - CoordinateSystems - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestCoordinateSystems(unittest.TestCase):
    """Test CoordinateSystem model of Isogeo API."""

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
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created metadata
        cls.isogeo.metadata.delete(cls.metadata_fixture_created._id)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_coordinate_systems_association_metadata(self):
        """POST :resources/{metadata_uuid}/coordinate-systems/"""
        # get a SRS among the associated in the workgroup
        coordinate_systems = self.isogeo.coordinate_system.listing(
            self.isogeo.metadata.get(self.metadata_fixture_created._id)._creator.get(
                "_id"
            )
        )

        # pick randomly one and load it into a model
        random_srs = CoordinateSystem(**sample(coordinate_systems, 1)[0])

        # associate it
        srs_associated = self.isogeo.srs.associate_metadata(
            metadata=self.metadata_fixture_created, coordinate_system=random_srs
        )

        # check type
        self.assertIsInstance(srs_associated, CoordinateSystem)

        # refresh fixture metadata
        self.metadata_updated = self.isogeo.metadata.get(
            metadata_id=self.metadata_fixture_created._id, include=["coordinate-system"]
        )

        # -- dissociate
        self.isogeo.srs.dissociate_metadata(metadata=self.metadata_fixture_created)

    # -- GET --
    def test_coordinate_systems_listing_global(self):
        """GET :/coordinate-systems/}"""
        # retrieve metadata coordinate_systems
        coordinate_systems = self.isogeo.coordinate_system.listing()
        # check result
        self.assertIsInstance(coordinate_systems, list)
        # parse and test object loader
        for i in coordinate_systems:
            # load it
            coordinate_system = CoordinateSystem(**i)
            # tests attributes structure
            self.assertTrue(hasattr(coordinate_system, "_tag"))
            self.assertTrue(hasattr(coordinate_system, "code"))
            self.assertTrue(hasattr(coordinate_system, "name"))
            # tests attributes value
            self.assertEqual(coordinate_system._tag, i.get("_tag"))
            self.assertEqual(coordinate_system.code, i.get("code"))
            self.assertEqual(coordinate_system.name, i.get("name"))

    def test_coordinate_systems_listing_workgroup(self):
        """GET :/groups/{workgroup_id}/coordinate-systems/}"""
        # retrieve metadata coordinate_systems
        coordinate_systems = self.isogeo.coordinate_system.listing(
            WORKGROUP_TEST_FIXTURE_UUID
        )
        # check result
        self.assertIsInstance(coordinate_systems, list)
        # parse and test object loader
        for i in coordinate_systems:
            # load it
            coordinate_system = CoordinateSystem(**i)
            # tests attributes structure
            self.assertTrue(hasattr(coordinate_system, "_tag"))
            self.assertTrue(hasattr(coordinate_system, "alias"))
            self.assertTrue(hasattr(coordinate_system, "code"))
            self.assertTrue(hasattr(coordinate_system, "name"))
            # tests attributes value
            self.assertEqual(coordinate_system._tag, i.get("_tag"))
            self.assertEqual(coordinate_system.alias, i.get("alias"))
            self.assertEqual(coordinate_system.code, i.get("code"))
            self.assertEqual(coordinate_system.name, i.get("name"))

    def test_coordinate_systems_detailed_global(self):
        """GET :/coordinate-systems/{epsg_code}"""
        # pick a random srs
        if len(self.isogeo._coordinate_systems):
            coordinate_systems = self.isogeo._coordinate_systems
        else:
            coordinate_systems = self.isogeo.coordinate_system.listing()

        srs_code = sample(coordinate_systems, 1)[0].get("code")
        # retrieve coordinate system with his EPSG code
        srs_detailed = self.isogeo.srs.coordinate_system(srs_code)
        # check result
        self.assertIsInstance(srs_detailed, CoordinateSystem)

    def test_coordinate_systems_detailed_workgroup(self):
        """GET :/groups/{workgroup_id}/coordinate-systems/{epsg_code}"""
        # pick a random srs
        if len(self.isogeo._wg_coordinate_systems):
            wg_coordinate_systems = self.isogeo._wg_coordinate_systems
        else:
            wg_coordinate_systems = self.isogeo.coordinate_system.listing(
                WORKGROUP_TEST_FIXTURE_UUID
            )

        srs_code = sample(wg_coordinate_systems, 1)[0].get("code")
        # retrieve coordinate system with his EPSG code
        srs_detailed = self.isogeo.srs.coordinate_system(srs_code)
        # check result
        self.assertIsInstance(srs_detailed, CoordinateSystem)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
