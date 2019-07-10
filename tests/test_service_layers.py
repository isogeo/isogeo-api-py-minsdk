# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_service_layers
    # for specific
    python -m unittest tests.test_service_layers.TestServiceLayers.test_service_layers_create
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
    ServiceLayer,
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
    return "TEST_UNIT_PythonSDK - ServiceLayers - {}".format(
        _getframe(1).f_code.co_name
    )


# #############################################################################
# ########## Classes ###############
# ##################################


class TestServiceLayers(unittest.TestCase):
    """Test ServiceLayer model of Isogeo API."""

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

        # clean created service_layers
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.layers.delete(layer=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_layers_create_basic(self):
        """POST :groups/{metadata_uuid}/layers/}"""
        # var
        layer_name = strftime("%Y-%m-%d", gmtime())
        layer_title = [
            {
                "lang": "fr",
                "value": "{} - {}".format(get_test_marker(), self.discriminator),
            }
        ]

        # create object locally
        layer_new = ServiceLayer(name=layer_name, titles=layer_title)

        # create it online
        layer_new = self.isogeo.metadata.layers.create(
            metadata=self.isogeo.metadata.metadata(METADATA_TEST_FIXTURE_UUID),
            layer=layer_new,
        )

        # add created layer to deletion
        self.li_fixtures_to_delete.append(layer_new)

    # -- GET --
    def test_layers_listing(self):
        """GET :resources/{metadata_uuid}/layers/}"""
        # retrieve metadata layers
        md_layers = self.isogeo.metadata.layers.listing(
            self.isogeo.metadata.metadata(METADATA_TEST_FIXTURE_UUID)
        )
        # parse and test object loader
        for i in md_layers:
            # load it
            layer = ServiceLayer(**i)
            # tests attributes structure
            self.assertTrue(hasattr(layer, "_id"))
            self.assertTrue(hasattr(layer, "mimeTypes"))
            self.assertTrue(hasattr(layer, "name"))
            self.assertTrue(hasattr(layer, "titles"))
            # tests attributes value
            self.assertEqual(layer._id, i.get("_id"))
            self.assertEqual(layer.mimeTypes, i.get("mimeTypes"))
            self.assertEqual(layer.name, i.get("id"))
            self.assertEqual(layer.titles, i.get("titles"))

    def test_layers_detailed(self):
        """GET :resources/{metadata_uuid}/layers/{layer_uuid}}"""
        self.isogeo.metadata.layers.layer(
            metadata_id=METADATA_TEST_FIXTURE_UUID,
            layer_id="77659ebc532a4ed3a1ef326af18348f0",
        )

    # -- PUT/PATCH --
    def test_layers_update(self):
        """PUT :groups/{workgroup_uuid}/layers/{layer_uuid}"""
        # var
        layer_name = self.discriminator
        layer_title = [
            {
                "lang": "fr",
                "value": "{} - {}".format(get_test_marker(), self.discriminator),
            }
        ]

        # create object locally
        layer_new = ServiceLayer(name=layer_name, titles=layer_title)

        # create it online
        layer_created = self.isogeo.metadata.layers.create(
            metadata=self.isogeo.metadata.metadata(METADATA_TEST_FIXTURE_UUID),
            layer=layer_new,
        )

        # modify local object
        layer_created.name = "{} - UPDATED".format(layer_name)

        # update the online layer
        layer_updated = self.isogeo.metadata.layers.update(layer_created)

        # # check if the change is effective
        # layer_fixture_updated = self.isogeo.layer.layer(layer_fixture._id)
        # self.assertEqual(
        #     layer_fixture_updated.name,
        #     "{} - {}".format(get_test_marker(), self.discriminator),
        # )
        # self.assertEqual(
        #     layer_fixture_updated.content,
        #     "{} content - {}".format(get_test_marker(), self.discriminator),
        # )
        # self.assertEqual(
        #     layer_fixture_updated.link,
        #     "https://github.com/isogeo/isogeo-api-py-minsdk",
        # )

        # add created layer to deletion
        # self.li_fixtures_to_delete.append(layer_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
