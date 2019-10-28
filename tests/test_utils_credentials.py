# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python python -m unittest tests.test_utils_credentials ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import unittest
import urllib3
from os import environ, path
from pathlib import Path
from socket import gethostname
from sys import exit

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import IsogeoUtils

# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# #############################################################################
# ########## Classes ###############
# ##################################


class TestIsogeoUtilsCredentials(unittest.TestCase):
    """Test utils for credentials loading."""

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
        """Fixtures prepared before each test."""
        self.utils = IsogeoUtils()

        # credentials
        self.credentials_group_json = [
            # without scopes
            path.normpath(r"tests/fixtures/client_secrets_group_old.json"),
            # with scopes, kind, type and staff
            path.normpath(r"tests/fixtures/client_secrets_group_new.json"),
            # qa with scopes, kind, type and staff
            path.normpath(r"tests/fixtures/client_secrets_group_new_qa.json"),
        ]
        self.credentials_user_json = [
            path.normpath(
                r"tests/fixtures/client_secrets_user_old.json"
            ),  # without scopes
            path.normpath(
                r"tests/fixtures/client_secrets_user_new.json"
            ),  # with scopes
        ]
        self.credentials_user_bad_json = path.normpath(
            r"tests/fixtures/client_secrets_user_bad.json"
        )
        self.credentials_ini = path.normpath(r"tests/fixtures/client_secrets.ini")
        self.credentials_ini_bad = path.normpath(
            r"tests/fixtures/client_secrets_bad.ini"
        )
        self.credentials_group_txt = path.normpath(
            r"tests/fixtures/client_secrets_group.txt"
        )

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- Credentials loader -------------------------------------
    def test_credentials_loader_json_user(self):
        """Test credentials loader for an user application from a JSON file."""
        for in_creds_json_user in self.credentials_user_json:
            creds_json_user = self.utils.credentials_loader(in_creds_json_user)
            # structure
            self.assertIsInstance(creds_json_user, dict)
            self.assertIn("auth_mode", creds_json_user)
            self.assertIn("client_id", creds_json_user)
            self.assertIn("client_secret", creds_json_user)
            self.assertIn("scopes", creds_json_user)
            self.assertIn("uri_auth", creds_json_user)
            self.assertIn("uri_base", creds_json_user)
            self.assertIn("uri_token", creds_json_user)
            self.assertIn("uri_redirect", creds_json_user)
            self.assertIn("kind", creds_json_user)
            self.assertIn("type", creds_json_user)
            self.assertIn("staff", creds_json_user)
            # values
            self.assertEqual(creds_json_user.get("auth_mode"), "user")
            self.assertEqual(
                creds_json_user.get("uri_auth"),
                "https://id.api.isogeo.com/oauth/authorize",
            )
            self.assertEqual(creds_json_user.get("uri_base"), "https://api.isogeo.com")
            self.assertEqual(
                creds_json_user.get("uri_token"),
                "https://id.api.isogeo.com/oauth/token",
            )
            self.assertIsInstance(creds_json_user.get("uri_redirect"), list)

    def test_credentials_loader_json_group(self):
        """Test credentials loader for an group application from a JSON
        file."""
        for in_creds_json_group in self.credentials_group_json:
            creds_json_group = self.utils.credentials_loader(in_creds_json_group)
            # structure
            self.assertIsInstance(creds_json_group, dict)
            self.assertIn("auth_mode", creds_json_group)
            self.assertIn("client_id", creds_json_group)
            self.assertIn("client_secret", creds_json_group)
            self.assertIn("scopes", creds_json_group)
            self.assertIn("uri_auth", creds_json_group)
            self.assertIn("uri_base", creds_json_group)
            self.assertIn("uri_token", creds_json_group)
            self.assertIn("uri_redirect", creds_json_group)
            self.assertIn("kind", creds_json_group)
            self.assertIn("type", creds_json_group)
            self.assertIn("staff", creds_json_group)
            self.assertIn("platform", creds_json_group)
            # values
            self.assertEqual(creds_json_group.get("auth_mode"), "group")
            self.assertIsNone(creds_json_group.get("uri_redirect"))

            if creds_json_group.get("platform") == "prod":
                self.assertEqual(
                    creds_json_group.get("uri_auth"),
                    "https://id.api.isogeo.com/oauth/authorize",
                )
                self.assertEqual(
                    creds_json_group.get("uri_token"),
                    "https://id.api.isogeo.com/oauth/token",
                )
                self.assertEqual(
                    creds_json_group.get("uri_base"), "https://api.isogeo.com"
                )
            elif creds_json_group.get("platform") == "qa":
                self.assertEqual(
                    creds_json_group.get("uri_auth"),
                    "https://id.api.qa.isogeo.com/oauth/authorize",
                )
                self.assertEqual(
                    creds_json_group.get("uri_token"),
                    "https://id.api.qa.isogeo.com/oauth/token",
                )
                self.assertEqual(
                    creds_json_group.get("uri_base"), "https://api.qa.isogeo.com"
                )

    def test_credentials_loader_ini(self):
        """Test credentials loader for an group application from an INI
        file."""
        creds_ini = self.utils.credentials_loader(self.credentials_ini)
        # structure
        self.assertIsInstance(creds_ini, dict)
        self.assertIn("auth_mode", creds_ini)
        self.assertIn("client_id", creds_ini)
        self.assertIn("client_secret", creds_ini)
        self.assertIn("uri_auth", creds_ini)
        self.assertIn("uri_base", creds_ini)
        self.assertIn("uri_token", creds_ini)
        self.assertIn("uri_redirect", creds_ini)
        # values
        self.assertEqual(creds_ini.get("auth_mode"), "group")
        self.assertEqual(
            creds_ini.get("uri_auth"), "https://id.api.isogeo.com/oauth/authorize"
        )
        self.assertEqual(creds_ini.get("uri_base"), "https://api.isogeo.com")
        self.assertEqual(
            creds_ini.get("uri_token"), "https://id.api.isogeo.com/oauth/token"
        )

    def test_credentials_loader_bad_file_path(self):
        """Raise error if credentials file is not reachable."""
        with self.assertRaises(IOError):
            self.utils.credentials_loader(in_credentials=r"imaginary_file.json")

    def test_credentials_loader_bad_file_extension(self):
        """Raise error if extension is not one of accepted ones."""
        with self.assertRaises(ValueError):
            self.utils.credentials_loader(in_credentials=self.credentials_group_txt)

    def test_credentials_loader_bad_file_structure(self):
        """Raise error if file structure is not good."""
        with self.assertRaises(ValueError):
            self.utils.credentials_loader(in_credentials=self.credentials_user_bad_json)
        with self.assertRaises(ValueError):
            self.utils.credentials_loader(in_credentials=self.credentials_ini_bad)
