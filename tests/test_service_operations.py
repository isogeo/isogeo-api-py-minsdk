# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_service_operations
    # for specific
    python -m unittest tests.test_service_operations.TestServiceOperations.test_operations_create
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from random import sample
from socket import gethostname
from sys import exit, _getframe
from time import gmtime, sleep, strftime
import unittest
import urllib3

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import (
    IsogeoSession,
    __version__ as pysdk_version,
    Metadata,
    ServiceOperation,
)


# #############################################################################
# ######## Globals #################
# ##################################

load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
app_script_id = environ.get("ISOGEO_API_USER_CLIENT_ID")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
platform = environ.get("ISOGEO_PLATFORM", "qa")
user_email = environ.get("ISOGEO_USER_NAME")
user_password = environ.get("ISOGEO_USER_PASSWORD")
METADATA_TEST_FIXTURE_UUID = "c6989e8b406845b5a86261bd5ef57b60"
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_UNIT_PythonSDK - ServiceOperations - {}".format(
        _getframe(1).f_code.co_name
    )


# #############################################################################
# ########## Classes ###############
# ##################################


class TestServiceOperations(unittest.TestCase):
    """Test ServiceOperation model of Isogeo API."""

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
        logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

        # class vars and attributes
        cls.li_fixtures_to_delete = []

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
        cls.isogeo.connect(username=user_email, password=user_password)

        # fixture metadata
        # md = Metadata(title=get_test_marker(), type="service")
        # cls.fixture_metadata = cls.isogeo.metadata.create(
        #     WORKGROUP_TEST_FIXTURE_UUID, metadata=md, check_exists=0
        # )

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
        # cls.isogeo.metadata.delete(cls.fixture_metadata._id)

        # clean created service_operations
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.operations.delete(operation=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- GET --
    def test_operations_listing(self):
        """GET :resources/{metadata_uuid}/operations/}"""
        # retrieve metadata operations
        md_operations = self.isogeo.metadata.operations.listing(
            self.isogeo.metadata.metadata(METADATA_TEST_FIXTURE_UUID)
        )
        # parse and test object loader
        for i in md_operations:
            # load it
            operation = ServiceOperation(**i)
            # tests attributes structure
            self.assertTrue(hasattr(operation, "_id"))
            self.assertTrue(hasattr(operation, "mimeTypesIn"))
            self.assertTrue(hasattr(operation, "mimeTypesOut"))
            self.assertTrue(hasattr(operation, "name"))
            self.assertTrue(hasattr(operation, "verb"))
            # tests attributes value
            self.assertEqual(operation._id, i.get("_id"))
            self.assertEqual(operation.mimeTypesIn, i.get("mimeTypesIn"))
            self.assertEqual(operation.mimeTypesOut, i.get("mimeTypesOut"))
            self.assertEqual(operation.name, i.get("name"))
            self.assertEqual(operation.verb, i.get("verb"))

    def test_operations_detailed(self):
        """GET :resources/{metadata_uuid}/operations/{operation_uuid}}"""
        # get operations
        md_operations = self.isogeo.metadata.operations.listing(
            self.isogeo.metadata.metadata(METADATA_TEST_FIXTURE_UUID)
        )
        # pick one
        operation_id = sample(md_operations, 1)[0].get("_id")
        # get it with a direct request
        operation = self.isogeo.metadata.operations.operation(
            metadata_id=METADATA_TEST_FIXTURE_UUID,
            operation_id=operation_id
        )

        # checks
        self.assertIsInstance(operation, ServiceOperation)



# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()