# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import ConfigParser     # to manage options.ini
from os import path
import unittest
 
# module target
from isogeo_pysdk import Isogeo

# #############################################################################
# ########## Classes ###############
# ##################################

class TestIsogeo(unittest.TestCase):

    # ------------ Basic methods ---------------------------------------------
    def setUp(self):
        """Before"""
        # reading config file
        settings_file = "../isogeo_pysdk/isogeo_params.ini"
        if not path.isfile(settings_file):
            return
        else:
            pass
        config = ConfigParser.SafeConfigParser()
        config.read(settings_file)
        self.share_id = config.get('auth', 'app_id')
        self.share_token = config.get('auth', 'app_secret')

        self.isogeo = Isogeo(client_id=self.share_id,
                             client_secret=self.share_token)
        self.jeton = self.isogeo.connect()
     
    def tearDown(self):
        """After"""
        # print("Cleaned up!")

    # ------------ Tests methods ---------------------------------------------

    def test_authentication(self):
        """Authentication and connection to Isogeo API"""
        # jeton = isogeo.connect()

    def test_connection(self):
        """Authentication and connection to Isogeo API"""
        self.jeton = self.isogeo.connect()

    def test_search(self):
        """Isogeo API search"""
        search_empty = self.isogeo.search(self.jeton)
 
        assert(type(search_empty) != unicode)
        assert(type(search_empty) == dict)
        assert("envelope" in search_empty.keys())
        assert("limit" in search_empty.keys())
        assert("offset" in search_empty.keys())
        assert("query" in search_empty.keys())
        assert("results" in search_empty.keys())
        assert("tags" in search_empty.keys())
        assert("total" in search_empty.keys())
        assert(type(search_empty.get("results")) == list)
 
# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
