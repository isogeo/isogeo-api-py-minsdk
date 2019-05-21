# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_keywords
    # for specific
    python -m unittest tests.test_keywords_complete.TestKeywordsComplete.test_keywords_create_basic
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
from isogeo_pysdk import (
    IsogeoSession,
    __version__ as pysdk_version,
    Keyword,
    KeywordSearch,
)


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


class TestKeywordsComplete(unittest.TestCase):
    """Test Keyword model of Isogeo API."""

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
                # cls.isogeo.keyword.keyword_delete(
                #     workgroup_id=workgroup_test, keyword_id=i
                # )
                pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    # def test_keywords_create_basic(self):
    #     """POST :groups/{workgroup_uuid}/keywords/}"""
    #     # var
    #     keyword_name = "{} - {}".format(get_test_marker(), self.discriminator)

    #     # create local object
    #     keyword_new = Keyword(name=keyword_name)

    #     # create it online
    #     keyword_new = self.isogeo.keyword.keyword_create(
    #         workgroup_id=workgroup_test, keyword=keyword_new, check_exists=0
    #     )

    #     # checks
    #     self.assertEqual(keyword_new.name, keyword_name)
    #     self.assertTrue(
    #         self.isogeo.keyword.keyword_exists(
    #             keyword_new.owner.get("_id"), keyword_new._id
    #         )
    #     )

    #     # add created keyword to deletion
    #     self.li_fixtures_to_delete.append(keyword_new._id)

    # def test_keywords_create_complete(self):
    #     """POST :groups/{workgroup_uuid}/keywords/}"""
    #     # populate model object locally
    #     keyword_new = Keyword(
    #         name="{} - {}".format(get_test_marker(), self.discriminator), scan=True
    #     )
    #     # create it online
    #     keyword_new = self.isogeo.keyword.keyword_create(
    #         workgroup_id=workgroup_test, keyword=keyword_new, check_exists=0
    #     )

    #     # checks
    #     self.assertEqual(
    #         keyword_new.name, "{} - {}".format(get_test_marker(), self.discriminator)
    #     )
    #     self.assertTrue(
    #         self.isogeo.keyword.keyword_exists(
    #             keyword_new.owner.get("_id"), keyword_new._id
    #         )
    #     )

    #     # add created keyword to deletion
    #     self.li_fixtures_to_delete.append(keyword_new._id)

    # def test_keywords_create_checking_name(self):
    #     """POST :groups/{workgroup_uuid}/keywords/}"""
    #     # vars
    #     name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

    #     # create local object
    #     keyword_local = Keyword(name=name_to_be_unique)

    #     # create it online
    #     keyword_new_1 = self.isogeo.keyword.keyword_create(
    #         workgroup_id=workgroup_test, keyword=keyword_local, check_exists=0
    #     )

    #     # try to create a keyword with the same name
    #     keyword_new_2 = self.isogeo.keyword.keyword_create(
    #         workgroup_id=workgroup_test, keyword=keyword_local, check_exists=1
    #     )

    #     # check if object has not been created
    #     self.assertEqual(keyword_new_2, False)

    #     # add created keyword to deletion
    #     self.li_fixtures_to_delete.append(keyword_new_1._id)

    # -- GET --
    def test_keywords_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/keywords/search}"""
        # retrieve workgroup keywords
        wg_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=workgroup_test, caching=0
        )
        # parse and test object loader
        for i in wg_keywords.results:
            # load it
            keyword = Keyword(**i)
            # tests attributes structure
            self.assertTrue(hasattr(keyword, "_abilities"))
            self.assertTrue(hasattr(keyword, "_id"))
            self.assertTrue(hasattr(keyword, "_tag"))
            self.assertTrue(hasattr(keyword, "code"))
            self.assertTrue(hasattr(keyword, "count"))
            self.assertTrue(hasattr(keyword, "description"))
            self.assertTrue(hasattr(keyword, "text"))
            self.assertTrue(hasattr(keyword, "thesaurus"))
            # tests attributes value
            self.assertEqual(keyword._abilities, i.get("_abilities"))
            self.assertEqual(keyword._id, i.get("_id"))
            self.assertEqual(keyword._tag, i.get("_tag"))
            self.assertEqual(keyword.code, i.get("code"))
            self.assertEqual(keyword.count, i.get("count"))
            self.assertEqual(keyword.description, i.get("description"))
            self.assertEqual(keyword.text, i.get("text"))
            self.assertEqual(keyword.thesaurus, i.get("thesaurus"))

    def test_keywords_get_thesaurus(self):
        """GET :thesauri/{thesauri_uuid}/keywords/search}"""
        # retrieve thesauri keywords
        wg_keywords = self.isogeo.keyword.thesaurus(caching=0)
        # parse and test object loader
        for i in wg_keywords.results:
            # load it
            keyword = Keyword(**i)
            # tests attributes structure
            self.assertTrue(hasattr(keyword, "_abilities"))
            self.assertTrue(hasattr(keyword, "_id"))
            self.assertTrue(hasattr(keyword, "_tag"))
            self.assertTrue(hasattr(keyword, "code"))
            self.assertTrue(hasattr(keyword, "count"))
            self.assertTrue(hasattr(keyword, "description"))
            self.assertTrue(hasattr(keyword, "text"))
            self.assertTrue(hasattr(keyword, "thesaurus"))
            # tests attributes value
            self.assertEqual(keyword._abilities, i.get("_abilities"))
            self.assertEqual(keyword._id, i.get("_id"))
            self.assertEqual(keyword._tag, i.get("_tag"))
            self.assertEqual(keyword.code, i.get("code"))
            self.assertEqual(keyword.count, i.get("count"))
            self.assertEqual(keyword.description, i.get("description"))
            self.assertEqual(keyword.text, i.get("text"))
            self.assertEqual(keyword.thesaurus, i.get("thesaurus"))

    # -- PUT/PATCH --
    # def test_keywords_update(self):
    #     """PUT :groups/{workgroup_uuid}/keywords/{keyword_uuid}}"""
    #     # create a new keyword
    #     keyword_fixture = Keyword(name="{}".format(get_test_marker()))
    #     keyword_fixture = self.isogeo.keyword.keyword_create(
    #         workgroup_id=workgroup_test, keyword=keyword_fixture, check_exists=0
    #     )

    #     # modify local object
    #     keyword_fixture.name = "{} - {}".format(get_test_marker(), self.discriminator)
    #     keyword_fixture.scan = True

    #     # update the online keyword
    #     keyword_fixture = self.isogeo.keyword.keyword_update(keyword_fixture)

    #     # check if the change is effective
    #     keyword_fixture_updated = self.isogeo.keyword.keyword(
    #         keyword_fixture.owner.get("_id"), keyword_fixture._id
    #     )
    #     self.assertEqual(
    #         keyword_fixture_updated.name,
    #         "{} - {}".format(get_test_marker(), self.discriminator),
    #     )
    #     self.assertEqual(keyword_fixture_updated.scan, True)

    #     # add created keyword to deletion
    #     self.li_fixtures_to_delete.append(keyword_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
