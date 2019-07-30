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
    return "TEST_PySDK - ServiceOperations - {}".format(_getframe(1).f_code.co_name)


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
        cls.isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )

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
    # -- POST --
    # def test_operations_create_basic(self):
    #     """POST :resources/{metadata_uuid}/operations/}"""
    #     # var
    #     operation_name = strftime("%Y-%m-%d", gmtime())
    #     operation_title = [
    #         {
    #             "lang": "fr",
    #             "value": "{} - {}".format(get_test_marker(), self.discriminator),
    #         }
    #     ]

    #     # create object locally
    #     operation_new = ServiceOperation(name=operation_name, titles=operation_title)

    #     # create it online
    #     operation_new = self.isogeo.metadata.operations.create(
    #         metadata=self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID),
    #         operation=operation_new,
    #     )

    #     # add created operation to deletion
    #     self.li_fixtures_to_delete.append(operation_new)

    # def test_operations_association(self):
    #     """POST :resources/{service_uuid}/operations/{operation_uuid}/dataset/{dataset_uuid}"""
    #     # var
    #     metadata_service = self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID)
    #     metadata_dataset = self.isogeo.metadata.get(
    #         "6b5cc93626634d0e9b0d2c48eff96bc3"
    #     )
    #     operation_name = "{} - {}".format(get_test_marker(), self.discriminator)
    #     operation_title = [
    #         {
    #             "lang": "fr",
    #             "value": "{} - {}".format(get_test_marker(), self.discriminator),
    #         }
    #     ]

    #     # create object locally
    #     operation_new = ServiceOperation(name=operation_name, titles=operation_title)

    #     # create it online
    #     operation_created = self.isogeo.metadata.operations.create(
    #         metadata=metadata_service, operation=operation_new
    #     )
    #     # associate it
    #     self.isogeo.metadata.operations.associate_metadata(
    #         service=metadata_service,
    #         operation=operation_created,
    #         dataset=metadata_dataset,
    #     )

    #     # check association result
    #     service_updated = self.isogeo.metadata.get(
    #         metadata_id=metadata_service._id, include=["operations"]
    #     )

    #     li_operations_datasets = list(
    #         filter(
    #             lambda d: d.get("_id") == operation_created._id,
    #             service_updated.operations,
    #         )
    #     )
    #     self.assertIsInstance(li_operations_datasets[0].get("dataset"), dict)

    #     # -- dissociate
    #     self.isogeo.metadata.operations.dissociate_metadata(
    #         service=metadata_service,
    #         operation=operation_created,
    #         dataset=metadata_dataset,
    #     )

    #     # add created operation to deletion
    #     self.li_fixtures_to_delete.append(operation_created)

    # -- GET --
    def test_operations_listing(self):
        """GET :resources/{metadata_uuid}/operations/}"""
        # retrieve metadata operations
        md_operations = self.isogeo.metadata.operations.listing(
            self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID)
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
            self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID)
        )
        # pick one
        operation_id = sample(md_operations, 1)[0].get("_id")
        # get it with a direct request
        operation = self.isogeo.metadata.operations.operation(
            metadata_id=METADATA_TEST_FIXTURE_UUID, operation_id=operation_id
        )

        # checks
        self.assertIsInstance(operation, ServiceOperation)

    # -- PUT/PATCH --
    # def test_operations_update(self):
    #     """PUT :resources/{metadata_uuid}/operations/{operation_uuid}"""
    #     # var
    #     operation_name = self.discriminator
    #     operation_title = [
    #         {
    #             "lang": "fr",
    #             "value": "{} - {}".format(get_test_marker(), self.discriminator),
    #         }
    #     ]

    #     # create object locally
    #     operation_new = ServiceOperation(name=operation_name, titles=operation_title)

    #     # create it online
    #     operation_created = self.isogeo.metadata.operations.create(
    #         metadata=self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID),
    #         operation=operation_new,
    #     )

    #     # modify local object
    #     operation_created.name = "{} - UPDATED".format(operation_name)

    #     # update the online operation
    #     operation_updated = self.isogeo.metadata.operations.update(operation_created)
    #     self.assertEqual(operation_updated.name, "{} - UPDATED".format(operation_name))

    #     # check if the change is effective
    #     operation_to_check = self.isogeo.metadata.operations.operation(
    #         metadata_id=METADATA_TEST_FIXTURE_UUID, operation_id=operation_created._id
    #     )
    #     self.assertEqual(operation_to_check.name, "{} - UPDATED".format(operation_name))

    #     # add created operation to deletion
    #     self.li_fixtures_to_delete.append(operation_to_check)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
