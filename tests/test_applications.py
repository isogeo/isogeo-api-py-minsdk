# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

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
from os import environ
import logging
from random import sample
from socket import gethostname
from sys import exit, _getframe
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv
from oauthlib.oauth2 import LegacyApplicationClient

# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Application


# #############################################################################
# ######## Globals #################
# ##################################

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


class TestApplications(unittest.TestCase):
    """Test Application model of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not app_script_id or not app_script_secret:
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass
        logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        # API connection
        cls.isogeo = IsogeoSession(
            client=LegacyApplicationClient(client_id=app_script_id),
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
        # clean created applications
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.application.application_delete(application_id=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_applications_create_basic(self):
        """POST :applications/}"""
        # var
        application_name = get_test_marker()

        # create local object
        application_to_create = Application(name=application_name)

        # create it online
        application_new = self.isogeo.application.application_create(
            application=application_to_create
        )

        # checks
        self.assertEqual(application_new.name, application_name)
        self.assertTrue(self.isogeo.application.application_exists(application_new._id))

        # add created application to deletion
        self.li_fixtures_to_delete.append(application_new._id)

    def test_applications_create_complete(self):
        """POST :applications/}"""
        # populate model object locally
        application_new = Application(
            name=get_test_marker(), type="user", canHaveManyGroups=True
        )
        # create it online
        application_new = self.isogeo.application.application_create(
            application=application_new, check_exists=0
        )

        # checks
        self.assertEqual(application_new.name, get_test_marker())
        self.assertTrue(self.isogeo.application.application_exists(application_new._id))

        # add created application to deletion
        self.li_fixtures_to_delete.append(application_new._id)

    def test_applications_create_checking_name(self):
        """POST :applications/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        application_local = Application(name=name_to_be_unique)

        # create it online
        application_new_1 = self.isogeo.application.application_create(
            application=application_local, check_exists=0
        )

        # try to create a application with the same name
        application_new_2 = self.isogeo.application.application_create(
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
        user_applications = self.isogeo.application.applications(caching=1)
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
        wg_applications = self.isogeo.application.applications(
            workgroup_id=workgroup_test, caching=1
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

    def test_application_detailed(self):
        """GET :applications/{application_uuid}"""
        # retrieve workgroup applications
        if self.isogeo._applications_names:
            wg_applications = self.isogeo._applications_names
        else:
            wg_applications = self.isogeo.application.applications(caching=0)

        # pick three applications: user public, user confidential, group
        application_id_user_confidential = sample(
            list(
                filter(
                    lambda d: d.get("type") == "user"
                    and d.get("kind") == "confidential",
                    wg_applications,
                )
            ),
            1,
        )[0]
        application_id_user_public = sample(
            list(
                filter(
                    lambda d: d.get("type") == "user" and d.get("kind") == "public",
                    wg_applications,
                )
            ),
            1,
        )[0]
        application_id_group = sample(
            list(filter(lambda d: d.get("type") == "group", wg_applications)), 1
        )[0]

        # check exist
        self.assertTrue(
            self.isogeo.application.application_exists(
                application_id_user_confidential.get("_id")
            )
        )
        self.assertTrue(
            self.isogeo.application.application_exists(
                application_id_user_public.get("_id")
            )
        )
        self.assertTrue(
            self.isogeo.application.application_exists(application_id_group.get("_id"))
        )

        # get and check
        application_user_confidential = self.isogeo.application.application(
            application_id_user_confidential.get("_id")
        )
        application_user_public = self.isogeo.application.application(
            application_id_user_public.get("_id")
        )
        application_group = self.isogeo.application.application(
            application_id_group.get("_id")
        )
        self.assertIsInstance(application_user_confidential, Application)
        self.assertIsInstance(application_user_public, Application)
        self.assertIsInstance(application_group, Application)

    # -- PUT/PATCH --
    def test_applications_update(self):
        """PUT :/applications/{application_uuid}}"""
        # create a new application
        application_fixture = Application(name=get_test_marker())
        application_fixture = self.isogeo.application.application_create(
            application=application_fixture, check_exists=0
        )

        # modify local object
        application_fixture.name = "{} - HOP".format(get_test_marker())
        application_fixture.url = "https://github.com/isogeo/isogeo-api-py-minsdk"

        # update the online application
        application_fixture = self.isogeo.application.application_update(
            application_fixture
        )

        # check if the change is effective
        application_fixture_updated = self.isogeo.application.application(
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
