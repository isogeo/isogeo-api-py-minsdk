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


class TestSearch(unittest.TestCase):
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

    # basic search and results
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
        """Searches with differents page sizes."""
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
        search_whole = self.isogeo.search(self.bearer, page_size=50,
                                          whole_share=1)
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
        self.assertEqual(len(search_whole.get("results")), search_whole.get("total"))

    # specific md
    def test_search_specifc_mds_ok(self):
        """Searches filtering on specific metadata."""
        # get random metadata within a small search
        search_10 = self.isogeo.search(self.bearer,
                                       page_size=10,
                                       whole_share=0)
        md_a, md_b = search_10.get("results")[randint(0, 5)].get("_id"),\
                     search_10.get("results")[randint(6, 9)].get("_id")
        md_bad = "trust_me_this_is_a_good_uuid"
        # get random metadata within a small search
        search_ids_1 = self.isogeo.search(self.bearer,
                                          specific_md=[md_a, ])
        search_ids_2 = self.isogeo.search(self.bearer,
                                          specific_md=[md_a, md_b])
        search_ids_3 = self.isogeo.search(self.bearer,
                                          specific_md=[md_a, md_b, md_bad])
        # test length
        self.assertEqual(len(search_ids_1.get("results")), 1)
        self.assertEqual(len(search_ids_2.get("results")), 2)
        self.assertEqual(len(search_ids_3.get("results")), 2)

    def test_search_specifc_mds_bad(self):
        """Searches filtering on specific metadata."""
        # get random metadata within a small search
        search_5 = self.isogeo.search(self.bearer,
                                      page_size=5,
                                      whole_share=0)
        md = search_5.get("results")[randint(0, 4)].get("_id")
        # pass metadata UUID
        with self.assertRaises(TypeError):
            self.isogeo.search(self.bearer,
                               page_size=0,
                               whole_share=0,
                               specific_md=md)

    # includes
    def test_search_includes_ok(self):
        """Searches including includes."""
        self.isogeo.search(self.bearer,
                           page_size=0,
                           whole_share=0,
                           include=["links", "contacts", ])

    def test_search_includes_all_ok(self):
        """Searches including includes."""
        self.isogeo.search(self.bearer,
                           page_size=0,
                           whole_share=0,
                           include="all")

    def test_search_includes_empty(self):
        """Search with empty includes list."""
        self.isogeo.search(self.bearer,
                           page_size=0,
                           whole_share=0,
                           include=[])

    def test_search_includes_bad(self):
        """Include sub_resrouces require a list."""
        with self.assertRaises(TypeError):
            self.isogeo.search(self.bearer,
                               page_size=0,
                               whole_share=0,
                               include="links")

    # query
    def test_search_parameter_query_ok(self):
        """Search with good query parameters."""
        # contacts
        self.isogeo.search(self.bearer,
                           query="contact:group:643f1035377b4ca59da6f31a39704c34",
                           page_size=0,
                           whole_share=0)
        self.isogeo.search(self.bearer,
                           query="contact:08b3054757544463abd06f3ab51ee491:fe3e8ef97b8446be92d3c315ccbc70f9",
                           page_size=0,
                           whole_share=0)
        # catalog
        self.isogeo.search(self.bearer,
                           query="catalog:633216a375ab48ca8ca72e4a1af7a266",
                           page_size=0,
                           whole_share=0)
        # CSW data-source
        self.isogeo.search(self.bearer,
                           query="data-source:ace35ec171da4d0aa2f10e7308dcbdc5",
                           page_size=0,
                           whole_share=0)
        # format
        self.isogeo.search(self.bearer,
                           query="format:shp",
                           page_size=0,
                           whole_share=0)
        # has-no
        self.isogeo.search(self.bearer,
                           query="has-no:keyword",
                           page_size=0,
                           whole_share=0)
        # inspire themes
        self.isogeo.search(self.bearer,
                           query="keyword:inspire-theme:administrativeunits",
                           page_size=0,
                           whole_share=0)
        # keyword
        self.isogeo.search(self.bearer,
                           query="keyword:isogeo:2018",
                           page_size=0,
                           whole_share=0)
        # licenses
        self.isogeo.search(self.bearer,
                           query="license:isogeo:63f121e14eda4f47b748595e0bcccc31",
                           page_size=0,
                           whole_share=0)
        self.isogeo.search(self.bearer,
                           query="license:32f7e95ec4e94ca3bc1afda960003882:76c02a0baf594c77a569b3a1325aee30",
                           page_size=0,
                           whole_share=0)
        # SRS
        self.isogeo.search(self.bearer,
                           query="coordinate-system:2154",
                           page_size=0,
                           whole_share=0)
        # types
        self.isogeo.search(self.bearer,
                           query="type:dataset",
                           page_size=0,
                           whole_share=0)
        self.isogeo.search(self.bearer,
                           query="type:vector-dataset",
                           page_size=0,
                           whole_share=0)
        self.isogeo.search(self.bearer,
                           query="type:raster-dataset",
                           page_size=0,
                           whole_share=0)
        self.isogeo.search(self.bearer,
                           query="type:service",
                           page_size=0,
                           whole_share=0)
        self.isogeo.search(self.bearer,
                           query="type:resource",
                           page_size=0,
                           whole_share=0)
        # workgroup - owner
        self.isogeo.search(self.bearer,
                           query="owner:32f7e95ec4e94ca3bc1afda960003882",
                           page_size=0,
                           whole_share=0)
        # unknown
        self.isogeo.search(self.bearer,
                           query="unknown:filter",
                           page_size=0,
                           whole_share=0)

    def test_search_bad_parameter_query(self):
        """Search with bad parameter."""
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="type:youpi")
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="action:yipiyo")
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="provider:youplaboum")

    def test_search_bad_parameter_geographic(self):
        """Search with bad parameter."""
        # geometric operator
        with self.assertRaises(ValueError):
            # georel should'nt be used without box or geo
            self.isogeo.search(self.bearer,
                               georel="intersects")
        with self.assertRaises(ValueError):
            # georel bad value
            self.isogeo.search(self.bearer,
                               bbox="-4.970,30.69418,8.258,51.237",
                               georel="cross")

    def test_parameter_not_unique_search(self):
        """SDK raises error for search with a parameter that must be unique."""
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="coordinate-system:32517 coordinate-system:4326")
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="format:shp format:dwg")
        with self.assertRaises(ValueError):
            self.isogeo.search(self.bearer,
                               query="owner:32f7e95ec4e94ca3bc1afda960003882 owner:08b3054757544463abd06f3ab51ee491")
        with self.assertRaises(ValueError):
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

    # search utilities
    def test_search_augmented(self):
        """Augmented search with shares UUID"""
        self.assertFalse(hasattr(self.isogeo, "shares_id"))  # at start, shares_id attribute doesn't exist
        # normal
        search = self.isogeo.search(self.bearer, page_size=0,
                                    whole_share=0, augment=0)
        tags_shares = [i for i in search.get("tags") if i.startswith("share:")]
        self.assertEqual(len(tags_shares), 0)
        self.assertFalse(hasattr(self.isogeo, "shares_id"))    # shares_id attribute still doesn't exist
        # augmented
        search = self.isogeo.search(self.bearer, page_size=0,
                                    whole_share=0, augment=1)
        tags_shares = [i for i in search.get("tags")
                       if i.startswith("share:")]
        self.assertNotEqual(len(tags_shares), 0)
        self.assertTrue(hasattr(self.isogeo, "shares_id"))  # now it exists
        # redo using existing attribute
        search = self.isogeo.search(self.bearer, page_size=0,
                                    whole_share=0, augment=1)

    def test_search_tags_dictionarized(self):
        """Search tags stored into key/values structures."""
        search = self.isogeo.search(self.bearer, page_size=0,
                                    whole_share=0, tags_as_dicts=1)
        tags = search.get("tags")
        self.assertIn("actions", tags)
        self.assertIn("catalogs", tags)
        self.assertIn("contacts", tags)
        self.assertIn("data-sources", tags)
        self.assertIn("formats", tags)
        self.assertIn("inspires", tags)
        self.assertIn("keywords", tags)
        self.assertIn("licenses", tags)
        self.assertIn("owners", tags)
        self.assertIn("providers", tags)
        self.assertIn("srs", tags)
        self.assertIn("types", tags), tags

    def test_app_properties(self):
        """Test if application properties are well added."""
        self.assertFalse(hasattr(self.isogeo, "app_properties"))
        # add it
        self.isogeo.get_app_properties(self.bearer)
        # now it exists
        self.assertTrue(hasattr(self.isogeo, "app_properties"))
        # check structure
        props = self.isogeo.app_properties
        self.assertIsInstance(props, dict)
        self.assertIn("admin_url", props)
        self.assertIn("creation_date", props)
        self.assertIn("last_update", props)
        self.assertIn("name", props)
        self.assertIn("type", props)
        self.assertIn("kind", props)
        self.assertIn("url", props)
        # redo using existing attribute
        self.isogeo.get_app_properties(self.bearer)

    def test_get_link_kinds(self):
        """Test link kinds response."""
        links = self.isogeo.get_link_kinds(self.bearer)
        self.assertEqual(len(links), 8)
        self.assertEqual(len(links[0]), 3)

    def test_get_directives(self):
        """Test environment directives response."""
        dirs = self.isogeo.get_directives(self.bearer)
        self.assertEqual(len(dirs), 9)

    def test_get_formats(self):
        """Test formats and format details requests."""
        # all datasets and services formats
        formats = self.isogeo.get_formats(self.bearer)
        self.assertEqual(len(formats), 32)
        self.assertEqual(len(formats[0]), 7)
        # a specific format
        shape = self.isogeo.get_formats(self.bearer, format_code="shp")
        self.assertEqual(len(shape), 7)
        # if specific format is bad formatted, so show all formats
        bad_specific_format = self.isogeo.get_formats(self.bearer,
                                                      format_code=["shp", ])
        self.assertEqual(len(bad_specific_format), 32)
        self.assertEqual(bad_specific_format, formats)

    def test_get_srs(self):
        """Test coordinate-systmes requests."""
        # all Isoego srs
        srs = self.isogeo.get_coordinate_systems(self.bearer)
        self.assertEqual(len(srs), 4301)
        self.assertEqual(len(srs[0]), 3)
        # a specific srs
        wgs84 = self.isogeo.get_coordinate_systems(self.bearer,
                                                   srs_code="4326")
        self.assertEqual(len(wgs84), 3)
        # if specific srs is bad formatted, so show all srs
        bad_specific_srs = self.isogeo.get_coordinate_systems(self.bearer,
                                                              srs_code=["4326", ])
        self.assertEqual(len(bad_specific_srs), 4301)
        self.assertEqual(bad_specific_srs, srs)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
