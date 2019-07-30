# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_authentication
    # for specific
    python -m unittest tests.test_authentication.TestAuthentication.test_other_language
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

# Isogeo
from isogeo_pysdk import Isogeo, IsogeoChecker, __version__ as pysdk_version

# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get("ISOGEO_API_DEV_ID")
app_token = environ.get("ISOGEO_API_DEV_SECRET")

checker = IsogeoChecker()

# #############################################################################
# ######## Classes #################
# ##################################


class TestAuthentication(unittest.TestCase):
    """Test authentication process."""

    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()

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
            isogeo = Isogeo(
                client_id="python-minimalist-sdk-dev-93test2017id64charsda805062youpi",
                client_secret="secretwithalengthlessthan64chars_thatshouldntbeacceptedbyisogeo",
            )
            del isogeo

    def test_bad_id_secret(self):
        """Bad API ID and secret."""
        isogeo = Isogeo(client_id=app_id[:-2], client_secret=app_token)
        with self.assertRaises(ValueError):
            isogeo.connect()

    def test_other_language(self):
        """Try to get other language."""
        isogeo = Isogeo(client_id=app_id, client_secret=app_token, lang="ES")
        # if other language passed the English is applied
        self.assertEqual(isogeo.lang, "en")

        # close
        isogeo.close()

    def test_bad_platform(self):
        """Bad platform value."""
        with self.assertRaises(ValueError):
            isogeo = Isogeo(
                client_id=app_id, client_secret=app_token, platform="skynet"
            )
            del isogeo

    def test_bad_auth_mode(self):
        """Bad auth mode value."""
        with self.assertRaises(ValueError):
            isogeo = Isogeo(
                client_id=app_id, client_secret=app_token, auth_mode="fingerprint"
            )
            del isogeo

    # Proxy management
    def test_proxy(self):
        """Simulate proxy settings assignment."""
        isogeo = Isogeo(
            client_id=app_id,
            client_secret=app_token,
            proxy={
                "http": "http://proxy.localhost:8888",
                "https": "http://proxy.localhost:8888",
            },
        )

        # close
        isogeo.close()

    def test_bad_proxy(self):
        """Bad proxy settings."""
        with self.assertRaises(TypeError):
            Isogeo(
                client_id=app_id,
                client_secret=app_token,
                proxy="this_is_my_string_proxy",
            )

    def test_successed_auth_prod(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(client_id=app_id, client_secret=app_token)
        bearer = isogeo.connect()
        self.assertIsInstance(bearer, dict)
        self.assertEqual(len(bearer), 4)

        # close
        isogeo.close()

    def test_successed_auth_qa(self):
        """Try to connect to QA platform."""
        isogeo = Isogeo(client_id=app_id, client_secret=app_token, platform="qa")
        bearer = isogeo.connect()
        self.assertIsInstance(bearer, dict)
        self.assertEqual(len(bearer), 4)

        # close
        isogeo.close()


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    unittest.main()
