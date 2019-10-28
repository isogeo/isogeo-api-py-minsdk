# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

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
import logging
import unittest
import urllib3
from os import environ
from pathlib import Path
from socket import gethostname
from sys import exit

# 3rd party
from dotenv import load_dotenv

# Isogeo
from isogeo_pysdk import Isogeo, IsogeoChecker

# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

checker = IsogeoChecker()

# #############################################################################
# ######## Classes #################
# ##################################


class TestAuthentication(unittest.TestCase):
    """Test authentication process."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID") or not environ.get(
            "ISOGEO_API_USER_LEGACY_CLIENT_SECRET"
        ):
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

        # API credentials settings
        cls.client_id = environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID")
        cls.client_secret = environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET")

    # standard methods
    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # close sessions
        pass

    # -- TESTS ---------------------------------------------------------
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
        with self.assertRaises(ValueError):
            isogeo = Isogeo(
                client_id=self.client_id[:-2], client_secret=self.client_secret
            )
            isogeo.connect()

    def test_other_language(self):
        """Try to get other language."""
        isogeo = Isogeo(
            client_id=self.client_id, client_secret=self.client_secret, lang="ES"
        )
        # if other language passed the English is applied
        self.assertEqual(isogeo.lang, "en")

        # close
        isogeo.close()

    def test_bad_platform(self):
        """Bad platform value."""
        with self.assertRaises(ValueError):
            isogeo = Isogeo(
                client_id=self.client_id,
                client_secret=self.client_secret,
                platform="skynet",
            )
            del isogeo

    def test_bad_auth_mode(self):
        """Bad auth mode value."""
        with self.assertRaises(ValueError):
            isogeo = Isogeo(
                client_id=self.client_id,
                client_secret=self.client_secret,
                auth_mode="fingerprint",
            )
            del isogeo

    # Proxy management
    def test_proxy(self):
        """Simulate proxy settings assignment."""
        isogeo = Isogeo(
            client_id=self.client_id,
            client_secret=self.client_secret,
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
                client_id=self.client_id,
                client_secret=self.client_secret,
                proxy="this_is_my_string_proxy",
            )

    def test_successed_auth_legacy_prod(self):
        """When a search works, check the response structure."""
        isogeo = Isogeo(
            auth_mode="user_legacy",
            client_id=self.client_id,
            client_secret=self.client_secret,
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform="qa",
        )
        isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )
        self.assertIsInstance(isogeo.token, dict)
        self.assertEqual(len(isogeo.token), 5)

        # close
        isogeo.close()

    def test_successed_auth_legacy_qa(self):
        """Try to connect to QA platform."""
        isogeo = Isogeo(
            auth_mode="user_legacy",
            client_id=self.client_id,
            client_secret=self.client_secret,
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform="qa",
        )
        isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )
        self.assertIsInstance(isogeo.token, dict)
        self.assertEqual(len(isogeo.token), 5)

        # close
        isogeo.close()


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    unittest.main()
