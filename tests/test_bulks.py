# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_bulks
        # for specific
        python -m unittest tests.test_bulks.TestBulks.test_bulks_basic

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
from isogeo_pysdk import BulkReport, Catalog, Isogeo, Metadata, Keyword

# #############################################################################
# ######## Globals #################
# ##################################

# load environment vars from .env file
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


class TestBulks(unittest.TestCase):
    """Test bulk operations of Isogeo API."""

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

        # fixture metadatas
        md_1 = Metadata(title=get_test_marker() + "_1", type="rasterDataset")
        md_2 = Metadata(title=get_test_marker() + "_2", type="vectorDataset")
        md_3 = Metadata(title=get_test_marker() + "_3", type="vectorDataset")
        cls.fixture_metadata_1 = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md_1
        )
        cls.fixture_metadata_2 = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md_2
        )
        cls.fixture_metadata_3 = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md_3
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
        cls.isogeo.metadata.delete(cls.fixture_metadata_1._id)
        cls.isogeo.metadata.delete(cls.fixture_metadata_2._id)
        cls.isogeo.metadata.delete(cls.fixture_metadata_3._id)

        # clean created licenses
        # if len(cls.li_fixtures_to_delete):
        #     for i in cls.li_fixtures_to_delete:
        #         cls.isogeo.catalog.delete(
        #             workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, catalog_id=i
        #         )
        #         pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    def test_bulks_basic(self):
        """POST /resources/"""
        # retrieve catalogs to be associated
        wg_catalogs = self.isogeo.catalog.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, include=None
        )
        catalogs = [Catalog.clean_attributes(cat) for cat in sample(wg_catalogs, 2)]

        # prepare request for catalogs
        self.isogeo.metadata.bulk.prepare(
            metadatas=(
                self.fixture_metadata_1._id,
                self.fixture_metadata_2._id,
                self.fixture_metadata_3._id,
            ),
            action="add",
            target="catalogs",
            models=catalogs,
        )

        # retrieve keywords
        keywords = [
            Keyword(**kwd) for kwd in sample(self.isogeo.keyword.thesaurus().results, 5)
        ]
        # prepare request for keywords
        self.isogeo.metadata.bulk.prepare(
            metadatas=(self.fixture_metadata_1, self.fixture_metadata_2._id),
            action="add",
            target="keywords",
            models=tuple(keywords),
        )

        # send the one-shot request
        req_bulk = self.isogeo.metadata.bulk.send()
        self.assertIsInstance(req_bulk, list)
        self.assertIsInstance(req_bulk[0], BulkReport)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
