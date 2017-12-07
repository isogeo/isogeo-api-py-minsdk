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
share_id = environ.get('ISOGEO_API_DEV_ID')
share_token = environ.get('ISOGEO_API_DEV_SECRET')

checker = IsogeoChecker()

# #############################################################################
# ######## Classes #################
# ##################################


class AuthBadCodes(unittest.TestCase):
    """Test authentication process."""
    if not share_id or not share_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    print('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # tests
    def test_bad_secret_length(self):
        """API secret must be 64 length."""
        with self.assertRaises(ValueError):
            isogeo = Isogeo(client_id="python-minimalist-sdk-dev-93test2017id64charsda805062youpi",
                            client_secret="secretwithalengthlessthan64chars_thatshouldntbeacceptedbyisogeo",
                            )
            del isogeo

    def test_bad_id_secret(self):
        """Bad API ID and secret."""
        isogeo = Isogeo(client_id=share_id[:-2],
                        client_secret=share_token)
        with self.assertRaises(ValueError):
            isogeo.connect()

    def test_successed_auth(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(client_id=share_id,
                        client_secret=share_token)
        bearer = isogeo.connect()
        self.assertIsInstance(bearer, tuple)
        self.assertEqual(len(bearer), 2)
        self.assertIsInstance(bearer[0], string_types)
        self.assertIsInstance(bearer[1], int)

    def test_checker_validity_bearer_valid(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(client_id=share_id,
                        client_secret=share_token)
        bearer = isogeo.connect()
        self.assertIsInstance(checker.check_bearer_validity(bearer, isogeo.connect()), tuple)
        self.assertEqual(len(checker.check_bearer_validity(bearer, isogeo.connect())), 2)
        self.assertIsInstance(checker.check_bearer_validity(bearer, isogeo.connect())[0],
                              string_types)
        self.assertIsInstance(checker.check_bearer_validity(bearer, isogeo.connect())[1], int)

    def test_checker_validity_bearer_expired(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(client_id=share_id,
                        client_secret=share_token)
        bearer = isogeo.connect()
        bearer = (bearer[0], 50)
        self.assertIsInstance(checker.check_bearer_validity(bearer, isogeo.connect()), tuple)
        self.assertEqual(len(checker.check_bearer_validity(bearer, isogeo.connect())), 2)
        self.assertIsInstance(checker.check_bearer_validity(bearer, isogeo.connect())[0],
                              string_types)
        self.assertIsInstance(checker.check_bearer_validity(bearer, isogeo.connect())[1], int)

# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == '__main__':
    unittest.main()
