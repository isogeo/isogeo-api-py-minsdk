# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

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
app_id = environ.get('ISOGEO_API_DEV_ID')
app_secret = environ.get('ISOGEO_API_DEV_SECRET')

# #############################################################################
# ########## Classes ###############
# ##################################


class Search(unittest.TestCase):
    """Test search to Isogeo API."""
    if not app_id or not app_secret:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    print('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=app_id,
                             client_secret=app_secret)
        self.bearer = self.isogeo.connect()

    def tearDown(self):
        """Executed after each test."""
        pass

    # tests
    def test_search(self):
        """Basic search."""
        search = self.isogeo.search(self.bearer, page_size=0, whole_share=0)
        self.assertIsInstance(search, dict)
        self.assertIn("envelope", search)
        self.assertIn("limit", search)
        self.assertIn("offset", search)
        self.assertIn("query", search)
        self.assertIn("results", search)
        self.assertIn("tags", search)
        self.assertIn("total", search)

    def test_bad_parameter_search(self):
        """Search with bad parameter."""
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="type:youpi")
            self.isogeo.search(self.bearer,
                               query="action:yipiyo")

    def test_parameter_not_unique_search(self):
        """SDK raises error for search with a parameter that must be unique."""
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="type:vector-dataset type:raster-dataset")
            self.isogeo.search(self.bearer,
                               query="format:shp format:dwg")
            self.isogeo.search(self.bearer,
                               query="coordinate-system:32517 coordinate-system:4326")
            self.isogeo.search(self.bearer,
                               query="owner:32f7e95ec4e94ca3bc1afda960003882 owner:08b3054757544463abd06f3ab51ee491")

    def test_search_augmented(self):
        """Augmented search."""
        # normal
        search = self.isogeo.search(self.bearer, page_size=0,
                                    whole_share=0, augment=0)
        tags_shares = [i for i in search.get("tags") if i.startswith("share:")]
        self.assertEqual(len(tags_shares), 0)

        # augmented
        search = self.isogeo.search(self.bearer, page_size=0,
                                    whole_share=0, augment=1)
        tags_shares = [i for i in search.get("tags") if i.startswith("share:")]
        self.assertNotEqual(len(tags_shares), 0)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
