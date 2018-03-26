# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from random import randint
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
    logging.debug('Isogeo PySDK version: {0}'.format(pysdk_version))

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
        # Search with _limit=0 must be empty of results.
        self.assertEqual(len(search.get("results")), 0)

    def test_search_length(self):
        """Searches with differents page sizes or filter on specific md."""
        rand = randint(1, 100)

        # requests
        search_default = self.isogeo.search(self.bearer,   # default value= 100
                                            whole_share=0)
        search_10 = self.isogeo.search(self.bearer, page_size=10,
                                       whole_share=0)
        search_20 = self.isogeo.search(self.bearer, page_size=20,
                                       whole_share=0)
        search_50 = self.isogeo.search(self.bearer, page_size=50,
                                       whole_share=0)
        search_100 = self.isogeo.search(self.bearer, page_size=100,
                                        whole_share=0)
        search_sup100 = self.isogeo.search(self.bearer, page_size=103,
                                           whole_share=0)
        search_rand = self.isogeo.search(self.bearer, page_size=rand,
                                         whole_share=0)

        # compare pages size and length of results
        self.assertEqual(len(search_default.get("results")), 100)
        self.assertEqual(len(search_10.get("results")), 10)
        self.assertEqual(len(search_20.get("results")), 20)
        self.assertEqual(len(search_50.get("results")), 50)
        self.assertEqual(len(search_100.get("results")), 100)
        self.assertEqual(len(search_sup100.get("results")), 100)
        self.assertEqual(len(search_rand.get("results")), rand)

    def test_search_specifc_mds(self):
        """Searches filtering on specific metadata."""
        # get random metadata within a small search
        search_10 = self.isogeo.search(self.bearer,
                                       page_size=10,
                                       whole_share=0)
        md_a, md_b = search_10.get("results")[randint(0, 5)].get("_id"),\
                     search_10.get("results")[randint(6, 9)].get("_id")
        # get random metadata within a small search
        search_ids_1 = self.isogeo.search(self.bearer,
                                          specific_md=[md_a, ])
        search_ids_2 = self.isogeo.search(self.bearer,
                                          specific_md=[md_a, md_b])
        # test length
        self.assertEqual(len(search_ids_1.get("results")), 1)
        self.assertEqual(len(search_ids_2.get("results")), 2)

    def test_search_bad_parameter_query(self):
        """Search with bad parameter."""
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="type:youpi")
            self.isogeo.search(self.bearer,
                               query="action:yipiyo")
            self.isogeo.search(self.bearer,
                               query="provider:youplaboum")

    def test_search_bad_parameter_geographic(self):
        """Search with bad parameter."""
        # geometric operator
        with self.assertRaises(ValueError):
            # georel should'nt be used without box or geo
            self.isogeo.search(self.bearer,
                               georel="intersects")
            # georel bad value
            self.isogeo.search(self.bearer,
                               box="-4.970,30.69418,8.258,51.237",
                               georel="cross")

    def test_parameter_not_unique_search(self):
        """SDK raises error for search with a parameter that must be unique."""
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="coordinate-system:32517 coordinate-system:4326")
            self.isogeo.search(self.bearer,
                               query="format:shp format:dwg")
            self.isogeo.search(self.bearer,
                               query="owner:32f7e95ec4e94ca3bc1afda960003882 owner:08b3054757544463abd06f3ab51ee491")
            self.isogeo.search(self.bearer,
                               query="type:vector-dataset type:raster-dataset")
        # disabling check, it should not raise anything
        self.isogeo.search(self.bearer,
                           query="coordinate-system:32517 coordinate-system:4326",
                           check=0)
        self.isogeo.search(self.bearer,
                           query="format:shp format:dwg",
                           check=0)
        self.isogeo.search(self.bearer,
                           query="owner:32f7e95ec4e94ca3bc1afda960003882 owner:08b3054757544463abd06f3ab51ee491",
                           check=0)
        self.isogeo.search(self.bearer,
                           query="type:vector-dataset type:raster-dataset",
                           check=0)

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

    def test_app_properties(self):
        """Test if application properties are well added."""
        self.isogeo.get_app_properties(self.bearer)
        hasattr(self.isogeo, "app_properties")
        props = self.isogeo.app_properties
        self.assertIsInstance(props, dict)
        self.assertIn("admin_url", props)
        self.assertIn("creation_date", props)
        self.assertIn("last_update", props)
        self.assertIn("name", props)
        self.assertIn("type", props)
        self.assertIn("kind", props)
        self.assertIn("url", props)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
