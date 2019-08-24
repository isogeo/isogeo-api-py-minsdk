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
import logging
import unittest
import urllib3
from os import environ
from pathlib import Path
from random import sample
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import Contact, Isogeo, Workgroup

from isogeo_pysdk.enums import WorkgroupStatisticsTags

# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
METADATA_TEST_FIXTURE_UUID = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE")
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_PySDK - {}".format(_getframe(1).f_code.co_name)


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
        if not environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID") or not environ.get(
            "ISOGEO_API_USER_LEGACY_CLIENT_SECRET"
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
            auth_mode="user_legacy",
            client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )
        # getting a token
        cls.isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )

    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(
            hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
        )

    def tearDown(self):
        """Executed after each test."""
        sleep(0.5)
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created workgroups
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.workgroup.delete(workgroup_id=i)
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
        new_workgroup = self.isogeo.workgroup.create(workgroup=workgroup)

        # checks
        self.assertEqual(new_workgroup.contact.get("name"), workgroup_name)

        self.assertTrue(self.isogeo.workgroup.exists(new_workgroup._id))

        # add created workgroup to deletion
        self.li_fixtures_to_delete.append(new_workgroup._id)

    # def test_workgroups_create_complete(self):
    #     """POST :groups/}"""
    #     # to create a workgroup, a contact is required
    #     existing_wg = Workgroup(self.isogeo.workgroup(workgroup_id=WORKGROUP_TEST_FIXTURE_UUID))
    #     new_wg = self.isogeo.create(workgroup=existing_wg)

    #     # checks
    #     self.assertEqual(
    #         new_wg.contact.get("name"), "TEST_UNIT_AUTO {}".format(self.discriminator)
    #     )
    #     # self.assertTrue(self.isogeo.exists(new_wg.get("_id")))

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
        workgroup_new_1 = self.isogeo.workgroup.create(
            workgroup=workgroup_local, check_exists=0
        )

        # try to create a workgroup with the same name
        workgroup_new_2 = self.isogeo.workgroup.create(
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
        wg_workgroups = self.isogeo.workgroup.listing(caching=1)
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
        workgroups = self.isogeo.workgroup.listing(caching=0)

        # pick one workgroup
        workgroup_id = sample(workgroups, 1)[0]

        # check both exist
        self.assertTrue(self.isogeo.workgroup.exists(workgroup_id.get("_id")))

        # get and check both
        workgroup = self.isogeo.workgroup.get(workgroup_id.get("_id"))

        self.assertIsInstance(workgroup, Workgroup)

    def test_workgroup_coordinate_systems(self):
        """GET :groups/{workgroup_uuid}/coordinate-systems"""
        # get
        workgroup_coordinate_systems = self.isogeo.workgroup.coordinate_systems(
            WORKGROUP_TEST_FIXTURE_UUID
        )

        # check
        self.assertIsInstance(workgroup_coordinate_systems, list)

    def test_workgroup_invitations(self):
        """GET :groups/{workgroup_uuid}/invitations"""
        # get
        workgroup_invitations = self.isogeo.workgroup.invitations(
            WORKGROUP_TEST_FIXTURE_UUID
        )
        # check
        self.assertIsInstance(workgroup_invitations, list)

    def test_workgroup_limits(self):
        """GET :groups/{workgroup_uuid}/limits"""
        # get
        workgroup_limits = self.isogeo.workgroup.limits(WORKGROUP_TEST_FIXTURE_UUID)
        # check
        self.assertIsInstance(workgroup_limits, dict)

    def test_workgroup_memberships(self):
        """GET :groups/{workgroup_uuid}/memberships"""
        # get
        workgroup_memberships = self.isogeo.workgroup.memberships(
            WORKGROUP_TEST_FIXTURE_UUID
        )
        # check
        self.assertIsInstance(workgroup_memberships, list)

    def test_workgroup_statistics(self):
        """GET :groups/{workgroup_uuid}/statistics"""
        # get
        workgroup_statistics = self.isogeo.workgroup.statistics(
            WORKGROUP_TEST_FIXTURE_UUID
        )
        # check
        self.assertIsInstance(workgroup_statistics, dict)
        self.assertEqual(len(workgroup_statistics), 12)

    def test_workgroup_statistics_tag(self):
        """GET :groups/{workgroup_uuid}/statistics/tag/{tag_name}"""
        # get
        for i in WorkgroupStatisticsTags:
            workgroup_statistics_tag = self.isogeo.workgroup.statistics_by_tag(
                WORKGROUP_TEST_FIXTURE_UUID, i.value
            )
            # check
            self.assertIsInstance(workgroup_statistics_tag, (list, tuple))

        # test bad tag
        with self.assertRaises(ValueError):
            self.isogeo.workgroup.statistics_by_tag(
                WORKGROUP_TEST_FIXTURE_UUID, "coordinateSystem"
            )

    # -- PUT/PATCH --
    # def test_workgroups_update(self):
    #     """PUT :groups/{workgroup_uuid}"""
    #     # create local object
    #     contact_owner = Contact(
    #         name=get_test_marker()
    #     )  # to create a workgroup, a contact is required
    #     workgroup_local = Workgroup(contact=contact_owner)

    #     workgroup_fixture = self.isogeo.workgroup.create(
    #         workgroup=workgroup_local,
    #         check_exists=0,
    #     )

    #     # modify local object
    #     workgroup_fixture.contact["name"] = "{} - {}".format(
    #         get_test_marker(), self.discriminator
    #     )

    #     # update the online workgroup
    #     workgroup_fixture = self.isogeo.workgroup.update(
    #         workgroup_fixture
    #     )

    #     # check if the change is effective
    #     workgroup_fixture_updated = self.isogeo.workgroup.get(
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
