# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_contacts
    # for specific
    python -m unittest tests.test_contacts.TestContacts.test_contacts_create
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from sys import exit
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv
from oauthlib.oauth2 import LegacyApplicationClient

# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Contact


# #############################################################################
# ######## Globals #################
# ##################################

load_dotenv("dev.env", override=True)

# API access
app_script_id = environ.get("ISOGEO_API_USER_CLIENT_ID")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
user_email = environ.get("ISOGEO_USER_NAME")
user_password = environ.get("ISOGEO_USER_PASSWORD")
workgroup_test = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestContacts(unittest.TestCase):
    """Test search to Isogeo API."""

    if not app_script_id or not app_script_secret:
        logging.critical("No API credentials set as env variables.")
        print(environ.keys())
        exit()
    else:
        pass
    logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.datestamp = strftime("%Y-%m-%d_%H%M%S", gmtime())
        self.li_contacts_to_delete = []
        # API connection
        self.isogeo = IsogeoSession(
            client=LegacyApplicationClient(client_id=app_script_id),
            auto_refresh_url="https://id.api.isogeo.com/oauth/token",
            client_secret=app_script_secret,
        )

        # getting a token
        self.token = self.isogeo.connect(username=user_email, password=user_password)

    def tearDown(self):
        """Executed after each test."""
        # clean created contacts
        if len(self.li_contacts_to_delete):
            for i in self.li_contacts_to_delete:
                self.isogeo.contact_delete(workgroup_id=workgroup_test, contact_id=i)
        # close sessions
        self.isogeo.close()

    # -- ALL APPS ------------------------------------------------------------
    def test_contacts_create_basic(self):
        """GET :groups/{workgroup_uuid}/contacts/{contact_uuid}"""
        ct = Contact(name="TEST_UNIT_AUTO {}".format(self.datestamp))
        new_ct = self.isogeo.contact_create(workgroup_id=workgroup_test, contact=ct)

        # checks
        self.assertEqual(new_ct.get("name"), "TEST_UNIT_AUTO {}".format(self.datestamp))
        self.assertTrue(self.isogeo.contact_exists(new_ct.get("_id")))

        # add created contact to deletion
        self.li_contacts_to_delete.append(new_ct.get("_id"))


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
