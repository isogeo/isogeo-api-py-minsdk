# -*- coding: UTF-8 -*-
#! python3  # noqa E265


"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_translator
# for specific
python -m unittest tests.test_translator.TestIsogeoTranslator.test_translation_fr
```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import unittest
from os import environ
from pathlib import Path
from sys import exit
from time import sleep

# 3rd party
from dotenv import load_dotenv
import urllib3

# module target
from isogeo_pysdk import Isogeo, IsogeoTranslator

# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# API access
METADATA_TEST_FIXTURE_UUID = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE")

li_contacts_fr = (
    "Auteur",
    "Point de contact",
    "Administrateur",
    "Distributeur",
    "Créateur",
    "Propriétaire",
    "Analyste principal",
    "Responsable du traitement",
    "Éditeur (publication)",
    "Fournisseur",
    "Utilisateur",
)

li_contacts_en = (
    "Author",
    "Point of contact",
    "Custodian",
    "Distributor",
    "Originator",
    "Owner",
    "Principal investigator",
    "Processor",
    "Publisher",
    "Resource provider",
    "User",
)

# #############################################################################
# ########## Classes ###############
# ##################################


class TestIsogeoTranslator(unittest.TestCase):
    """Test translation of specific words wihtin Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_GROUP_CLIENT_ID") or not environ.get(
            "ISOGEO_API_GROUP_CLIENT_SECRET"
        ):
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

        # API connection
        cls.isogeo = Isogeo(
            auth_mode="group",
            client_id=environ.get("ISOGEO_API_GROUP_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_GROUP_CLIENT_SECRET"),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )
        # getting a token
        cls.isogeo.connect()

        # get contacts on a metadata
        cls.md_contacts = cls.isogeo.metadata.get(
            metadata_id=METADATA_TEST_FIXTURE_UUID, include=("contacts",)
        )
        cls.li_contacts_roles = [i.get("role") for i in cls.md_contacts.contacts]

    # standard methods
    def setUp(self):
        """Executed before each test."""

    def tearDown(self):
        """Executed after each test."""
        sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # tests
    def test_translation_fr(self):
        """Some French translations get from the subclass."""
        tr = IsogeoTranslator("FR")
        # contacts roles
        for role in self.li_contacts_roles:
            self.assertIn(tr.tr("roles", role), li_contacts_fr)

    def test_translation_en(self):
        """Some English translations get from the subclass."""
        tr = IsogeoTranslator("EN")
        # contacts roles
        for role in self.li_contacts_roles:
            self.assertIn(tr.tr("roles", role), li_contacts_en)

    def test_translation_bad(self):
        """Test translation of inexistent word.."""
        tr = IsogeoTranslator("EN")
        with self.assertRaises(ValueError):
            for role in self.li_contacts_roles:
                self.assertIn(tr.tr("BAD_SUBDOMAIN", role), li_contacts_en)


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    unittest.main()
