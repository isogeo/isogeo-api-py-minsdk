# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_workgroups
    # for specific
    python -m unittest tests.test_workgroups.TestWorkgroups.test_workgroups_create
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from socket import gethostname
from sys import exit
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv
from oauthlib.oauth2 import LegacyApplicationClient

# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Contact, Workgroup


# #############################################################################
# ######## Globals #################
# ##################################

load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
app_script_id = environ.get("ISOGEO_API_USER_CLIENT_ID")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
user_email = environ.get("ISOGEO_USER_NAME")
user_password = environ.get("ISOGEO_USER_PASSWORD")
workgroup_test = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestWorkgroups(unittest.TestCase):
    """Test Workgroup model of Isogeo API."""

    if not app_script_id or not app_script_secret:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(hostname, strftime("%Y-%m-%d_%H%M%S", gmtime()))
        self.li_workgroups_to_delete = []
        # API connection
        self.isogeo = IsogeoSession(
            client=LegacyApplicationClient(client_id=app_script_id),
            auto_refresh_url="https://id.api.isogeo.com/oauth/token",
            client_secret=app_script_secret,
        )

        # getting a token
        self.isogeo.connect(username=user_email, password=user_password)

    def tearDown(self):
        """Executed after each test."""
        # clean created workgroups
        if len(self.li_workgroups_to_delete):
            for i in self.li_workgroups_to_delete:
                self.isogeo.workgroup_delete(workgroup_id=workgroup_test)
        # close sessions
        self.isogeo.close()

    # -- ALL APPS ------------------------------------------------------------
    def test_workgroups_create_basic(self):
        """POST :groups/}"""
        # to create a workgroup, a contact is required
        contact_owner = Contact(name="TEST_UNIT_AUTO {}".format(self.discriminator),
                                email="test@isogeo.com")
        wg = Workgroup(contact=contact_owner)
        new_wg = self.isogeo.workgroup_create(workgroup=wg)

        # checks
        self.assertEqual(new_wg.contact.get("name"), "TEST_UNIT_AUTO {}".format(self.discriminator))
        # self.assertTrue(self.isogeo.workgroup_exists(new_wg.get("_id")))

        # add created workgroup to deletion
        self.li_workgroups_to_delete.append(new_wg._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
