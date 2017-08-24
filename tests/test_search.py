# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import unittest

# module target
from isogeo_pysdk import Isogeo, __version__ as pysdk_version


# #############################################################################
# ######## Globals #################
# ##################################

# API access
share_id = environ.get('ISOGEO_API_DEV_ID')
share_token = environ.get('ISOGEO_API_DEV_SECRET')

# #############################################################################
# ########## Classes ###############
# ##################################


class Search(unittest.TestCase):
    """Test search to Isogeo API."""
    print('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=share_id,
                             client_secret=share_token)
        self.bearer = self.isogeo.connect()

    def tearDown(self):
        """Executed after each test."""
        pass

    # tests
    def test_search(self):
        """Basic search."""
        search = self.isogeo.search(self.bearer)
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


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
