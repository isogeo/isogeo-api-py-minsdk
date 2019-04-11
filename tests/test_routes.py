# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_routes
    # for specific
    python -m unittest tests.test_routes.TestRoutes.test_resources_search
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from sys import exit
import unittest

# module target
from isogeo_pysdk import Isogeo, __version__ as pysdk_version


# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get("ISOGEO_API_DEV_ID")
app_token = environ.get("ISOGEO_API_DEV_SECRET")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestRoutes(unittest.TestCase):
    """Test search to Isogeo API."""

    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=app_id, client_secret=app_token)
        self.isogeo.connect()

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- ALL APPS ------------------------------------------------------------
    def test_resources_search(self):
        """GET :/resources/search and GET :/resources/{rid}"""
        search = self.isogeo.search(page_size=1, whole_share=0, check=0)

        self.isogeo.resource(id_resource=search.get("results")[0].get("_id"))

    def test_shares(self):
        """GET :/shares and GET :/shares/{sid}"""
        shares = self.isogeo.shares()
        self.isogeo.share(share_id=shares[0].get("_id"))

    def test_thesauri(self):
        """GET :/thesauri and GET :/thesaurus/{tid}"""
        thesauri = self.isogeo.thesauri()
        self.isogeo.thesaurus(thez_id=thesauri[0].get("_id"))

    def test_licenses(self):
        """Try to get licenses details."""
        search = self.isogeo.search(page_size=0, whole_share=0, check=0)
        # get a workgroup id and a license within tags
        for tag in search.get("tags"):
            if tag.startswith("license:"):
                lic = tag.split(":")[2]
            else:
                pass

            if tag.startswith("owner:"):
                wg = tag.split(":")[1]
            else:
                pass

        # get workgroup licenses
        licenses = self.isogeo.licenses(owner_id=wg)
        self.assertIsInstance(licenses, tuple)
        self.assertIn(401, licenses)

        # a specific license
        license = self.isogeo.license(license_id="f6e0c665905a4feab1e9c1d6359a225f")
        self.assertIsInstance(license, dict)
        self.assertIn("_id", license)
        self.assertIn("_tag", license)
        self.assertIn("_abilities", license)
        self.assertIn("link", license)
        self.assertIn("name", license)

    def test_keywords(self):
        """GET :/thesauri/keywords"""
        thez_id = self.isogeo.thesauri()[0].get("_id")
        # list tags
        thez_keywords = self.isogeo.keywords(thez_id=thez_id, page_size=1)
        self.assertIsInstance(thez_keywords, dict)
        self.assertIn("limit", thez_keywords)
        self.assertIn("offset", thez_keywords)
        self.assertIn("results", thez_keywords)
        self.assertIn("total", thez_keywords)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
