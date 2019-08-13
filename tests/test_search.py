# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_search
        # for specific
        python -m unittest tests.test_search.TestSearch.test_search_search_as_application

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
from random import randint, sample
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import Isogeo, Metadata, MetadataSearch


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
    return "TEST_PySDK - Search - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestSearch(unittest.TestCase):
    """Test search methods."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_GROUP_CLIENT_ID") or not environ.get(
            "ISOGEO_API_GROUP_CLIENT_SECRET"
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
            auth_mode="group",
            client_id=environ.get("ISOGEO_API_GROUP_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_GROUP_CLIENT_SECRET"),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )
        # getting a token
        cls.isogeo.connect()

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
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- GET --
    def test_search_search_as_application(self):
        """GET :resources/search"""
        basic_search = self.isogeo.search()
        # check attributes
        self.assertTrue(hasattr(basic_search, "envelope"))
        self.assertTrue(hasattr(basic_search, "limit"))
        self.assertTrue(hasattr(basic_search, "offset"))
        self.assertTrue(hasattr(basic_search, "query"))
        self.assertTrue(hasattr(basic_search, "results"))
        self.assertTrue(hasattr(basic_search, "tags"))
        self.assertTrue(hasattr(basic_search, "total"))

        # additional checks
        print(
            "Authenticated application has access to {} results".format(
                basic_search.total
            )
        )
        self.assertIsInstance(basic_search.total, int)
        self.assertEqual(len(basic_search.results), 20)

    # filter on a list of metadata uuids
    def test_search_specific_mds_ok(self):
        """Searches filtering on specific metadata."""
        # get random metadata within a small search
        search_10 = self.isogeo.search(page_size=10, whole_share=0)
        md_a, md_b = sample(search_10.results, 2)
        md_bad = "trust_me_this_is_a_good_uuid"
        # get random metadata within a small search
        search_ids_1 = self.isogeo.search(specific_md=[md_a.get("_id")])
        search_ids_2 = self.isogeo.search(
            specific_md=[md_a.get("_id"), md_b.get("_id")]
        )
        search_ids_3 = self.isogeo.search(
            specific_md=[md_a.get("_id"), md_b.get("_id"), md_bad]
        )
        # test length
        self.assertEqual(len(search_ids_1.results), 1)
        self.assertEqual(len(search_ids_2.results), 2)
        self.assertEqual(len(search_ids_3.results), 2)

    def test_search_specific_mds_bad(self):
        """Searches filtering on specific metadata."""
        # get random metadata within a small search
        search = self.isogeo.search(
            page_size=5,
            # whole_share=0
        )
        metadata_id = sample(search.results, 2)

        # # pass metadata UUID
        # with self.assertRaises(TypeError):
        #     self.isogeo.search(self.bearer,
        #                         page_size=0,
        #                         whole_share=0,
        #                         specific_md=md)
