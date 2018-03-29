# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from sys import exit
from tempfile import mkstemp
import unittest

# module target
from isogeo_pysdk import Isogeo


# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get('ISOGEO_API_DEV_ID')
app_token = environ.get('ISOGEO_API_DEV_SECRET')

# #############################################################################
# ########## Classes ###############
# ##################################


class DownloadHosted(unittest.TestCase):
    """Test download hosted data through Isogeo API."""
    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=app_id,
                             client_secret=app_token)
        self.bearer = self.isogeo.connect()

    def tearDown(self):
        """Executed after each test."""
        pass

    # # metadata models
    # def test_dl_hosted(self):
    #     """Download an hosted data from Isogeo metadata."""
    #     search = self.isogeo.search(self.bearer, whole_share=0,
    #                                 query="action:download type:dataset",
    #                                 sub_resources=["links", ],
    #                                 page_size=100)
    #     # get an hosted link
    #     for md in search.get("results"):
    #         for link in md.get("links"):
    #             if link.get("type") == "hosted":
    #                 target_link = link
    #             else:
    #                 continue

    #     # download the XML version
    #     print(target_link)
    #     dl_stream = self.isogeo.dl_hosted(self.bearer,
    #                                       id_resource=md.get("_id"),
    #                                       resource_link=target_link)

    #     # create tempfile and fill with downloaded XML
    #     # tmp_output = mkstemp(prefix="IsogeoPySDK_" + md.get("_id")[:5])
    #     with open(dl_stream[1], 'wb') as fd:
    #         for block in dl_stream[0].iter_content(1024):
    #             fd.write(block)

    def test_dl_hosted_bad(self):
        """Test errors raised by download method"""
        with self.assertRaises(ValueError):
            self.isogeo.dl_hosted(self.bearer,
                                  id_resource="trust_me_its_an_uuid",
                                  resource_link={})


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
