# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

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
from os import environ
from pathlib import Path
from random import sample
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv
import urllib3


# module target
from isogeo_pysdk import Isogeo


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
METADATA_TEST_FIXTURE_UUID_ML = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE_ML")
WORKGROUP_TEST_FIXTURE_UUID_ML = environ.get("ISOGEO_WORKGROUP_TEST_UUID_ML")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name."""
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
        if environ.get("ISOGEO_PLATFORM").lower() in ["qa", "custom"]:
            urllib3.disable_warnings()

        # API connection
        if environ.get("ISOGEO_PLATFORM").lower() == "custom":
            isogeo_urls = {
                "api_url": environ.get("ISOGEO_API_URL")
            }
            cls.isogeo = Isogeo(
                auth_mode="group",
                client_id=environ.get("ISOGEO_API_GROUP_CLIENT_ID"),
                client_secret=environ.get("ISOGEO_API_GROUP_CLIENT_SECRET"),
                auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
                platform=environ.get("ISOGEO_PLATFORM").lower(),
                isogeo_urls=isogeo_urls
            )
        else:
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

    def authenticate_as_user_legacy(self):
        # API connection
        if environ.get("ISOGEO_PLATFORM").lower() == "custom":
            isogeo_urls = {
                "api_url": environ.get("ISOGEO_API_URL")
            }
            isogeo_client = Isogeo(
                client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
                client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
                auth_mode="user_legacy",
                auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
                platform=environ.get("ISOGEO_PLATFORM").lower(),
                isogeo_urls=isogeo_urls
            )
        else:
            isogeo_client = Isogeo(
                auth_mode="user_legacy",
                client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
                client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
                auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
                platform=environ.get("ISOGEO_PLATFORM", "qa"),
            )
        # getting a token
        isogeo_client.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )
        return isogeo_client

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- GET --
    def test_search_augmented(self):
        """Augmented search with shares UUID."""
        # at start, shares_id attribute doesn't exist
        # self.assertFalse(hasattr(self.isogeo, "shares_id"))
        # normal
        search = self.isogeo.search(page_size=0, whole_results=0, augment=0)
        tags_shares = [i for i in search.tags if i.startswith("share:")]
        # shares_id attribute still doesn't exist
        self.assertEqual(len(tags_shares), 0)
        # self.assertFalse(hasattr(self.isogeo, "shares_id"))

        # augment it
        search = self.isogeo.search(page_size=0, whole_results=0, augment=1)

        # compare
        tags_shares = [i for i in search.tags if i.startswith("share:")]
        self.assertNotEqual(len(tags_shares), 0)
        self.assertTrue(hasattr(self.isogeo, "shares_id"))  # now it exists

        # redo using existing attribute
        search = self.isogeo.search(page_size=0, whole_results=0, augment=1)

    def test_search_search_as_application(self):
        """GET :resources/search."""
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
        search_10 = self.isogeo.search(page_size=10, whole_results=0)
        md_a, md_b = sample(search_10.results, 2)
        md_bad = "trust_me_this_is_a_good_uuid"
        # get random metadata within a small search
        search_ids_1 = self.isogeo.search(specific_md=(md_a.get("_id"),))
        search_ids_2 = self.isogeo.search(
            specific_md=(md_a.get("_id"), md_b.get("_id"))
        )
        search_ids_3 = self.isogeo.search(
            specific_md=(md_a.get("_id"), md_b.get("_id"), md_bad)
        )
        # test length
        self.assertEqual(len(search_ids_1.results), 1)
        self.assertEqual(len(search_ids_2.results), 2)
        self.assertEqual(len(search_ids_3.results), 2)

    def test_search_specific_mds_bad(self):
        """Searches filtering on specific metadata."""
        # get random metadata within a small search
        search = self.isogeo.search(whole_results=0)
        metadata_id = sample(search.results, 1)[0]

        # pass metadata UUID
        with self.assertRaises(TypeError):
            self.isogeo.search(
                page_size=0, whole_results=0, specific_md=metadata_id.get("_id")
            )

    # includes
    def test_search_includes_ok(self):
        """Searches including includes."""
        self.isogeo.search(page_size=0, whole_results=0, include=("links", "contacts"))

    def test_search_includes_all_ok(self):
        """Searches including includes."""
        self.isogeo.search(page_size=0, whole_results=0, include="all")

    def test_search_includes_empty(self):
        """Search with empty includes list."""
        self.isogeo.search(page_size=0, whole_results=0, include=())

    def test_search_includes_bad(self):
        """Include sub_resources require a list."""
        with self.assertRaises(TypeError):
            self.isogeo.search(page_size=0, whole_results=0, include="links")

    # query
    def test_search_parameter_query_ok(self):
        """Search with good query parameters."""
        # contacts
        self.isogeo.search(
            query="contact:group:643f1035377b4ca59da6f31a39704c34",
            page_size=0,
            whole_results=0,
        )
        self.isogeo.search(
            query="contact:08b3054757544463abd06f3ab51ee491:fe3e8ef97b8446be92d3c315ccbc70f9",
            page_size=0,
            whole_results=0,
        )
        # catalog
        self.isogeo.search(
            query="catalog:633216a375ab48ca8ca72e4a1af7a266",
            page_size=0,
            whole_results=0,
        )
        # CSW data-source
        self.isogeo.search(
            query="data-source:ace35ec171da4d0aa2f10e7308dcbdc5",
            page_size=0,
            whole_results=0,
        )
        # format
        self.isogeo.search(query="format:shp", page_size=0, whole_results=0)
        # has-no
        self.isogeo.search(query="has-no:keyword", page_size=0, whole_results=0)
        # inspire themes
        self.isogeo.search(
            query="keyword:inspire-theme:administrativeunits",
            page_size=0,
            whole_results=0,
        )
        # keyword
        self.isogeo.search(query="keyword:isogeo:2018", page_size=0, whole_results=0)
        # licenses
        self.isogeo.search(
            query="license:isogeo:63f121e14eda4f47b748595e0bcccc31",
            page_size=0,
            whole_results=0,
        )
        self.isogeo.search(
            query="license:{}:76c02a0baf594c77a569b3a1325aee30".format(
                WORKGROUP_TEST_FIXTURE_UUID
            ),
            page_size=0,
            whole_results=0,
        )
        # SRS
        self.isogeo.search(query="coordinate-system:2154", page_size=0, whole_results=0)
        # types
        self.isogeo.search(query="type:dataset", page_size=0, whole_results=0)
        self.isogeo.search(query="type:vector-dataset", page_size=0, whole_results=0)
        self.isogeo.search(query="type:raster-dataset", page_size=0, whole_results=0)
        self.isogeo.search(query="type:no-geo-dataset", page_size=0, whole_results=0)
        self.isogeo.search(query="type:service", page_size=0, whole_results=0)
        self.isogeo.search(query="type:resource", page_size=0, whole_results=0)
        # workgroup - owner
        self.isogeo.search(
            query="owner:{}".format(WORKGROUP_TEST_FIXTURE_UUID),
            page_size=0,
            whole_results=0,
        )
        # unknown
        self.isogeo.search(query="unknown:filter", page_size=0, whole_results=0)

    def test_search_bad_parameter_query(self):
        """Search with bad parameter."""
        with self.assertRaises(ValueError):
            self.isogeo.search(query="type:youpi")
        with self.assertRaises(ValueError):
            self.isogeo.search(query="action:yipiyo")
        with self.assertRaises(ValueError):
            self.isogeo.search(query="provider:youplaboum")

    def test_search_bad_parameter_geographic(self):
        """Search with bad parameter."""
        # geometric operator
        with self.assertRaises(ValueError):
            # georel should'nt be used without box or geo
            self.isogeo.search(georel="intersects")
        with self.assertRaises(ValueError):
            # georel bad value
            self.isogeo.search(bbox="-4.970,30.69418,8.258,51.237", georel="cross")

    def test_parameter_not_unique_search(self):
        """SDK raises error for search with a parameter that must be
        unique."""
        with self.assertRaises(ValueError):
            self.isogeo.search(query="coordinate-system:32517 coordinate-system:4326")
        with self.assertRaises(ValueError):
            self.isogeo.search(query="format:shp format:dwg")
        with self.assertRaises(ValueError):
            self.isogeo.search(
                query="owner:{} owner:08b3054757544463abd06f3ab51ee491".format(
                    WORKGROUP_TEST_FIXTURE_UUID
                )
            )
        with self.assertRaises(ValueError):
            self.isogeo.search(query="type:vector-dataset type:raster-dataset")
        # disabling check, it should not raise anything
        self.isogeo.search(
            query="coordinate-system:32517 coordinate-system:4326", check=0
        )
        self.isogeo.search(query="format:shp format:dwg", check=0)
        self.isogeo.search(
            query="owner:{} owner:08b3054757544463abd06f3ab51ee491".format(
                WORKGROUP_TEST_FIXTURE_UUID
            ),
            check=0,
        )
        self.isogeo.search(query="type:vector-dataset type:raster-dataset", check=0)

    def test_search_multilingual_fr(self):
        """Searches filtering on specific metadata."""

        # launch 1 searches in french about a specific resource
        lang_code = "fr"
        expected_title = "Fiche complète"
        expected_abstract = "Résumé en français"
        search = self.isogeo.search(
            whole_results=1,
            lang=lang_code,
            specific_md=(METADATA_TEST_FIXTURE_UUID_ML,),
            include=("translations",)
        )
        metadata = search.results[0]

        self.assertEqual(len(search.results), 1)
        self.assertTrue(len(metadata.get("translations")) > 0)
        self.assertIn("translations", metadata)
        translation = [
            trans for trans in metadata.get("translations")
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)
        self.assertIn("_fieldsLanguage", metadata)
        self.assertEqual(metadata.get("_fieldsLanguage"), lang_code)
        self.assertEqual(metadata.get("title"), expected_title)
        self.assertEqual(metadata.get("abstract"), expected_abstract)

    def test_search_multilingual_en(self):
        """Searches filtering on specific metadata."""

        # launch 1 searches in english about a specific resource
        lang_code = "en"
        expected_title = "Title in english"
        expected_abstract = "English summary"
        search = self.isogeo.search(
            whole_results=1,
            lang=lang_code,
            specific_md=(METADATA_TEST_FIXTURE_UUID_ML,),
            include=("translations",)
        )
        metadata = search.results[0]

        self.assertEqual(len(search.results), 1)
        self.assertTrue(len(metadata.get("translations")) > 0)
        self.assertIn("translations", metadata)
        translation = [
            trans for trans in metadata.get("translations")
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)
        self.assertIn("_fieldsLanguage", metadata)
        self.assertEqual(metadata.get("_fieldsLanguage"), lang_code)
        self.assertEqual(metadata.get("title"), expected_title)
        self.assertEqual(metadata.get("abstract"), expected_abstract)

    def test_search_multilingual_es(self):
        """Searches filtering on specific metadata."""

        # launch 1 searches in spanish about a specific resource
        lang_code = "es"
        expected_title = "Hoja de metadatos completa"
        expected_abstract = "Resumen en español"
        search = self.isogeo.search(
            whole_results=1,
            lang=lang_code,
            specific_md=(METADATA_TEST_FIXTURE_UUID_ML,),
            include=("translations",)
        )
        metadata = search.results[0]

        self.assertEqual(len(search.results), 1)
        self.assertTrue(len(metadata.get("translations")) > 0)
        self.assertIn("translations", metadata)
        translation = [
            trans for trans in metadata.get("translations")
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)
        self.assertIn("_fieldsLanguage", metadata)
        self.assertEqual(metadata.get("_fieldsLanguage"), lang_code)
        self.assertEqual(metadata.get("title"), expected_title)
        self.assertEqual(metadata.get("abstract"), expected_abstract)

    def test_search_group_multilingual_fr(self):
        """Searches filtering on specific metadata."""
        isogeo_client = self.authenticate_as_user_legacy()

        # launch 1 searches in french about a specific resource
        lang_code = "fr"
        expected_title = "Fiche complète"
        expected_abstract = "Résumé en français"
        search = isogeo_client.search(
            group=WORKGROUP_TEST_FIXTURE_UUID_ML,
            whole_results=1,
            lang=lang_code,
            specific_md=(METADATA_TEST_FIXTURE_UUID_ML,),
            include=("translations",)
        )
        metadata = search.results[0]

        self.assertEqual(len(search.results), 1)
        self.assertTrue(len(metadata.get("translations")) > 0)
        self.assertIn("translations", metadata)
        translation = [
            trans for trans in metadata.get("translations")
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)
        self.assertIn("_fieldsLanguage", metadata)
        self.assertEqual(metadata.get("_fieldsLanguage"), lang_code)
        self.assertEqual(metadata.get("title"), expected_title)
        self.assertEqual(metadata.get("abstract"), expected_abstract)

        isogeo_client.close()

    def test_search_group_multilingual_en(self):
        """Searches filtering on specific metadata."""
        isogeo_client = self.authenticate_as_user_legacy()

        # launch 1 searches in english about a specific resource
        lang_code = "en"
        expected_title = "Title in english"
        expected_abstract = "English summary"
        search = isogeo_client.search(
            group=WORKGROUP_TEST_FIXTURE_UUID_ML,
            whole_results=1,
            lang=lang_code,
            specific_md=(METADATA_TEST_FIXTURE_UUID_ML,),
            include=("translations",)
        )
        metadata = search.results[0]

        self.assertEqual(len(search.results), 1)
        self.assertTrue(len(metadata.get("translations")) > 0)
        self.assertIn("translations", metadata)
        translation = [
            trans for trans in metadata.get("translations")
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)
        self.assertIn("_fieldsLanguage", metadata)
        self.assertEqual(metadata.get("_fieldsLanguage"), lang_code)
        self.assertEqual(metadata.get("title"), expected_title)
        self.assertEqual(metadata.get("abstract"), expected_abstract)

        isogeo_client.close()

    def test_search_group_multilingual_es(self):
        """Searches filtering on specific metadata."""
        isogeo_client = self.authenticate_as_user_legacy()

        # launch 1 searches in spanish about a specific resource
        lang_code = "es"
        expected_title = "Hoja de metadatos completa"
        expected_abstract = "Resumen en español"
        search = isogeo_client.search(
            group=WORKGROUP_TEST_FIXTURE_UUID_ML,
            whole_results=1,
            lang=lang_code,
            specific_md=(METADATA_TEST_FIXTURE_UUID_ML,),
            include=("translations",)
        )
        metadata = search.results[0]

        self.assertEqual(len(search.results), 1)
        self.assertTrue(len(metadata.get("translations")) > 0)
        self.assertIn("translations", metadata)
        translation = [
            trans for trans in metadata.get("translations")
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)
        self.assertIn("_fieldsLanguage", metadata)
        self.assertEqual(metadata.get("_fieldsLanguage"), lang_code)
        self.assertEqual(metadata.get("title"), expected_title)
        self.assertEqual(metadata.get("abstract"), expected_abstract)

        isogeo_client.close()

    def test_search_full(self):
        """Complete searches."""
        # launch a full search
        self.isogeo.search(whole_results=1)

        # launch again to test event loop management is OK
        self.isogeo.search(whole_results=1, augment=1)
