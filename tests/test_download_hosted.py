# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:
    
    ```python
    python -m unittest tests.test_download_hosted
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ, path
from sys import exit
from tempfile import mkdtemp
import unittest

# module target
from isogeo_pysdk import Isogeo


# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get("ISOGEO_API_DEV_ID")
app_token = environ.get("ISOGEO_API_DEV_SECRET")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestDownloadHosted(unittest.TestCase):
    """Test download hosted data through Isogeo API."""

    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=app_id, client_secret=app_token)
        self.bearer = self.isogeo.connect()

    def tearDown(self):
        """Executed after each test."""
        pass

    def test_dl_hosted(self):
        """Download an hosted data from Isogeo metadata."""
        search = self.isogeo.search(
            self.bearer,
            whole_share=0,
            query="action:download type:dataset",
            include=["links"],
            page_size=100,
        )
        # get an hosted link
        for md in search.get("results"):
            for link in md.get("links"):
                if link.get("type") == "hosted":
                    target_link = link
                    break
                else:
                    continue

        # stream hosted data
        # Example of link dict:
        # {
        #  "_id": "c7725558b34a4ea8bfe475ca19e27641",
        #  "type": "hosted",
        #  "title": "bootstrap-4.0.0.zip",
        #  "url": "/resources/b765d9886f4b4fc69df65e5206f39a9d/links/c7725558b34a4ea8bfe475ca19e27641.bin",
        #  "kind": "data",
        #  "actions": ["download", ],
        #  "size": "2253029",
        # }
        dl_stream = self.isogeo.dl_hosted(self.bearer, resource_link=target_link)

        # create tempfile and fill with downloaded XML
        tmp_output = mkdtemp(prefix="IsogeoPySDK_")
        with open(path.join(tmp_output, dl_stream[1]), "wb") as fd:
            for block in dl_stream[0].iter_content(1024):
                fd.write(block)

    def test_dl_hosted_bad(self):
        """Test errors raised by download method"""
        with self.assertRaises(ValueError):
            self.isogeo.dl_hosted(self.bearer, resource_link={})
        with self.assertRaises(TypeError):
            self.isogeo.dl_hosted(
                self.bearer, resource_link="my_resource_link_is_a_nice_string"
            )
        with self.assertRaises(ValueError):
            self.isogeo.dl_hosted(self.bearer, resource_link={"type": "url"})


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
