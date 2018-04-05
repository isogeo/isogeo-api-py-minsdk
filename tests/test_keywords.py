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


class TestKeywords(unittest.TestCase):
    """Test request to unique resource."""
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

        # a random metadata
        search = self.isogeo.search(self.bearer,
                                    whole_share=0,
                                    check=0)
        self.md_rand = search.get("results")[randint(0, 99)]
        self.thez_isogeo = "1616597fbc4348c8b11ef9d59cf594c8"

    def tearDown(self):
        """Executed after each test."""
        pass

    # subresources
    def test_keywords_includes_ok(self):
        """Resource with a few sub resources."""
        self.isogeo.keywords(self.bearer,
                             page_size=0,
                             include=["count", ],
                             )

    def test_keywords_includes_all_ok(self):
        """Resource with all sub resources."""
        self.isogeo.keywords(self.bearer,
                             page_size=0,
                             include="all",
                             )

    def test_keywords_includes_empty(self):
        """Resource with empty sub_resources list."""
        self.isogeo.keywords(self.bearer,
                             page_size=0,
                             include=[],
                             )

    def test_keywords_includes_bad(self):
        """Include sub_resources requires a list."""
        with self.assertRaises(TypeError):
            self.isogeo.keywords(self.bearer,
                                 page_size=0,
                                 include="count",
                                 )

    # specific md
    def test_keywords_specific_mds_ok(self):
        """Keywords filtering on specific metadata."""
        # get random metadata within a small search
        search_10 = self.isogeo.search(self.bearer,
                                       page_size=10,
                                       whole_share=0)
        md_a, md_b = search_10.get("results")[randint(0, 5)].get("_id"),\
                     search_10.get("results")[randint(6, 9)].get("_id")
        md_bad = "trust_me_this_is_a_good_uuid"
        # get random metadata within a small search
        search_ids_1 = self.isogeo.keywords(self.bearer,
                                            specific_md=[md_a, ],
                                            page_size=1)
        search_ids_2 = self.isogeo.keywords(self.bearer,
                                            specific_md=[md_a, md_b],
                                            page_size=1)
        search_ids_3 = self.isogeo.keywords(self.bearer,
                                            specific_md=[md_a, md_b, md_bad],
                                            page_size=1)
        # test type
        self.assertIsInstance(search_ids_1, dict)
        self.assertIsInstance(search_ids_2, dict)
        self.assertIsInstance(search_ids_3, dict)

    def test_keywords_specifc_mds_bad(self):
        """Keywords filtering on specific metadata."""
        # get random metadata within a small search
        search_5 = self.isogeo.search(self.bearer,
                                      page_size=5,
                                      whole_share=0)
        md = search_5.get("results")[randint(0, 4)].get("_id")
        # pass metadata UUID
        with self.assertRaises(TypeError):
            self.isogeo.keywords(self.bearer,
                                 page_size=0,
                                 whole_share=0,
                                 specific_md=md)

    # specific tag
    def test_keywords_specifc_tag_ok(self):
        """Keywords filtering on specific tags."""
        # get tags
        search_tags = self.isogeo.search(self.bearer,
                                         page_size=0,
                                         whole_share=0).get("tags")
        # keep only Isogeo keywords
        keywords = [tag for tag in search_tags
                    if tag.startswith("keyword:isogeo")]
        # get random keywords
        kw_a, kw_b = keywords[randint(0, (len(keywords)/2)-1)],\
                     keywords[randint(len(keywords)/2, len(keywords))]
        kw_bad = "trust_me_i_m_a_real_keyword"
        # get random metadata within a small search
        search_ids_1 = self.isogeo.keywords(self.bearer,
                                            specific_tag=[kw_a, ],
                                            page_size=5)
        search_ids_2 = self.isogeo.keywords(self.bearer,
                                            specific_tag=[kw_a, kw_b],
                                            page_size=5)
        search_ids_3 = self.isogeo.keywords(self.bearer,
                                            specific_tag=[kw_a, kw_b, kw_bad],
                                            page_size=5)
        # # test type
        self.assertIsInstance(search_ids_1, dict)
        self.assertIsInstance(search_ids_2, dict)
        self.assertIsInstance(search_ids_3, dict)

    def test_keywords_specifc_tag_bad(self):
        """Errors filtering on specific tag."""
        kw_bad = "trust_me_i_m_a_real_keyword"
        # pass metadata UUID
        with self.assertRaises(TypeError):
            self.isogeo.keywords(self.bearer,
                                 page_size=0,
                                 whole_share=0,
                                 specific_tag=kw_bad)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
