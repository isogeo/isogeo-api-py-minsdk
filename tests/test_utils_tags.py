# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:
    
    ```python
    # for whole test
    python -m unittest tests.test_utils
    # for specific
    python -m unittest tests.test_utils.TestIsogeoUtils.
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
import logging
from os import environ, path
from sys import exit
import unittest
from urllib.parse import urlparse

# module target
from isogeo_pysdk import IsogeoUtils, __version__ as pysdk_version

# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get("ISOGEO_API_DEV_ID")
app_token = environ.get("ISOGEO_API_DEV_SECRET")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestIsogeoUtilsTags(unittest.TestCase):
    """Test utils for tags in Isogeo API requests."""

    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

    # standard methods
    def setUp(self):
        """ Fixtures prepared before each test."""
        self.utils = IsogeoUtils()

        # API response samples
        self.tags_sample = path.normpath(r"tests/fixtures/api_response_tests_tags.json")

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- Tags utils --------
    def test_tags_dictionarization_search_rename(self):
        """Tags dictionarization bullet-proof."""
        # load fixture
        with open(self.tags_sample, "r") as f:
            search = json.loads(f.read())
        # dictionarize tags
        t = self.utils.tags_to_dict(
            tags=search.get("tags"),
            prev_query=search.get("query"),
            # duplicated="rename"   # default option
        )

        # check actions
        self.assertDictEqual(
            t[0].get("actions"),
            {
                "Download": "action:download",
                "Other": "action:other",
                "View": "action:view",
            },
        )
        # check catalogs
        self.assertDictEqual(
            t[0].get("catalogs"),
            {
                "OpenData MEL": "catalog:e5b6519c37174854961b952a3afdc31a",
                "Transports": "catalog:e5baf75066614c3cafbeeda93b38692a",
                "Transports (e5baf)": "catalog:e5baf75066614c3cafbeeda93b38692b",
                "Hydrographie": "catalog:e5dc2014418d4deca62e8b7a1307a89e",
            },
        )

        # check providers
        self.assertDictEqual(
            t[0].get("providers"),
            {"auto": "provider:auto", "manual": "provider:manual"},
        )

        # check contacts
        self.assertEqual(len(t[0].get("contacts")), 14)
        self.assertDictEqual(
            t[0].get("contacts"),
            {
                "Isogeo": "contact:32f7e95ec4e94ca3bc1afda960003882:16c82f156326452faaba3b5c78490aa7",
                "Institut national de l'information géographique et forestière (IGN-F)": "contact:32f7e95ec4e94ca3bc1afda960003882:424b3b6024594a35b079a40b6555da6e",
                "BRGM": "contact:69ae2d62eeb44ae2954711da5821d8ba:7533517f803041c1b98c6473a66c0748",
                "BRGM (BRGM)": "contact:69ae2d62eeb44ae2954711da5821d8ba:ed05557bcc924ba3b327cec9245d212b",
                "Service SIG": "contact:79c8b45e196c43878f6309cb6a03dd0c:0e42ebfeebbd419babb6b96922462947",
                "Service SIG (79c8b)": "contact:79c8b45e196c43878f6309cb6a03dd0c:8ea4d13102f94f02838432037f36e252",
                "SIG Brest métropole": "contact:819c49300b9b4921a527629874b49122:93f847d99b01499bacde089f08359314",
                "SIG Brest métropole (Brest Métropole Océane)": "contact:819c49300b9b4921a527629874b49122:9e61a3a3479e49f789c2e275bf396c8e",
                "Isogeo (643f1)": "contact:group:643f1035377b4ca59da6f31a39704c34",
                "OpenStreetMap": "contact:group:6f356d698c8343f2894bc03bd9a96927",
                "Isogeo (709d9)": "contact:group:709d9c129baf4ac1b5dfe658555e424f",
                "Brest Métropole Océane": "contact:group:75fbeca39ef84b1badd670c7cc0bd426",
                "Joe Languille": "contact:user:81060c656c9f48c2bae0953da96943fc",
                "Moby Dick": "contact:user:9edbf593662341b19eba7aea0f13551c",
            },
        )

    def test_tags_dictionarization_search_ignore(self):
        """Tags dictionarization bullet-proof."""
        # load fixture
        with open(self.tags_sample, "r") as f:
            search = json.loads(f.read())
        # dictionarize tags
        t = self.utils.tags_to_dict(
            tags=search.get("tags"), prev_query=search.get("query"), duplicated="ignore"
        )

        # check catalogs
        self.assertDictEqual(
            t[0].get("catalogs"),
            {
                "OpenData MEL": "catalog:e5b6519c37174854961b952a3afdc31a",
                "Transports": "catalog:e5baf75066614c3cafbeeda93b38692b",
                "Hydrographie": "catalog:e5dc2014418d4deca62e8b7a1307a89e",
            },
        )

        # check contacts
        self.assertEqual(len(t[0].get("contacts")), 9)
        self.assertDictEqual(
            t[0].get("contacts"),
            {
                "Isogeo": "contact:group:709d9c129baf4ac1b5dfe658555e424f",
                "Institut national de l'information géographique et forestière (IGN-F)": "contact:32f7e95ec4e94ca3bc1afda960003882:424b3b6024594a35b079a40b6555da6e",
                "BRGM": "contact:69ae2d62eeb44ae2954711da5821d8ba:ed05557bcc924ba3b327cec9245d212b",
                "Service SIG": "contact:79c8b45e196c43878f6309cb6a03dd0c:8ea4d13102f94f02838432037f36e252",
                "SIG Brest métropole": "contact:819c49300b9b4921a527629874b49122:9e61a3a3479e49f789c2e275bf396c8e",
                "OpenStreetMap": "contact:group:6f356d698c8343f2894bc03bd9a96927",
                "Brest Métropole Océane": "contact:group:75fbeca39ef84b1badd670c7cc0bd426",
                "Joe Languille": "contact:user:81060c656c9f48c2bae0953da96943fc",
                "Moby Dick": "contact:user:9edbf593662341b19eba7aea0f13551c",
            },
        )

    def test_tags_dictionarization_search_merge(self):
        """Tags dictionarization bullet-proof."""
        # load fixture
        with open(self.tags_sample, "r") as f:
            search = json.loads(f.read())
        # dictionarize tags
        t = self.utils.tags_to_dict(
            tags=search.get("tags"), prev_query=search.get("query"), duplicated="merge"
        )

        # check catalogs
        self.assertDictEqual(
            t[0].get("catalogs"),
            {
                "OpenData MEL": "catalog:e5b6519c37174854961b952a3afdc31a",
                "Transports": "catalog:e5baf75066614c3cafbeeda93b38692a||catalog:e5baf75066614c3cafbeeda93b38692b",
                "Hydrographie": "catalog:e5dc2014418d4deca62e8b7a1307a89e",
            },
        )

        # check contacts
        self.assertEqual(len(t[0].get("contacts")), 9)
        self.assertDictEqual(
            t[0].get("contacts"),
            {
                "Isogeo": "contact:32f7e95ec4e94ca3bc1afda960003882:16c82f156326452faaba3b5c78490aa7||contact:group:643f1035377b4ca59da6f31a39704c34||contact:group:709d9c129baf4ac1b5dfe658555e424f",
                "Institut national de l'information géographique et forestière (IGN-F)": "contact:32f7e95ec4e94ca3bc1afda960003882:424b3b6024594a35b079a40b6555da6e",
                "BRGM": "contact:69ae2d62eeb44ae2954711da5821d8ba:7533517f803041c1b98c6473a66c0748||contact:69ae2d62eeb44ae2954711da5821d8ba:abdcb17d392a46bc89919fc96e460fd9||contact:69ae2d62eeb44ae2954711da5821d8ba:ed05557bcc924ba3b327cec9245d212b",
                "Service SIG": "contact:79c8b45e196c43878f6309cb6a03dd0c:0e42ebfeebbd419babb6b96922462947||contact:79c8b45e196c43878f6309cb6a03dd0c:49db2bfd0a2848e4b995b90f28a9e1a5||contact:79c8b45e196c43878f6309cb6a03dd0c:7a8368b8d41e4e019f6f280092ae7d6c||contact:79c8b45e196c43878f6309cb6a03dd0c:8ea4d13102f94f02838432037f36e252",
                "SIG Brest métropole": "contact:819c49300b9b4921a527629874b49122:93f847d99b01499bacde089f08359314||contact:819c49300b9b4921a527629874b49122:9e61a3a3479e49f789c2e275bf396c8e",
                "OpenStreetMap": "contact:group:6f356d698c8343f2894bc03bd9a96927",
                "Brest Métropole Océane": "contact:group:75fbeca39ef84b1badd670c7cc0bd426",
                "Joe Languille": "contact:user:81060c656c9f48c2bae0953da96943fc",
                "Moby Dick": "contact:user:9edbf593662341b19eba7aea0f13551c",
            },
        )

    # Bad Boys #####################
    def test_tags_dictionarization_bad(self):
        """Tags dictionarization bullet-proof."""
        with open(self.tags_sample, "r") as f:
            search = json.loads(f.read())
        with self.assertRaises(ValueError):
            self.utils.tags_to_dict(search.get("tags"), duplicated="renam")
