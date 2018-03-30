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


class TestAuthentication(unittest.TestCase):
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
        isogeo = Isogeo(client_id=app_id[:-2],
                        client_secret=app_token)
        with self.assertRaises(ValueError):
            isogeo.connect()

    def test_other_language(self):
        """Try to get other language."""
        isogeo = Isogeo(client_id=app_id,
                        client_secret=app_token,
                        lang="ES")
        # if other language passed the English is applied
        self.assertEqual(isogeo.lang, "en")

    def test_bad_platform(self):
        """Bad platform value."""
        with self.assertRaises(ValueError):
            isogeo = Isogeo(client_id=app_id,
                            client_secret=app_token,
                            platform="skynet"
                            )
            del isogeo

    def test_bad_auth_mode(self):
        """Bad auth mode value."""
        with self.assertRaises(ValueError):
            isogeo = Isogeo(client_id=app_id,
                            client_secret=app_token,
                            auth_mode="fingerprint"
                            )
            del isogeo

    def test_bad_proxy(self):
        """Bad auth mode value."""
        with self.assertRaises(TypeError):
            Isogeo(client_id=app_id,
                   client_secret=app_token,
                   proxy="this_is_my_string_proxy",
                   )

    def test_successed_auth(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(client_id=app_id,
                        client_secret=app_token)
        bearer = isogeo.connect()
        self.assertIsInstance(bearer, tuple)
        self.assertEqual(len(bearer), 2)
        self.assertIsInstance(bearer[0], string_types)
        self.assertIsInstance(bearer[1], int)


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == '__main__':
    unittest.main()
