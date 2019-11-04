# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_service_layers
# for specific
python -m unittest tests.test_service_layers.TestServiceLayers.test_layers_create
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
from isogeo_pysdk import Isogeo, Metadata, ServiceLayer


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
    return "TEST_PySDK - ServiceLayers - {}".format(_getframe(1).f_code.co_name)


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
            metadata=self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID),
            layer=layer_new,
        )

        # add created layer to deletion
        self.li_fixtures_to_delete.append(layer_new)

    def test_layers_association(self):
        """POST
        :resources/{service_uuid}/layers/{layer_uuid}/dataset/{dataset_uuid}"""
        # fixtures
        metadata_service = self.isogeo.services.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            service_type="ogc",
            service_format="wms",
            service_url="https://magosm.magellium.com/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities",
            service_title="{}_{}".format(
                hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
            ),
            check_exists=0,
        )
        metadata_dataset = self.isogeo.metadata.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            metadata=Metadata(
                type="vectorDataset",
                title="{} - {}".format(get_test_marker(), self.discriminator),
            ),
        )

        # vars
        layer_name = "{} - {}".format(get_test_marker(), self.discriminator)
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
            metadata=metadata_service, layer=layer_new
        )

        # associate it
        self.isogeo.metadata.layers.associate_metadata(
            service=metadata_service, layer=layer_created, dataset=metadata_dataset
        )

        # check association result
        service_updated = self.isogeo.metadata.get(
            metadata_id=metadata_service._id, include=("layers",)
        )

        li_associated_layers = [
            layer
            for layer in service_updated.layers
            if layer.get("dataset") is not None
        ]

        # test results
        self.assertIsInstance(li_associated_layers[0].get("dataset"), dict)
        ServiceLayer(**li_associated_layers[0])

        # -- dissociate
        self.isogeo.metadata.layers.dissociate_metadata(
            service=metadata_service, layer=layer_created, dataset=metadata_dataset
        )

        # add created layer to deletion
        self.isogeo.metadata.delete(metadata_service._id)
        self.isogeo.metadata.delete(metadata_dataset._id)

    # -- GET --
    def test_layers_listing(self):
        """GET :resources/{metadata_uuid}/layers/}"""
        # retrieve metadata layers
        md_layers = self.isogeo.metadata.layers.listing(
            self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID)
        )
        # parse and test object loader
        for i in md_layers:
            # load it
            layer = ServiceLayer(**i)
            # tests attributes structure
            self.assertTrue(hasattr(layer, "_id"))
            self.assertTrue(hasattr(layer, "dataset"))
            self.assertTrue(hasattr(layer, "mimeTypes"))
            self.assertTrue(hasattr(layer, "name"))
            self.assertTrue(hasattr(layer, "titles"))
            # tests attributes value
            self.assertEqual(layer._id, i.get("_id"))
            self.assertEqual(layer.mimeTypes, i.get("mimeTypes"))
            self.assertEqual(layer.name, i.get("id"))
            self.assertEqual(layer.titles, i.get("titles"))

    def test_layers_detailed(self):
        """GET :resources/{metadata_uuid}/layers/{layer_uuid}"""
        # get layers
        md_layers = self.isogeo.metadata.layers.listing(
            self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID)
        )
        # pick one
        layer_id = sample(md_layers, 1)[0].get("_id")
        self.isogeo.metadata.layers.layer(
            metadata_id=METADATA_TEST_FIXTURE_UUID, layer_id=layer_id
        )

    # -- PUT/PATCH --
    def test_layers_update(self):
        """PUT :resources/{metadata_uuid}/layers/{layer_uuid}"""
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
            metadata=self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID),
            layer=layer_new,
        )

        # modify local object
        layer_created.name = "{} - UPDATED".format(layer_name)

        # update the online layer
        layer_updated = self.isogeo.metadata.layers.update(layer_created)
        self.assertEqual(layer_updated.name, "{} - UPDATED".format(layer_name))

        # check if the change is effective
        layer_to_check = self.isogeo.metadata.layers.layer(
            metadata_id=METADATA_TEST_FIXTURE_UUID, layer_id=layer_created._id
        )
        self.assertEqual(layer_to_check.name, "{} - UPDATED".format(layer_name))

        # add created layer to deletion
        self.li_fixtures_to_delete.append(layer_to_check)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
