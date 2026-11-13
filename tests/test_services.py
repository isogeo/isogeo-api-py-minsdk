# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

    :Example:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_services
        # for specific
        python -m unittest tests.test_services.TestServices.test_services_workgroup

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
from sys import exit
from time import sleep

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import Isogeo


# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# fixtures
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")


# #############################################################################
# ########## Classes ###############
# ##################################


class TestServices(unittest.TestCase):
    """Test services routes of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID") or not environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"):
            logging.critical("No API credentials set as env variables.")
            exit()

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() in ["qa", "custom"]:
            urllib3.disable_warnings()

        # API connection
        if environ.get("ISOGEO_PLATFORM").lower() == "custom":
            cls.isogeo = Isogeo(
                client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
                client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
                auth_mode="user_legacy",
                auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
                platform=environ.get("ISOGEO_PLATFORM").lower(),
                isogeo_urls={"api_url": environ.get("ISOGEO_API_URL")},
            )
        else:
            cls.isogeo = Isogeo(
                auth_mode="user_legacy",
                client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
                client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
                auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
                platform=environ.get("ISOGEO_PLATFORM", "qa"),
            )
        # getting a token
        cls.isogeo.connect(username=environ.get("ISOGEO_USER_NAME"), password=environ.get("ISOGEO_USER_PASSWORD"))

    def tearDown(self):
        """Executed after each test."""
        sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- GET workgroup services --
    # --
    def test_services_workgroup(self):
        """GET :groups/{workgroup_uuid}/services"""
        layers_statuses = ("notChecked", "match", "mismatch", "unreadable", "tooLarge", "unknownFormat")

        # one page without check
        wg_services = self.isogeo.services.workgroup(WORKGROUP_TEST_FIXTURE_UUID, check=False, page_size=5)
        self.assertIsInstance(wg_services, dict)
        self.assertEqual(wg_services.get("offset"), 0)
        self.assertEqual(wg_services.get("limit"), 5)
        self.assertLessEqual(len(wg_services.get("results")), 5)
        for service in wg_services.get("results"):
            self.assertIsInstance(service.get("_id"), str)
            self.assertEqual(service.get("check").get("status"), "notChecked")
            self.assertEqual(service.get("layers").get("status"), "notChecked")
            self.assertIsInstance(service.get("layers").get("declared"), int)

        # all the pages, requested one by one
        wg_services_all = self.isogeo.services.workgroup(WORKGROUP_TEST_FIXTURE_UUID, check=False, page_size=1, whole_results=True)
        self.assertEqual(len(wg_services_all.get("results")), wg_services_all.get("total"))
        self.assertEqual(len({service.get("_id") for service in wg_services_all.get("results")}), wg_services_all.get("total"))

        # checked page (the test user administrates the workgroup)
        wg_services_checked = self.isogeo.services.workgroup(WORKGROUP_TEST_FIXTURE_UUID, check=True, page_size=2)
        for service in wg_services_checked.get("results"):
            self.assertIn(service.get("layers").get("status"), layers_statuses)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
