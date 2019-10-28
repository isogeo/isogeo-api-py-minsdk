# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_applications
# for specific
python -m unittest tests.test_applications.TestApplications.test_applications_create_basic
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
from isogeo_pysdk import Application, Isogeo


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


class TestApplications(unittest.TestCase):
    """Test Application model of Isogeo API."""

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
        # clean created applications
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.application.delete(application_id=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- MODEL --
    def test_applications_model(self):
        """Testing the model structure, properties and methods."""
        # var
        application = Application(name="My App to test")
        with self.assertRaises(ValueError):
            application.type = "random"

    # -- POST --
    def test_applications_create_basic(self):
        """POST :applications/}"""
        # var
        application_name = get_test_marker()

        # create local object
        application_to_create = Application(name=application_name)

        # create it online
        application_new = self.isogeo.application.create(
            application=application_to_create, check_exists=0
        )

        # checks
        self.assertEqual(application_new.name, application_name)
        self.assertTrue(self.isogeo.application.exists(application_new._id))

        # add created application to deletion
        self.li_fixtures_to_delete.append(application_new._id)

    def test_applications_create_complete(self):
        """POST :applications/}"""
        # populate model object locally
        application_new = Application(
            name=get_test_marker(), type="user", canHaveManyGroups=True
        )
        # create it online
        application_new = self.isogeo.application.create(
            application=application_new, check_exists=0
        )

        # checks
        self.assertEqual(application_new.name, get_test_marker())
        self.assertTrue(self.isogeo.application.exists(application_new._id))

        # add created application to deletion
        self.li_fixtures_to_delete.append(application_new._id)

    def test_applications_create_checking_name(self):
        """POST :applications/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        application_local = Application(name=name_to_be_unique)

        # create it online
        application_new_1 = self.isogeo.application.create(
            application=application_local, check_exists=0
        )

        # try to create a application with the same name
        application_new_2 = self.isogeo.application.create(
            application=application_local, check_exists=1
        )

        # check if object has not been created
        self.assertEqual(application_new_2, False)

        # add created application to deletion
        self.li_fixtures_to_delete.append(application_new_1._id)

    # -- GET --
    def test_applications(self):
        """GET :/applications}"""
        # retrieve user applications
        user_applications = self.isogeo.application.listing(caching=1)
        self.assertIsInstance(user_applications, list)
        # parse and test object loader
        for i in user_applications:
            application = Application(**i)
            # tests attributes structure
            self.assertTrue(hasattr(application, "_abilities"))
            self.assertTrue(hasattr(application, "_created"))
            self.assertTrue(hasattr(application, "_id"))
            self.assertTrue(hasattr(application, "_modified"))
            self.assertTrue(hasattr(application, "canHaveManyGroups"))
            self.assertTrue(hasattr(application, "client_id"))
            self.assertTrue(hasattr(application, "client_secret"))
            self.assertTrue(hasattr(application, "groups"))
            self.assertTrue(hasattr(application, "name"))
            self.assertTrue(hasattr(application, "redirect_uris"))
            self.assertTrue(hasattr(application, "scopes"))
            self.assertTrue(hasattr(application, "staff"))
            self.assertTrue(hasattr(application, "type"))
            self.assertTrue(hasattr(application, "url"))
            # tests attributes value
            self.assertEqual(application.client_id, i.get("client_id"))
            self.assertEqual(application.client_secret, i.get("client_secret"))
            self.assertEqual(application.name, i.get("name"))
            self.assertEqual(application.staff, i.get("staff"))

    def test_applications_workgroup(self):
        """GET :/groups/{workgroup_uiid}/applications}"""
        # retrieve workgroup applications
        wg_applications = self.isogeo.application.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
        )
        self.assertIsInstance(wg_applications, list)
        # parse and test object loader
        for i in wg_applications:
            application = Application(**i)
            # tests attributes structure
            self.assertTrue(hasattr(application, "_abilities"))
            self.assertTrue(hasattr(application, "_created"))
            self.assertTrue(hasattr(application, "_id"))
            self.assertTrue(hasattr(application, "_modified"))
            self.assertTrue(hasattr(application, "canHaveManyGroups"))
            self.assertTrue(hasattr(application, "client_id"))
            self.assertTrue(hasattr(application, "client_secret"))
            self.assertTrue(hasattr(application, "groups"))
            self.assertTrue(hasattr(application, "name"))
            self.assertTrue(hasattr(application, "redirect_uris"))
            self.assertTrue(hasattr(application, "scopes"))
            self.assertTrue(hasattr(application, "staff"))
            self.assertTrue(hasattr(application, "type"))
            self.assertTrue(hasattr(application, "url"))
            # tests attributes value
            self.assertEqual(application.client_id, i.get("client_id"))
            self.assertEqual(application.client_secret, i.get("client_secret"))
            self.assertEqual(application.name, i.get("name"))
            self.assertEqual(application.staff, i.get("staff"))

            # check admin url
            self.assertIsInstance(application.admin_url(self.isogeo.mng_url), str)
            self.assertTrue(
                application.admin_url(self.isogeo.mng_url).startswith("https")
            )

    def test_application_workgroups(self):
        """GET :/applications/{application_uiid}/groups}"""
        # retrieve applications
        applications = self.isogeo.application.listing(caching=0)

        # filter on 'groups' applications
        applications = [app for app in applications if app.get("type") == "group"]

        # pick a random application
        application = sample(applications, 1)[0]

        # retrieve workgroup applications
        app_workgroups = self.isogeo.application.workgroups(
            application_id=application.get("_id")
        )
        self.assertIsInstance(app_workgroups, list)

    def test_application_detailed(self):
        """GET :applications/{application_uuid}"""
        # retrieve workgroup applications
        applications = self.isogeo.application.listing(caching=0)

        # pick three applications: user public, user confidential, group
        li_applications_user_confidential = [
            app
            for app in applications
            if app.get("type") == "user" and app.get("kind") == "confidential"
        ]
        li_applications_user_public = [
            app
            for app in applications
            if app.get("type") == "user" and app.get("kind") == "public"
        ]
        li_applications_groups = [
            app for app in applications if app.get("type") == "group"
        ]

        # pick 3 random apps
        application_user_confidential = sample(li_applications_user_confidential, 1)[0]
        application_user_public = sample(li_applications_user_public, 1)[0]
        application_group = sample(li_applications_groups, 1)[0]

        # check exist
        self.assertTrue(
            self.isogeo.application.exists(application_user_confidential.get("_id"))
        )
        self.assertTrue(
            self.isogeo.application.exists(application_user_public.get("_id"))
        )
        self.assertTrue(self.isogeo.application.exists(application_group.get("_id")))

        # get and check
        application_user_confidential = self.isogeo.application.get(
            application_user_confidential.get("_id")
        )
        application_user_public = self.isogeo.application.get(
            application_user_public.get("_id")
        )
        application_group = self.isogeo.application.get(application_group.get("_id"))
        self.assertIsInstance(application_user_confidential, Application)
        self.assertIsInstance(application_user_public, Application)
        self.assertIsInstance(application_group, Application)

    # -- PUT/PATCH --
    def test_applications_update(self):
        """PUT :/applications/{application_uuid}}"""
        # create a new application
        application_fixture = Application(name=get_test_marker())
        application_fixture = self.isogeo.application.create(
            application=application_fixture, check_exists=0
        )

        # modify local object
        application_fixture.name = "{} - HOP".format(get_test_marker())
        application_fixture.url = "https://github.com/isogeo/isogeo-api-py-minsdk"

        # update the online application
        application_fixture = self.isogeo.application.update(application_fixture)

        # check if the change is effective
        application_fixture_updated = self.isogeo.application.get(
            application_fixture._id
        )
        self.assertEqual(
            application_fixture_updated.name, "{} - HOP".format(get_test_marker())
        )
        self.assertEqual(
            application_fixture_updated.url,
            "https://github.com/isogeo/isogeo-api-py-minsdk",
        )
        # self.assertEqual(
        #     application_fixture_updated.published,
        #     "{} content - {}".format(get_test_marker(), self.discriminator),
        # )

        # add created application to deletion
        self.li_fixtures_to_delete.append(application_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
