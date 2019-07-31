# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_limitations
    # for specific
    python -m unittest tests.test_limitations.TestLimitations.test_limitations_create_basic
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
from isogeo_pysdk import (
    IsogeoSession,
    __version__ as pysdk_version,
    Limitation,
    Metadata,
)


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
    return "TEST_PySDK - Limitations {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestLimitations(unittest.TestCase):
    """Test Limitation model of Isogeo API."""

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

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

        # API connection
        cls.isogeo = IsogeoSession(
            client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )
        # getting a token
        cls.isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.metadata_fixture_created = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md, check_exists=0
        )
        cls.metadata_fixture_existing = cls.isogeo.metadata.get(
            metadata_id=METADATA_TEST_FIXTURE_UUID
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
        # clean created metadata
        cls.isogeo.metadata.delete(cls.metadata_fixture_created._id)
        # clean created limitations
        # if len(cls.li_fixtures_to_delete):
        #     for i in cls.li_fixtures_to_delete:
        #         cls.isogeo.metadata.limitations.delete(limitation=i)
        #         pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    # def test_limitations_create_basic(self):
    #     """POST :groups/{workgroup_uuid}/limitations/}"""
    #     # var
    #     limitation_date = strftime("%Y-%m-%d", gmtime())
    #     limitation_kind_creation = "creation"
    #     limitation_kind_update = "update"
    #     limitation_description = "{} - {}".format(get_test_marker(), self.discriminator)

    #     # create object locally
    #     limitation_new_creation = Limitation(
    #         date=limitation_date,
    #         kind=limitation_kind_creation,
    #         description=limitation_description,
    #         parent_resource=self.metadata_fixture_created._id,
    #     )
    #     limitation_new_update = Limitation(
    #         date=limitation_date,
    #         kind=limitation_kind_update,
    #         description=limitation_description,
    #         parent_resource=self.metadata_fixture_created._id,
    #     )

    #     # create it online
    #     limitation_new_creation = self.isogeo.metadata.limitations.create(
    #         metadata=self.metadata_fixture_created, limitation=limitation_new_creation
    #     )
    #     limitation_new_update = self.isogeo.metadata.limitations.create(
    #         metadata=self.metadata_fixture_created, limitation=limitation_new_update
    #     )

    #     # checks
    #     self.assertEqual(limitation_new_creation.kind, limitation_kind_creation)
    #     self.assertEqual(limitation_new_update.kind, limitation_kind_update)
    #     self.assertEqual(limitation_new_creation.description, None)
    #     self.assertEqual(limitation_new_update.description, limitation_description)

    # def test_limitations_create_checking_name(self):
    #     """POST :groups/{workgroup_uuid}/limitations/}"""
    #     # vars
    #     name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

    #     # create local object
    #     limitation_local = Limitation(name=name_to_be_unique)

    #     # create it online
    #     limitation_new_1 = self.isogeo.limitation.limitation_create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, limitation=limitation_local, check_exists=0
    #     )

    #     # try to create a limitation with the same name
    #     limitation_new_2 = self.isogeo.limitation.limitation_create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, limitation=limitation_local, check_exists=1
    #     )

    #     # check if object has not been created
    #     self.assertEqual(limitation_new_2, False)

    #     # add created limitation to deletion
    #     self.li_fixtures_to_delete.append(limitation_new_1._id)

    # -- GET --
    def test_limitations_listing(self):
        """GET :resources/{metadata_uuid}/limitations/}"""
        # retrieve workgroup limitations
        md_limitations = self.isogeo.metadata.limitations.listing(
            self.metadata_fixture_existing
        )
        # parse and test object loader
        for i in md_limitations:
            # load it
            limitation = Limitation(**i)
            # tests attributes structure
            self.assertTrue(hasattr(limitation, "_id"))
            self.assertTrue(hasattr(limitation, "description"))
            self.assertTrue(hasattr(limitation, "directive"))
            self.assertTrue(hasattr(limitation, "type"))

            # tests attributes value
            self.assertEqual(limitation._id, i.get("_id"))
            self.assertEqual(limitation.directive, i.get("directive"))
            self.assertEqual(limitation.type, i.get("type"))

    def test_limitation_detailed(self):
        """GET :resources/{metadata_uuid}/limitations/{limitation_uuid}"""
        # retrieve limitation
        md_limitations = self.isogeo.metadata.limitations.listing(
            self.metadata_fixture_existing
        )
        # pick one randomly
        random_limitation = sample(md_limitations, 1)[0]
        # get
        online_limitation = self.isogeo.metadata.limitations.get(
            metadata_id=self.metadata_fixture_existing._id,
            limitation_id=random_limitation.get("_id"),
        )
        # check
        self.assertIsInstance(online_limitation, Limitation)

    # -- PUT/PATCH --
    # def test_limitations_update(self):
    #     """PUT :groups/{workgroup_uuid}/limitations/{limitation_uuid}}"""
    #     # create a new limitation
    #     limitation_fixture = Limitation(name="{}".format(get_test_marker()))
    #     limitation_fixture = self.isogeo.limitation.limitation_create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, limitation=limitation_fixture, check_exists=0
    #     )

    #     # modify local object
    #     limitation_fixture.name = "{} - {}".format(get_test_marker(), self.discriminator)
    #     limitation_fixture.scan = True

    #     # update the online limitation
    #     limitation_fixture = self.isogeo.limitation.limitation_update(limitation_fixture)

    #     # check if the change is effective
    #     limitation_fixture_updated = self.isogeo.limitation.limitation(
    #         limitation_fixture.owner.get("_id"), limitation_fixture._id
    #     )
    #     self.assertEqual(
    #         limitation_fixture_updated.name,
    #         "{} - {}".format(get_test_marker(), self.discriminator),
    #     )
    #     self.assertEqual(limitation_fixture_updated.scan, True)

    #     # add created limitation to deletion
    #     self.li_fixtures_to_delete.append(limitation_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
