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
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Catalog


# #############################################################################
# ######## Globals #################
# ##################################


if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
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
        logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        # API connection
        cls.isogeo = IsogeoSession(
            client=LegacyApplicationClient(
                client_id=environ.get("ISOGEO_API_USER_CLIENT_ID")
            ),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
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
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                # cls.isogeo.catalog.catalog_delete(workgroup_id=workgroup_test, catalog_id=i)
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
        catalog_new = self.isogeo.catalog.catalog_create(
            workgroup_id=workgroup_test, catalog=catalog_new, check_exists=0
        )

        # checks
        self.assertEqual(catalog_new.name, catalog_name)
        self.assertTrue(
            self.isogeo.catalog.catalog_exists(
                catalog_new.owner.get("_id"), catalog_new._id
            )
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
        catalog_new = self.isogeo.catalog.catalog_create(
            workgroup_id=workgroup_test, catalog=catalog_new, check_exists=0
        )

        # checks
        self.assertEqual(
            catalog_new.name, "{} - {}".format(get_test_marker(), self.discriminator)
        )
        self.assertTrue(
            self.isogeo.catalog.catalog_exists(
                catalog_new.owner.get("_id"), catalog_new._id
            )
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
        catalog_new_1 = self.isogeo.catalog.catalog_create(
            workgroup_id=workgroup_test, catalog=catalog_local, check_exists=0
        )

        # try to create a catalog with the same name
        catalog_new_2 = self.isogeo.catalog.catalog_create(
            workgroup_id=workgroup_test, catalog=catalog_local, check_exists=1
        )

        # check if object has not been created
        self.assertEqual(catalog_new_2, False)

        # add created catalog to deletion
        self.li_fixtures_to_delete.append(catalog_new_1._id)

    # -- GET --
    def test_catalogs_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/catalogs}"""
        # retrieve workgroup catalogs
        wg_catalogs = self.isogeo.workgroup_catalogs(
            workgroup_id=workgroup_test, caching=0
        )
        # parse and test object loader
        for i in wg_catalogs:
            ct = Catalog(**i)
            # tests attributes structure
            self.assertTrue(hasattr(ct, "_abilities"))
            self.assertTrue(hasattr(ct, "_created"))
            self.assertTrue(hasattr(ct, "_id"))
            self.assertTrue(hasattr(ct, "_modified"))
            self.assertTrue(hasattr(ct, "_tag"))
            self.assertTrue(hasattr(ct, "code"))
            self.assertTrue(hasattr(ct, "count"))
            self.assertTrue(hasattr(ct, "name"))
            self.assertTrue(hasattr(ct, "owner"))
            self.assertTrue(hasattr(ct, "scan"))
            # tests attributes value
            self.assertEqual(ct._created, i.get("_created"))
            self.assertEqual(ct._id, i.get("_id"))
            self.assertEqual(ct._modified, i.get("_modified"))
            self.assertEqual(ct._tag, i.get("_tag"))
            self.assertEqual(ct.code, i.get("code"))
            self.assertEqual(ct.count, i.get("count"))
            self.assertEqual(ct.name, i.get("name"))

    # -- PUT/PATCH --
    def test_catalogs_update(self):
        """PUT :groups/{workgroup_uuid}/catalogs/{catalog_uuid}}"""
        # create a new catalog
        catalog_fixture = Catalog(name="{}".format(get_test_marker()))
        catalog_fixture = self.isogeo.catalog.catalog_create(
            workgroup_id=workgroup_test, catalog=catalog_fixture, check_exists=0
        )

        # modify local object
        catalog_fixture.name = "{} - {}".format(get_test_marker(), self.discriminator)
        catalog_fixture.scan = True

        # update the online catalog
        catalog_fixture = self.isogeo.catalog.catalog_update(catalog_fixture)

        # check if the change is effective
        catalog_fixture_updated = self.isogeo.catalog.catalog(
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
