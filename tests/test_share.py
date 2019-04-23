# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_share
    # for specific
    python -m unittest tests.test_share.TestShares.test_share_augmented
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
app_secret = environ.get("ISOGEO_API_DEV_SECRET")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestShares(unittest.TestCase):
    """Test routes of Isogeo API about shares."""

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

    def tearDown(self):
        """Executed after each test."""
        # close session
        self.isogeo.close()

    # basic search and results
    def test_shares(self):
        """Basic shares request"""
        self.isogeo.shares()

    def test_share(self):
        """Basic share details request"""
        shares = self.isogeo.shares()
        self.isogeo.share(share_id=shares[0].get("_id"))

    def test_share_augmented(self):
        """Augmented share."""
        shares = self.isogeo.shares()
        self.isogeo.share(share_id=shares[0].get("_id"), augment=1)

    def test_share_ids(self):
        """Search with augment option should add shares_id."""
        self.isogeo.search(page_size=0, whole_share=0, augment=1)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
