# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_shares
# for specific
python -m unittest tests.test_shares.TestShares.test_shares_create_basic_application
```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import urllib3
import unittest
from os import environ
from pathlib import Path
from random import sample
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import Isogeo, Share


# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name."""
    return "TEST_PySDK - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestShares(unittest.TestCase):
    """Test Share model of Isogeo API."""

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

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.share.delete(share_id=i)
                pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_shares_create_basic_application(self):
        """POST :groups/{workgroup_uuid}/shares/}"""
        # var
        share_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        share_new = Share(name=share_name, type="application")

        # create it online
        share_new = self.isogeo.share.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, share=share_new, check_exists=0
        )

        # checks
        self.assertEqual(share_new.name, share_name)
        self.assertTrue(self.isogeo.share.exists(share_new._id))

        # add created share to deletion
        self.li_fixtures_to_delete.append(share_new._id)

    def test_shares_create_basic_group(self):
        """POST :groups/{workgroup_uuid}/shares/}"""
        # var
        share_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        share_new = Share(name=share_name, type="group")

        # create it online
        share_new = self.isogeo.share.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, share=share_new, check_exists=0
        )

        # checks
        self.assertEqual(share_new.name, share_name)
        self.assertTrue(self.isogeo.share.exists(share_new._id))

        # add created share to deletion
        self.li_fixtures_to_delete.append(share_new._id)

    # def test_shares_create_complete(self):
    #     """POST :groups/{workgroup_uuid}/shares/}"""
    #     # populate model object locally
    #     share_new = Share(
    #         name="{} - {}".format(get_test_marker(), self.discriminator),
    #         type="application",
    #         catalogs= [
    #             isogeo.catalog.get(workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, "75a6e6b16026410999dc4153f16c7de2")
    #         ]
    #     )
    #     # create it online
    #     share_new = self.isogeo.share.create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, share=share_new, check_exists=0
    #     )

    #     # checks
    #     self.assertEqual(
    #         share_new.name, "{} - {}".format(get_test_marker(), self.discriminator)
    #     )
    #     self.assertTrue(
    #         self.isogeo.share.share_exists(
    #             share_new.owner.get("_id"), share_new._id
    #         )
    #     )

    #     # add created share to deletion
    #     self.li_fixtures_to_delete.append(share_new._id)

    # def test_shares_create_checking_name(self):
    # """POST :groups/{workgroup_uuid}/shares/}"""
    # # vars
    # name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

    # # create local object
    # share_local = Share(name=name_to_be_unique)

    # # create it online
    # share_new_1 = self.isogeo.share.create(
    #     workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, share=share_local, check_exists=0
    # )

    # # try to create a share with the same name
    # share_new_2 = self.isogeo.share.create(
    #     workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, share=share_local, check_exists=1
    # )

    # # check if object has not been created
    # self.assertEqual(share_new_2, False)

    # # add created share to deletion
    # self.li_fixtures_to_delete.append(share_new_1._id)

    # -- GET --
    def test_shares_get_user(self):
        """GET :/shares}"""
        # retrieve workgroup shares
        shares = self.isogeo.share.listing(caching=0)
        # parse and test object loader
        for i in shares[:50]:
            # load it
            share = Share(**i)
            # tests attributes structure
            self.assertTrue(hasattr(share, "_created"))
            self.assertTrue(hasattr(share, "_creator"))
            self.assertTrue(hasattr(share, "_id"))
            self.assertTrue(hasattr(share, "_modified"))
            self.assertTrue(hasattr(share, "applications"))
            self.assertTrue(hasattr(share, "catalogs"))
            self.assertTrue(hasattr(share, "groups"))
            self.assertTrue(hasattr(share, "name"))
            self.assertTrue(hasattr(share, "rights"))
            self.assertTrue(hasattr(share, "type"))
            self.assertTrue(hasattr(share, "urlToken"))
            # tests attributes value
            self.assertEqual(share._created, i.get("_created"))
            self.assertEqual(share._creator, i.get("_creator"))
            self.assertEqual(share._id, i.get("_id"))
            self.assertEqual(share._modified, i.get("_modified"))
            self.assertEqual(share.applications, i.get("applications"))
            self.assertEqual(share.catalogs, i.get("catalogs"))
            self.assertEqual(share.groups, i.get("groups"))
            self.assertEqual(share.name, i.get("name"))
            self.assertEqual(share.rights, i.get("rights"))
            self.assertEqual(share.type, i.get("type"))
            self.assertEqual(share.urlToken, i.get("urlToken"))

    def test_shares_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/shares}"""
        # retrieve workgroup shares
        wg_shares = self.isogeo.share.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=0
        )
        # parse and test object loader
        for i in wg_shares:
            # load it
            share = Share(**i)
            # tests attributes structure
            self.assertTrue(hasattr(share, "_created"))
            self.assertTrue(hasattr(share, "_creator"))
            self.assertTrue(hasattr(share, "_id"))
            self.assertTrue(hasattr(share, "_modified"))
            self.assertTrue(hasattr(share, "applications"))
            self.assertTrue(hasattr(share, "catalogs"))
            self.assertTrue(hasattr(share, "groups"))
            self.assertTrue(hasattr(share, "name"))
            self.assertTrue(hasattr(share, "rights"))
            self.assertTrue(hasattr(share, "type"))
            self.assertTrue(hasattr(share, "urlToken"))
            # tests attributes value
            self.assertEqual(share._created, i.get("_created"))
            self.assertEqual(share._creator, i.get("_creator"))
            self.assertEqual(share._id, i.get("_id"))
            self.assertEqual(share._modified, i.get("_modified"))
            self.assertEqual(share.applications, i.get("applications"))
            self.assertEqual(share.catalogs, i.get("catalogs"))
            self.assertEqual(share.groups, i.get("groups"))
            self.assertEqual(share.name, i.get("name"))
            self.assertEqual(share.rights, i.get("rights"))
            self.assertEqual(share.type, i.get("type"))
            self.assertEqual(share.urlToken, i.get("urlToken"))

    def test_shares_get_detailed_basic(self):
        """GET :groups/{workgroup_uuid}/shares}"""
        # retrieve workgroup shares
        wg_shares = self.isogeo.share.listing(workgroup_id=WORKGROUP_TEST_FIXTURE_UUID)

        # pick a random share
        share_id_app = sample(
            [i for i in wg_shares if i.get("type") == "application"], 1
        )[0].get("_id")
        share_id_group = sample([i for i in wg_shares if i.get("type") == "group"], 1)[
            0
        ].get("_id")

        # get the detailed shares
        share_appli = self.isogeo.share.get(share_id=share_id_app)
        share_group = self.isogeo.share.get(share_id=share_id_group)

        # checks
        for share in (share_appli, share_group):
            self.assertIsInstance(share, Share)
            # tests attributes structure
            self.assertTrue(hasattr(share, "_created"))
            self.assertTrue(hasattr(share, "_creator"))
            self.assertTrue(hasattr(share, "_id"))
            self.assertTrue(hasattr(share, "_modified"))
            self.assertTrue(hasattr(share, "applications"))
            self.assertTrue(hasattr(share, "catalogs"))
            self.assertTrue(hasattr(share, "groups"))
            self.assertTrue(hasattr(share, "name"))
            self.assertTrue(hasattr(share, "rights"))
            self.assertTrue(hasattr(share, "type"))
            self.assertTrue(hasattr(share, "urlToken"))
        # test methods
        self.assertIn("app", share_appli.admin_url(self.isogeo.app_url))
        self.assertIsInstance(
            share_appli.opencatalog_url(self.isogeo.oc_url), (str, None)
        )

        self.assertIn("app", share_group.admin_url(self.isogeo.app_url))
        self.assertFalse(share_group.opencatalog_url(self.isogeo.oc_url))

    # -- PUT/PATCH --
    # def test_shares_update(self):
    #     """PUT :groups/{workgroup_uuid}/shares/{share_uuid}}"""
    #     # create a new share
    #     share_fixture = Share(name="{}".format(get_test_marker()))
    #     share_fixture = self.isogeo.share.create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, share=share_fixture, check_exists=0
    #     )

    #     # modify local object
    #     share_fixture.name = "{} - {}".format(get_test_marker(), self.discriminator)
    #     share_fixture.scan = True

    #     # update the online share
    #     share_fixture = self.isogeo.share.update(share_fixture)

    #     # check if the change is effective
    #     share_fixture_updated = self.isogeo.share.get(
    #         share_fixture.owner.get("_id"), share_fixture._id
    #     )
    #     self.assertEqual(
    #         share_fixture_updated.name,
    #         "{} - {}".format(get_test_marker(), self.discriminator),
    #     )
    #     self.assertEqual(share_fixture_updated.scan, True)

    #     # add created share to deletion
    #     self.li_fixtures_to_delete.append(share_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
