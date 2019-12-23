# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_datasources
# for specific
python -m unittest tests.test_datasources.TestDatasources.test_datasources_create_basic
```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from pathlib import Path
from socket import gethostname
from sys import exit, _getframe
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import Isogeo, Datasource


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


class TestDatasources(unittest.TestCase):
    """Test Datasource model of Isogeo API."""

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
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.datasource.delete(
                    workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, datasource_id=i
                )
                pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_datasources_create_basic(self):
        """POST :groups/{workgroup_uuid}/datasources/}"""
        # var
        datasource_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        datasource_new = Datasource(
            name=datasource_name,
            location="http://catalogue.geo-ide.developpement-durable.gouv.fr/catalogue/srv/eng/csw-moissonnable-dreal-npdc",
        )

        # create it online
        datasource_new = self.isogeo.datasource.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            datasource=datasource_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(datasource_new.name, datasource_name)
        self.assertTrue(
            self.isogeo.datasource.exists(
                WORKGROUP_TEST_FIXTURE_UUID, datasource_new._id
            )
        )

        # add created datasource to deletion
        self.li_fixtures_to_delete.append(datasource_new._id)

    def test_datasources_create_complete(self):
        """POST :groups/{workgroup_uuid}/datasources/}"""
        # populate model object locally
        datasource_new = Datasource(
            name="{} - {}".format(get_test_marker(), self.discriminator),
            location="https://geobretagne.fr/geonetwork/srv/fre/csw?",
        )
        # create it online
        datasource_new = self.isogeo.datasource.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            datasource=datasource_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(
            datasource_new.name, "{} - {}".format(get_test_marker(), self.discriminator)
        )
        self.assertTrue(
            self.isogeo.datasource.exists(
                WORKGROUP_TEST_FIXTURE_UUID, datasource_new._id
            )
        )

        # add created datasource to deletion
        self.li_fixtures_to_delete.append(datasource_new._id)

    def test_datasources_create_checking_location(self):
        """POST :groups/{workgroup_uuid}/datasources/}"""
        # vars
        location_to_be_unique = "https://geobretagne.fr/geonetwork/srv/fre/csw"

        # create local object
        datasource_local = Datasource(
            name="{} - {}".format(get_test_marker(), self.discriminator),
            location=location_to_be_unique,
        )

        # create it online
        datasource_new_1 = self.isogeo.datasource.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            datasource=datasource_local,
            check_exists=0,
        )

        # try to create a datasource with the same name
        datasource_new_2 = self.isogeo.datasource.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            datasource=datasource_local,
            check_exists=2,
        )

        # check if object has not been created
        self.assertEqual(datasource_new_2, False)

        # add created datasource to deletion
        self.li_fixtures_to_delete.append(datasource_new_1._id)

    def test_datasources_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/datasources/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE NAME"

        # create local object
        datasource_local = Datasource(
            name=name_to_be_unique,
            location="https://geobretagne.fr/geonetwork/srv/fre/csw?",
        )

        # create it online
        datasource_new_1 = self.isogeo.datasource.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            datasource=datasource_local,
            check_exists=0,
        )

        # try to create a datasource with the same name
        datasource_new_2 = self.isogeo.datasource.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            datasource=datasource_local,
            check_exists=1,
        )

        # check if object has not been created
        self.assertEqual(datasource_new_2, False)

        # add created datasource to deletion
        self.li_fixtures_to_delete.append(datasource_new_1._id)

    # -- GET --
    def test_datasources_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/datasources}"""
        # retrieve workgroup datasources
        wg_datasources = self.isogeo.datasource.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=0
        )
        # parse and test object loader
        for i in wg_datasources:
            datasource = Datasource(**i)
            # tests attributes structure
            self.assertTrue(hasattr(datasource, "_created"))
            self.assertTrue(hasattr(datasource, "_id"))
            self.assertTrue(hasattr(datasource, "_modified"))
            self.assertTrue(hasattr(datasource, "_tag"))
            self.assertTrue(hasattr(datasource, "enabled"))
            self.assertTrue(hasattr(datasource, "resourceCount"))
            self.assertTrue(hasattr(datasource, "name"))
            self.assertTrue(hasattr(datasource, "location"))
            self.assertTrue(hasattr(datasource, "lastSession"))
            # tests attributes value
            self.assertEqual(datasource._created, i.get("_created"))
            self.assertEqual(datasource._id, i.get("_id"))
            self.assertEqual(datasource._modified, i.get("_modified"))
            self.assertEqual(datasource._tag, i.get("_tag"))
            self.assertEqual(datasource.enabled, i.get("enabled"))
            self.assertEqual(datasource.location, i.get("location"))
            self.assertEqual(datasource.name, i.get("name"))
            self.assertEqual(datasource.resourceCount, i.get("resourceCount"))

    # -- PUT/PATCH --
    def test_datasources_update(self):
        """PUT :groups/{workgroup_uuid}/datasources/{datasource_uuid}}"""
        # create a new datasource
        datasource_fixture = Datasource(
            name="{}".format(get_test_marker()),
            location="https://geobretagne.fr/geonetwork/srv/fre/csw?",
        )
        datasource_fixture = self.isogeo.datasource.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            datasource=datasource_fixture,
            check_exists=0,
        )

        # modify local object
        datasource_fixture.name = "{} - {}".format(
            get_test_marker(), self.discriminator
        )
        datasource_fixture.location = "http://catalogue.geo-ide.developpement-durable.gouv.fr/catalogue/srv/eng/csw-moissonnable-dreal-npdc"

        # update the online datasource
        datasource_fixture = self.isogeo.datasource.update(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, datasource=datasource_fixture
        )

        # check if the change is effective
        datasource_fixture_updated = self.isogeo.datasource.datasource(
            WORKGROUP_TEST_FIXTURE_UUID, datasource_fixture._id
        )
        self.assertEqual(
            datasource_fixture_updated.name,
            "{} - {}".format(get_test_marker(), self.discriminator),
        )
        # self.assertEqual(datasource_fixture_updated.location, "http://catalogue.geo-ide.developpement-durable.gouv.fr/catalogue/srv/eng/csw-moissonnable-dreal-npdc")

        # add created datasource to deletion
        self.li_fixtures_to_delete.append(datasource_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
