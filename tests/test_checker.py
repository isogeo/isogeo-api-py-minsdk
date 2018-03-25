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

# Isogeo
from isogeo_pysdk import Isogeo, IsogeoChecker, __version__ as pysdk_version
from six import string_types

# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get('ISOGEO_API_DEV_ID')
app_token = environ.get('ISOGEO_API_DEV_SECRET')

checker = IsogeoChecker()

# #############################################################################
# ######## Classes #################
# ##################################


class AuthBadCodes(unittest.TestCase):
    """Test authentication process."""
    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    logging.debug('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # auth
    def test_checker_validity_bearer_valid(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(client_id=app_id,
                        client_secret=app_token)
        bearer = isogeo.connect()
        self.assertIsInstance(checker.check_bearer_validity(bearer,
                                                            isogeo.connect()),
                              tuple)
        self.assertEqual(len(checker.check_bearer_validity(bearer,
                                                           isogeo.connect())),
                         2)
        self.assertIsInstance(checker.check_bearer_validity(bearer,
                                                            isogeo.connect())[0],
                              string_types)
        self.assertIsInstance(checker.check_bearer_validity(bearer,
                                                            isogeo.connect())[1],
                              int)

    def test_checker_validity_bearer_expired(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(client_id=app_id,
                        client_secret=app_token)
        bearer = isogeo.connect()
        bearer = (bearer[0], 50)
        self.assertIsInstance(checker.check_bearer_validity(bearer,
                                                            isogeo.connect()),
                              tuple)
        self.assertEqual(len(checker.check_bearer_validity(bearer,
                                                           isogeo.connect())),
                         2)
        self.assertIsInstance(checker.check_bearer_validity(bearer,
                                                            isogeo.connect())[0],
                              string_types)
        self.assertIsInstance(checker.check_bearer_validity(bearer,
                                                            isogeo.connect())[1],
                              int)

    # UUID
    def test_checker_uuid_valid(self):
        """Test if a valid UUID is matched."""
        uuid_ok_1 = checker.check_is_uuid("0269803d50c446b09f5060ef7fe3e22b")
        uuid_ok_2 = checker.check_is_uuid("urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b")
        uuid_ok_3 = checker.check_is_uuid("urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b")
        # test type
        self.assertIsInstance(uuid_ok_1, bool)
        self.assertIsInstance(uuid_ok_2, bool)
        self.assertIsInstance(uuid_ok_3, bool)
        # test value
        self.assertEqual(uuid_ok_1, 1)
        self.assertEqual(uuid_ok_2, 1)
        self.assertEqual(uuid_ok_3, 1)

    def test_checker_uuid_bad(self):
        """Test if a valid UUID is matched."""
        uuid_bad_1 = checker.check_is_uuid("0269803d50c446b09f5060ef7fe3e22")
        uuid_bad_2 = checker.check_is_uuid("urn:umid:0269803d-50c4-46b0-9f50-60ef7fe3e22b")
        uuid_bad_3 = checker.check_is_uuid("urn:geonetwork:siret:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b")
        # test type
        self.assertIsInstance(uuid_bad_1, bool)
        self.assertIsInstance(uuid_bad_2, bool)
        self.assertIsInstance(uuid_bad_3, bool)
        # test value
        self.assertEqual(uuid_bad_1, 0)
        self.assertEqual(uuid_bad_2, 0)
        self.assertEqual(uuid_bad_3, 0)

    # Internet connection
    def test_checker_internet_ok(self):
        """Test if a host works to valid connection from a good host."""
        self.assertEqual(checker.check_internet_connection(), 1)
        self.assertEqual(checker.check_internet_connection("google.com"), 1)

    def test_checker_internet_bad(self):
        """Test if a host works to invalid connection from bad hostnames."""
        self.assertEqual(checker.check_internet_connection("https://www.isogeo.com"), 0)
        self.assertEqual(checker.check_internet_connection("https://www.google.com"), 0)

    # edition tabs
    def test_check_edit_tab_ok(self):
        """Test if a good tab is valid"""

        


    def test_check_edit_tab_bad(self):
        """Raise errors"""
        with self.assertRaises(TypeError):
            checker.check_edit_tab(tab=1984, md_type="vector-dataset")
            checker.check_edit_tab(tab="identification",
                                   md_type=2)
            checker.check_edit_tab(tab=True,
                                   md_type=False)
        with self.assertRaises(ValueError):
            checker.check_edit_tab(tab="download", md_type="raster-dataset")
            checker.check_edit_tab(tab="identification", md_type="nogeographic")
            # resource type
            checker.check_edit_tab(tab="geography", md_type="resource")
            checker.check_edit_tab(tab="quality", md_type="resource")
            checker.check_edit_tab(tab="attributes", md_type="resource")
            # raster
            checker.check_edit_tab(tab="attributes", md_type="raster-dataset")
            # service
            checker.check_edit_tab(tab="attributes", md_type="service")


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == '__main__':
    unittest.main()
