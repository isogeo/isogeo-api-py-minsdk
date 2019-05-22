# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_workgroups
    # for specific
    python -m unittest tests.test_workgroups.TestWorkgroups.test_workgroups_create_basic
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from pathlib import Path
from random import sample
from socket import gethostname
from sys import exit, _getframe
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

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
app_script_id = environ.get("ISOGEO_API_USER_CLIENT_ID")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
platform = environ.get("ISOGEO_PLATFORM", "qa")
user_email = environ.get("ISOGEO_USER_NAME")
user_password = environ.get("ISOGEO_USER_PASSWORD")
workgroup_test = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_UNIT_PythonSDK - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################
class TestWorkgroups(unittest.TestCase):
    """Test Workgroup model of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_USER_CLIENT_ID") or not environ.get(
            "ISOGEO_API_USER_CLIENT_SECRET"
        ):
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass
        logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        # API connection
        cls.isogeo = IsogeoSession(
            client=LegacyApplicationClient(
                client_id=environ.get("ISOGEO_API_USER_CLIENT_ID")
            ),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            client_secret=app_script_secret,
            platform=platform,
        )
        # getting a token
        cls.isogeo.connect(username=user_email, password=user_password)

    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(
            hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
        )

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created workgroups
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.workgroup.workgroup_delete(workgroup_id=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_workgroups_create_basic(self):
        """POST :groups/}"""
        # var
        workgroup_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        contact_owner = Contact(
            name=workgroup_name, email="test@isogeo.com"
        )  # to create a workgroup, a contact is required
        workgroup = Workgroup(contact=contact_owner)
        # create it online
        new_workgroup = self.isogeo.workgroup.workgroup_create(workgroup=workgroup)

        # checks
        self.assertEqual(new_workgroup.contact.get("name"), workgroup_name)

        self.assertTrue(self.isogeo.workgroup.workgroup_exists(new_workgroup._id))

        # add created workgroup to deletion
        self.li_fixtures_to_delete.append(new_workgroup._id)

    # def test_workgroups_create_complete(self):
    #     """POST :groups/}"""
    #     # to create a workgroup, a contact is required
    #     existing_wg = Workgroup(self.isogeo.workgroup(workgroup_id=workgroup_test))
    #     new_wg = self.isogeo.workgroup_create(workgroup=existing_wg)

    #     # checks
    #     self.assertEqual(
    #         new_wg.contact.get("name"), "TEST_UNIT_AUTO {}".format(self.discriminator)
    #     )
    #     # self.assertTrue(self.isogeo.workgroup_exists(new_wg.get("_id")))

    #     # add created workgroup to deletion
    #     # self.li_fixtures_to_delete.append(new_wg._id)

    def test_workgroups_create_checking_name(self):
        """POST :groups/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        contact_owner = Contact(
            name=name_to_be_unique
        )  # to create a workgroup, a contact is required
        workgroup_local = Workgroup(contact=contact_owner)

        # create it online
        workgroup_new_1 = self.isogeo.workgroup.workgroup_create(
            workgroup=workgroup_local, check_exists=0
        )

        # try to create a workgroup with the same name
        workgroup_new_2 = self.isogeo.workgroup.workgroup_create(
            workgroup=workgroup_local, check_exists=1
        )

        # check if object has not been created
        self.assertEqual(workgroup_new_2, False)

        # add created workgroup to deletion
        self.li_fixtures_to_delete.append(workgroup_new_1._id)

    # -- GET --
    def test_workgroups_listing_global(self):
        """GET :groups/"""
        # retrieve workgroup workgroups
        wg_workgroups = self.isogeo.workgroup.workgroups(caching=1)
        self.assertIsInstance(wg_workgroups, list)
        # parse and test object loader
        for i in wg_workgroups:
            workgroup = Workgroup(**i)
            # tests attributes structure
            self.assertTrue(hasattr(workgroup, "_abilities"))
            self.assertTrue(hasattr(workgroup, "_created"))
            self.assertTrue(hasattr(workgroup, "_id"))
            self.assertTrue(hasattr(workgroup, "_modified"))
            self.assertTrue(hasattr(workgroup, "_tag"))
            self.assertTrue(hasattr(workgroup, "areKeywordsRestricted"))
            self.assertTrue(hasattr(workgroup, "canCreateLegacyServiceLinks"))
            self.assertTrue(hasattr(workgroup, "canCreateMetadata"))
            self.assertTrue(hasattr(workgroup, "code"))
            self.assertTrue(hasattr(workgroup, "contact"))
            self.assertTrue(hasattr(workgroup, "hasCswClient"))
            self.assertTrue(hasattr(workgroup, "limits"))
            self.assertTrue(hasattr(workgroup, "keywordsCasing"))
            self.assertTrue(hasattr(workgroup, "metadataLanguage"))
            self.assertTrue(hasattr(workgroup, "themeColor"))
            # tests attributes value

    def test_workgroup_detailed(self):
        """GET :groups/{workgroup_uuid}"""
        # retrieve workgroups
        if self.isogeo._workgroups_names:
            workgroups = self.isogeo._workgroups_names
        else:
            workgroups = self.isogeo.workgroup.workgroups(caching=0)

        # pick one workgroup
        workgroup_id = sample(workgroups, 1)[0]

        # check both exist
        self.assertTrue(self.isogeo.workgroup.workgroup_exists(workgroup_id.get("_id")))

        # get and check both
        workgroup = self.isogeo.workgroup.workgroup(workgroup_id.get("_id"))

        self.assertIsInstance(workgroup, Workgroup)

    def test_workgroup_statistics(self):
        """GET :groups/{workgroup_uuid}/statistics"""
        # get
        workgroup_statistics = self.isogeo.workgroup.statistics(workgroup_test)
        # check
        self.assertIsInstance(workgroup_statistics, dict)
        self.assertEqual(len(workgroup_statistics), 12)

    # -- PUT/PATCH --
    # def test_workgroups_update(self):
    #     """PUT :groups/{workgroup_uuid}"""
    #     # create local object
    #     contact_owner = Contact(
    #         name=get_test_marker()
    #     )  # to create a workgroup, a contact is required
    #     workgroup_local = Workgroup(contact=contact_owner)

    #     workgroup_fixture = self.isogeo.workgroup.workgroup_create(
    #         workgroup=workgroup_local,
    #         check_exists=0,
    #     )

    #     # modify local object
    #     workgroup_fixture.contact["name"] = "{} - {}".format(
    #         get_test_marker(), self.discriminator
    #     )

    #     # update the online workgroup
    #     workgroup_fixture = self.isogeo.workgroup.workgroup_update(
    #         workgroup_fixture
    #     )

    #     # check if the change is effective
    #     workgroup_fixture_updated = self.isogeo.workgroup.workgroup(
    #         workgroup_fixture._id
    #     )
    #     self.assertEqual(
    #         workgroup_fixture_updated.contact.get("name"),
    #         "{} - {}".format(get_test_marker(), self.discriminator),
    #     )

    #     # add created workgroup to deletion
    #     self.li_fixtures_to_delete.append(workgroup_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
