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
        search = self.isogeo.search(self.bearer, page_size=0, whole_share=0)
        self.assertIsInstance(search, dict)
        self.assertIn("envelope", search)
        self.assertIn("limit", search)
        self.assertIn("offset", search)
        self.assertIn("query", search)
        self.assertIn("results", search)
        self.assertIn("tags", search)
        self.assertIn("total", search)

    # tests
    def test_search_includes(self):
        """Search with sub-resources included."""
        # from a specific md. Can be viewed here: https://goo.gl/RDWDWJ
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    specific_md=["461a37319b704b90b49babdd79827e4f",])
        md = search.get("results")[0]
        self.assertIsInstance(md, dict)
        self.assertIn("_id", md)
        self.assertIn("_created", md)
        self.assertIn("_modified", md)
        self.assertIn("_creator", md)
        self.assertIn("_abilities", md)
        self.assertIn("title", md)
        self.assertIn("abstract", md)
        self.assertIn("path", md)
        self.assertIn("format", md)
        self.assertIn("formatVersion", md)
        self.assertIn("created", md)
        self.assertIn("modified", md)
        self.assertIn("published", md)
        self.assertIn("language", md)
        self.assertIn("type", md)
        self.assertIn("tags", md)
        self.assertIn("envelope", md)
        self.assertIn("editionProfile", md)
        self.assertIn("scale", md)
        self.assertIn("series", md)
        self.assertIn("distance", md)
        self.assertIn("validFrom", md)
        self.assertIn("validTo", md)
        self.assertIn("updateFrequency", md)
        self.assertIn("validityComment", md)
        self.assertIn("encoding", md)
        self.assertIn("collectionMethod", md)
        self.assertIn("collectionContext", md)
        self.assertIn("topologicalConsistency", md)
        self.assertIn("features", md)

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
