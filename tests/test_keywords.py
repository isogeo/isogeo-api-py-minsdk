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
    def test_keywords_subresources_ok(self):
        """Resource with a few sub resources."""
        self.isogeo.keywords(self.bearer,
                             page_size=0,
                             sub_resources=["count", ],
                             )

    def test_keywords_subresources_all_ok(self):
        """Resource with all sub resources."""
        self.isogeo.keywords(self.bearer,
                             page_size=0,
                             sub_resources="all",
                             )

    def test_keywords_subresources_empty(self):
        """Resource with empty sub_resources list."""
        self.isogeo.keywords(self.bearer,
                             page_size=0,
                             sub_resources=[],
                             )

    def test_keywords_subresources_bad(self):
        """Include sub_resrouces requires a list."""
        with self.assertRaises(TypeError):
            self.isogeo.keywords(self.bearer,
                                 page_size=0,
                                 sub_resources="count",
                                 )

    # specific md

    # specific tag

# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
