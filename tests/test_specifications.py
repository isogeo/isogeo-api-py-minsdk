# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_specifications
    # for specific
    python -m unittest tests.test_specifications.TestSpecifications.test_specifications_create
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


# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Specification


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


class TestSpecifications(unittest.TestCase):
    """Test Specification model of Isogeo API."""

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
            client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
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
        # clean created specifications
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.specification.delete(
                    workgroup_id=workgroup_test, specification_id=i
                )
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_specifications_create_basic(self):
        """POST :groups/{workgroup_uuid}/specifications/}"""
        # var
        specification_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        specification_new = Specification(name=specification_name)

        # create it online
        specification_new = self.isogeo.specification.specification_create(
            workgroup_id=workgroup_test, specification=specification_new, check_exists=0
        )

        # checks
        self.assertEqual(specification_new.name, specification_name)
        self.assertTrue(
            self.isogeo.specification.specification_exists(specification_new._id)
        )

        # add created specification to deletion
        self.li_fixtures_to_delete.append(specification_new._id)

    def test_specifications_create_complete(self):
        """POST :groups/{workgroup_uuid}/specifications/}"""
        # populate model object locally
        specification_new = Specification(
            name="{} - {}".format(get_test_marker(), self.discriminator),
            link="https://fr.wikipedia.org/wiki/Licence_Creative_Commons",
        )
        # create it online
        specification_new = self.isogeo.specification.specification_create(
            workgroup_id=workgroup_test, specification=specification_new, check_exists=0
        )

        # checks
        self.assertEqual(
            specification_new.name,
            "{} - {}".format(get_test_marker(), self.discriminator),
        )
        self.assertTrue(
            self.isogeo.specification.specification_exists(specification_new._id)
        )

        # add created specification to deletion
        self.li_fixtures_to_delete.append(specification_new._id)

    def test_specifications_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/specifications/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        specification_local = Specification(name=name_to_be_unique)

        # create it online
        specification_new_1 = self.isogeo.specification.specification_create(
            workgroup_id=workgroup_test,
            specification=specification_local,
            check_exists=0,
        )

        # try to create a specification with the same name
        specification_new_2 = self.isogeo.specification.specification_create(
            workgroup_id=workgroup_test,
            specification=specification_local,
            check_exists=1,
        )

        # check if object has not been created
        self.assertEqual(specification_new_2, False)

        # add created specification to deletion
        self.li_fixtures_to_delete.append(specification_new_1._id)

    # -- GET --
    def test_specifications_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/specifications}"""
        # retrieve workgroup specifications
        wg_specifications = self.isogeo.specification.specifications(
            workgroup_id=workgroup_test, caching=1
        )
        self.assertIsInstance(wg_specifications, list)
        # parse and test object loader
        for i in wg_specifications:
            specification = Specification(**i)
            # tests attributes structure
            self.assertTrue(hasattr(specification, "_abilities"))
            self.assertTrue(hasattr(specification, "_id"))
            self.assertTrue(hasattr(specification, "_tag"))
            self.assertTrue(hasattr(specification, "link"))
            self.assertTrue(hasattr(specification, "name"))
            self.assertTrue(hasattr(specification, "owner"))
            # tests attributes value
            self.assertEqual(specification.link, i.get("link"))
            self.assertEqual(specification.name, i.get("name"))
            self.assertEqual(specification.published, i.get("published"))

    def test_specification_detailed(self):
        """GET :specifications/{specification_uuid}"""
        # retrieve workgroup specifications
        if self.isogeo._wg_specifications_names:
            wg_specifications = self.isogeo._wg_specifications_names
        else:
            wg_specifications = self.isogeo.specification.specifications(
                workgroup_id=workgroup_test, caching=0
            )

        # pick two specifications: one locked by Isogeo, one workgroup specific
        specification_id_isogeo = sample(
            list(filter(lambda d: "isogeo" in d.get("_tag"), wg_specifications)), 1
        )[0]
        specification_id_specific = sample(
            list(filter(lambda d: "isogeo" not in d.get("_tag"), wg_specifications)), 1
        )[0]

        # check both exist
        self.assertTrue(
            self.isogeo.specification.specification_exists(
                specification_id_isogeo.get("_id")
            )
        )
        self.assertTrue(
            self.isogeo.specification.specification_exists(
                specification_id_specific.get("_id")
            )
        )

        # get and check both
        specification_isogeo = self.isogeo.specification.specification(
            specification_id_isogeo.get("_id")
        )
        specification_specific = self.isogeo.specification.specification(
            specification_id_specific.get("_id")
        )
        self.assertIsInstance(specification_isogeo, Specification)
        self.assertIsInstance(specification_specific, Specification)

    # -- PUT/PATCH --
    def test_specifications_update(self):
        """PUT :groups/{workgroup_uuid}/specifications/{specification_uuid}}"""
        # create a new specification
        specification_fixture = Specification(
            name="{} - {}".format(get_test_marker(), self.discriminator)
        )
        specification_fixture = self.isogeo.specification.specification_create(
            workgroup_id=workgroup_test,
            specification=specification_fixture,
            check_exists=0,
        )

        # modify local object
        specification_fixture.name = "{} - {}".format(
            get_test_marker(), self.discriminator
        )
        specification_fixture.link = "https://github.com/isogeo/isogeo-api-py-minsdk"
        # specification_fixture.published = "{} content - {}".format(
        #     get_test_marker(), self.discriminator
        # )

        # update the online specification
        specification_fixture = self.isogeo.specification.specification_update(
            specification_fixture
        )

        # check if the change is effective
        specification_fixture_updated = self.isogeo.specification.specification(
            specification_fixture._id
        )
        self.assertEqual(
            specification_fixture_updated.name,
            "{} - {}".format(get_test_marker(), self.discriminator),
        )
        self.assertEqual(
            specification_fixture_updated.link,
            "https://github.com/isogeo/isogeo-api-py-minsdk",
        )
        # self.assertEqual(
        #     specification_fixture_updated.published,
        #     "{} content - {}".format(get_test_marker(), self.discriminator),
        # )

        # add created specification to deletion
        self.li_fixtures_to_delete.append(specification_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
