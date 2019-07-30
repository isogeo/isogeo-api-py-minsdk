# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_catalogs
    # for specific
    python -m unittest tests.test_catalogs.TestCatalogs.test_catalogs_create_basic
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
from isogeo_pysdk import Catalog, IsogeoSession, Share
from isogeo_pysdk import __version__ as pysdk_version
from isogeo_pysdk.enums import CatalogStatisticsTags

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
    """Returns the function name"""
    return "TEST_PySDK - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestCatalogs(unittest.TestCase):
    """Test Catalog model of Isogeo API."""

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

        # class vars and attributes
        cls.li_fixtures_to_delete = []

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
                cls.isogeo.catalog.delete(
                    workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, catalog_id=i
                )
                pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_catalogs_create_basic(self):
        """POST :groups/{workgroup_uuid}/catalogs/}"""
        # var
        catalog_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        catalog_new = Catalog(name=catalog_name)

        # create it online
        catalog_new = self.isogeo.catalog.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            catalog=catalog_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(catalog_new.name, catalog_name)
        self.assertTrue(
            self.isogeo.catalog.exists(catalog_new.owner.get("_id"), catalog_new._id)
        )

        # add created catalog to deletion
        self.li_fixtures_to_delete.append(catalog_new._id)

    def test_catalogs_create_complete(self):
        """POST :groups/{workgroup_uuid}/catalogs/}"""
        # populate model object locally
        catalog_new = Catalog(
            name="{} - {}".format(get_test_marker(), self.discriminator), scan=True
        )
        # create it online
        catalog_new = self.isogeo.catalog.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            catalog=catalog_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(
            catalog_new.name, "{} - {}".format(get_test_marker(), self.discriminator)
        )
        self.assertTrue(
            self.isogeo.catalog.exists(catalog_new.owner.get("_id"), catalog_new._id)
        )

        # add created catalog to deletion
        self.li_fixtures_to_delete.append(catalog_new._id)

    def test_catalogs_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/catalogs/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        catalog_local = Catalog(name=name_to_be_unique)

        # create it online
        catalog_new_1 = self.isogeo.catalog.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            catalog=catalog_local,
            check_exists=0,
        )

        # try to create a catalog with the same name
        catalog_new_2 = self.isogeo.catalog.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            catalog=catalog_local,
            check_exists=1,
        )

        # check if object has not been created
        self.assertEqual(catalog_new_2, False)

        # add created catalog to deletion
        self.li_fixtures_to_delete.append(catalog_new_1._id)

    # -- GET --
    def test_catalogs_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/catalogs}"""
        # retrieve workgroup catalogs
        wg_catalogs = self.isogeo.catalog.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
        )
        # parse and test object loader
        for i in wg_catalogs:
            # handle bad json attribute
            i["scan"] = i.pop("$scan")
            # load it
            catalog = Catalog(**i)
            # tests attributes structure
            self.assertTrue(hasattr(catalog, "_abilities"))
            self.assertTrue(hasattr(catalog, "_created"))
            self.assertTrue(hasattr(catalog, "_id"))
            self.assertTrue(hasattr(catalog, "_modified"))
            self.assertTrue(hasattr(catalog, "_tag"))
            self.assertTrue(hasattr(catalog, "code"))
            self.assertTrue(hasattr(catalog, "count"))
            self.assertTrue(hasattr(catalog, "name"))
            self.assertTrue(hasattr(catalog, "owner"))
            self.assertTrue(hasattr(catalog, "scan"))
            # tests attributes value
            self.assertEqual(catalog._created, i.get("_created"))
            self.assertEqual(catalog._id, i.get("_id"))
            self.assertEqual(catalog._modified, i.get("_modified"))
            self.assertEqual(catalog._tag, i.get("_tag"))
            self.assertEqual(catalog.code, i.get("code"))
            self.assertEqual(catalog.count, i.get("count"))
            self.assertEqual(catalog.name, i.get("name"))

    def test_catalog_shares(self):
        """GET :catalogs/{catalog_uuid}/shares"""
        # pick a random catalog
        wg_catalogs = self.isogeo.catalog.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
        )
        catalog_id = sample(wg_catalogs, 1)[0].get("_id")
        # retrieve shares
        catalog_shares = self.isogeo.catalog.shares(catalog_id)
        # check container
        self.assertIsInstance(catalog_shares, list)
        # check content
        if len(catalog_shares):
            for i in catalog_shares:
                Share(**i)

    def test_catalog_statistics(self):
        """GET :catalogs/{catalog_uuid}/statistics"""
        wg_catalogs = self.isogeo.catalog.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
        )
        catalog_id = sample(wg_catalogs, 1)[0].get("_id")
        # get
        catalog_statistics = self.isogeo.catalog.statistics(catalog_id)
        # check
        self.assertIsInstance(catalog_statistics, dict)

    def test_catalog_statistics_tag(self):
        """GET :catalogs/{catalog_uuid}/statistics/tag/{tag_name}"""
        wg_catalogs = self.isogeo.catalog.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
        )
        catalog_id = sample(wg_catalogs, 1)[0].get("_id")
        # get
        for i in CatalogStatisticsTags:
            catalog_statistics_tag = self.isogeo.catalog.statistics_by_tag(
                catalog_id, i.value
            )
            # check
            self.assertIsInstance(catalog_statistics_tag, (list, tuple))

        # test bad tag
        with self.assertRaises(ValueError):
            self.isogeo.catalog.statistics_by_tag(catalog_id, "coordinateSystem")
            self.isogeo.catalog.statistics_by_tag(catalog_id, "catalog")

    # -- PUT/PATCH --
    def test_catalogs_update(self):
        """PUT :groups/{workgroup_uuid}/catalogs/{catalog_uuid}}"""
        # create a new catalog
        catalog_fixture = Catalog(name="{}".format(get_test_marker()))
        catalog_fixture = self.isogeo.catalog.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            catalog=catalog_fixture,
            check_exists=0,
        )

        # modify local object
        catalog_fixture.name = "{} - {}".format(get_test_marker(), self.discriminator)
        catalog_fixture.scan = True

        # update the online catalog
        catalog_fixture = self.isogeo.catalog.update(catalog_fixture)

        # check if the change is effective
        catalog_fixture_updated = self.isogeo.catalog.get(
            catalog_fixture.owner.get("_id"), catalog_fixture._id
        )
        self.assertEqual(
            catalog_fixture_updated.name,
            "{} - {}".format(get_test_marker(), self.discriminator),
        )
        self.assertEqual(catalog_fixture_updated.scan, True)

        # add created catalog to deletion
        self.li_fixtures_to_delete.append(catalog_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
