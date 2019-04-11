# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_resource
    # for specific
    python -m unittest tests.test_resource.TestResource.test_resource_includes_ok
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import unittest
from os import environ
from random import randint
from sys import exit

# module target
from isogeo_pysdk import Isogeo
from isogeo_pysdk import __version__ as pysdk_version

# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get("ISOGEO_API_DEV_ID")
app_secret = environ.get("ISOGEO_API_DEV_SECRET")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestResource(unittest.TestCase):
    """Test request to unique resource."""

    if not app_id or not app_secret:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=app_id, client_secret=app_secret)
        self.isogeo.connect()

        # a random metadata
        search = self.isogeo.search(whole_share=0, check=0)
        self.md_rand = search.get("results")[randint(0, 99)]

    def tearDown(self):
        """Executed after each test."""
        pass

    # includes
    def test_resource_includes_ok(self):
        """Resource with a few sub resources."""
        self.isogeo.resource(
            id_resource=self.md_rand.get("_id"), include=["links", "contacts"]
        )

    def test_resource_includes_all_ok(self):
        """Resource with all sub resources."""
        self.isogeo.resource(id_resource=self.md_rand.get("_id"), include="all")

    def test_resource_includes_empty(self):
        """Resource with empty sub_resources list."""
        self.isogeo.resource(id_resource=self.md_rand.get("_id"), include=[])

    def test_resource_includes_bad(self):
        """Include sub_resrouces requires a list."""
        with self.assertRaises(TypeError):
            self.isogeo.resource(
                id_resource=self.md_rand.get("_id"), include="contacts"
            )

    # subresource
    def test_resource_subresource_ok(self):
        """Resource with a few sub resources."""
        self.isogeo.resource(id_resource=self.md_rand.get("_id"), subresource="links")

    def test_resource_subresource_empty(self):
        """Resource with empty sub_resources list."""
        self.isogeo.resource(id_resource=self.md_rand.get("_id"), subresource="tags")


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
