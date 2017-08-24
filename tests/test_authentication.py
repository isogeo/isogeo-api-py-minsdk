# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import unittest

# Isogeo
from isogeo_pysdk import Isogeo, __version__ as pysdk_version

# #############################################################################
# ######## Globals #################
# ##################################

# API access
share_id = environ.get('ISOGEO_API_DEV_ID')
share_token = environ.get('ISOGEO_API_DEV_SECRET')

# #############################################################################
# ######## Classes #################
# ##################################


class AuthBadCodes(unittest.TestCase):
    """Test authentication process."""
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
        """Bad API ID and secret."""
        isogeo = Isogeo(client_id=share_id,
                        client_secret=share_token)
        bearer = isogeo.connect()
        self.assertIsInstance(bearer, tuple)
        self.assertEqual(len(bearer), 2)
        self.assertIsInstance(bearer[0], basestring)
        self.assertIsInstance(bearer[1], int)

# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == '__main__':
    unittest.main()
