# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from sys import exit
import unittest

# module target
from isogeo_pysdk import IsogeoUtils, __version__ as pysdk_version


# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get('ISOGEO_API_DEV_ID')
app_token = environ.get('ISOGEO_API_DEV_SECRET')

# #############################################################################
# ########## Classes ###############
# ##################################


class Search(unittest.TestCase):
    """Test search to Isogeo API."""
    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        # """Executed before each test."""
        self.utils = IsogeoUtils()
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # Isogeo components versions
    def test_get_isogeo_version_api(self):
        """"""
        version_api = self.utils.get_isogeo_version(component="api")
        version_api_naive = self.utils.get_isogeo_version()
        self.assertIsInstance(version_api, str)
        self.assertIsInstance(version_api_naive, str)
        self.assertEqual(version_api, version_api_naive)

    def test_get_isogeo_version_app(self):
        """"""
        version_app = self.utils.get_isogeo_version(component="app")
        self.assertIsInstance(version_app, str)

    def test_get_isogeo_version_db(self):
        """Check res"""
        version_db = self.utils.get_isogeo_version(component="db")
        self.assertIsInstance(version_db, str)

    def test_get_isogeo_version_bad_parameter(self):
        """Raise error if component parameter is bad."""
        with self.assertRaises(ValueError):
            self.utils.get_isogeo_version(component="youpi")

    # base URLs
    def test_set_base_url(self):
        """"""
        platform, base_url = self.utils.set_base_url()
        self.assertIsInstance(platform, str)
        self.assertIsInstance(base_url, str)

    def test_set_base_url_bad_parameter(self):
        """Raise error if platform parameter is bad."""
        with self.assertRaises(ValueError):
            self.utils.set_base_url(platform="skynet")

    # UUID converter
    def test_hex_to_urn(self):
        """Test UUID converter from hex to urn"""
        self.utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b",
                                mode=1)

    def test_urn_to_hex(self):
        """Test UUID converter from urn to hex"""
        self.utils.convert_uuid(in_uuid="urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b",
                                mode=0)
        self.utils.convert_uuid(in_uuid="urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b",
                                mode=0)

    def test_uuid_converter_bad_parameter(self):
        """Raise error if one parameter is bad."""
        with self.assertRaises(ValueError):
            self.utils.convert_uuid(in_uuid="oh_my_bad_i_m_not_a_correct_uuid")
        with self.assertRaises(TypeError):
            self.utils.convert_uuid(in_uuid=2)
        with self.assertRaises(TypeError):
            self.utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b",
                                    mode="ups_not_an_int")
            self.utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b",
                                    mode=3)
            self.utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b",
                                    mode=True)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
