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
    def test_shares(self):
        """Basic shares request"""
        self.isogeo.shares(self.bearer)

    def test_share(self):
        """Basic share details request"""
        shares = self.isogeo.shares(self.bearer)
        self.isogeo.share(self.bearer,
                          share_id=shares[0].get("_id"))

    def test_share_augmented(self):
        """Augmented share."""
        shares = self.isogeo.shares(self.bearer)
        self.isogeo.share(self.bearer,
                          share_id=shares[0].get("_id"),
                          augment=1)

    def test_share_ids(self):
        """Search with augment option should add shares_id."""
        self.isogeo.search(self.bearer, page_size=0,
                           whole_share=0, augment=1)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
