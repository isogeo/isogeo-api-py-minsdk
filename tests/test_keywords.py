# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_keywords
# for specific
python -m unittest tests.test_keywords.TestKeywordsComplete.test_keywords_create_basic
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
from isogeo_pysdk import Isogeo, Keyword


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

# shorctuts
ISOGEO_THESAURUS_ID = "1616597fbc4348c8b11ef9d59cf594c8"
GROUPTHEME_THESAURUS_ID = "0edc90b138ef41e593cf47fbca2cb1ad"
INSPIRE_THESAURUS_ID = "926c676c380046d7af99bcae343ac813"

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name."""
    return "TEST_PySDK - {}".format(_getframe(1).f_code.co_name)


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
        if not environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID") or not environ.get(
            "ISOGEO_API_USER_LEGACY_CLIENT_SECRET"
        ):
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass

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

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        cls.metadata_fixture_existing = cls.isogeo.metadata.get(
            metadata_id=METADATA_TEST_FIXTURE_UUID
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
        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for kw, th_id in cls.li_fixtures_to_delete:
                cls.isogeo.keyword.delete(
                    keyword=kw,
                    thesaurus_id=th_id
                )
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_keywords_create_basic_nochecking_exists(self):
        """POST :thesauri/{isogeo_thesaurus_uuid}/keywords/}"""
        # var
        keyword_text = "{} - {}".format(get_test_marker(), self.discriminator)

        for thesaurus_id in [ISOGEO_THESAURUS_ID, GROUPTHEME_THESAURUS_ID]:
            # create local object
            keyword_new = Keyword(text=keyword_text)

            # create it online
            keyword_new = self.isogeo.keyword.create(
                keyword=keyword_new,
                thesaurus_id=thesaurus_id,
                check_exists=0
            )

            # checks
            self.assertEqual(keyword_new.text, keyword_text)
            self.assertIsInstance(keyword_new, Keyword)

            # add created keyword to deletion
            self.li_fixtures_to_delete.append(
                (keyword_new, thesaurus_id)
            )

        keyword_new = Keyword(text=keyword_text)
        with self.assertRaises(ValueError):
            keyword_new = self.isogeo.keyword.create(
                keyword=keyword_new,
                thesaurus_id=INSPIRE_THESAURUS_ID,
                check_exists=0
            )
        if keyword_new._id is not None:
            self.li_fixtures_to_delete.append(
                (keyword_new, thesaurus_id)
            )

    def test_keywords_create_basic_checking_exists(self):
        """POST :thesauri/{isogeo_thesaurus_uuid}/keywords/}"""
        # var
        keyword_text = "{} - {}".format(get_test_marker(), self.discriminator)

        for thesaurus_id in [ISOGEO_THESAURUS_ID, GROUPTHEME_THESAURUS_ID]:
            # create local object
            keyword_new = Keyword(text=keyword_text)

            # create it online
            keyword_new = self.isogeo.keyword.create(
                keyword=keyword_new,
                thesaurus_id=thesaurus_id,
                check_exists=1
            )

            # checks
            self.assertEqual(keyword_new.text, keyword_text)
            self.assertIsInstance(keyword_new, Keyword)

            # add created keyword to deletion
            self.li_fixtures_to_delete.append(
                (keyword_new, thesaurus_id)
            )

        keyword_new = Keyword(text=keyword_text)
        with self.assertRaises(ValueError):
            keyword_new = self.isogeo.keyword.create(
                keyword=keyword_new,
                thesaurus_id=INSPIRE_THESAURUS_ID,
                check_exists=1
            )
        if keyword_new._id is not None:
            self.li_fixtures_to_delete.append(
                (keyword_new, thesaurus_id)
            )

    def test_keywords_create_similar_nochecking_exists(self):
        """POST :thesauri/{isogeo_thesaurus_uuid}/keywords/}

        Handling case when the keyword already exists
        """
        # var
        keyword_text = "{} - {}".format(get_test_marker(), self.discriminator)

        for thesaurus_id in [ISOGEO_THESAURUS_ID, GROUPTHEME_THESAURUS_ID]:
            # create local objects
            keyword_new_1 = Keyword(text=keyword_text)
            keyword_new_2 = Keyword(text=keyword_text)

            # create first it online
            keyword_new_1_created = self.isogeo.keyword.create(
                keyword=keyword_new_1, thesaurus_id=thesaurus_id, check_exists=0
            )

            # add created keyword to deletion
            self.li_fixtures_to_delete.append(
                (keyword_new_1_created, thesaurus_id)
            )

            # check
            self.assertEqual(keyword_new_1_created.text, keyword_text)
            self.assertIsInstance(keyword_new_1_created, Keyword)

            # try to create a keyword with the same text
            keyword_new_2_created = self.isogeo.keyword.create(
                keyword=keyword_new_2, thesaurus_id=thesaurus_id, check_exists=0
            )

            # check
            self.assertEqual(keyword_new_2_created.text, keyword_text)
            self.assertIsInstance(keyword_new_2_created, Keyword)

            # compare
            self.assertTrue(keyword_new_1_created._id == keyword_new_2_created._id)

    def test_keywords_create_similar_checking_exists(self):
        """POST :thesauri/{isogeo_thesaurus_uuid}/keywords/}

        Handling case when the keyword already exists
        """
        # var
        keyword_text = "{} - {}".format(get_test_marker(), self.discriminator)

        for thesaurus_id in [ISOGEO_THESAURUS_ID, GROUPTHEME_THESAURUS_ID]:
            # create local objects
            keyword_new_1 = Keyword(text=keyword_text)
            keyword_new_2 = Keyword(text=keyword_text)

            # create first it online
            keyword_new_1_created = self.isogeo.keyword.create(
                keyword=keyword_new_1, thesaurus_id=thesaurus_id, check_exists=1
            )

            # add created keyword to deletion
            self.li_fixtures_to_delete.append(
                (keyword_new_1_created, thesaurus_id)
            )

            # check
            self.assertEqual(keyword_new_1_created.text, keyword_text)
            self.assertIsInstance(keyword_new_1_created, Keyword)

            # try to create a keyword with the same text
            keyword_new_2_created = self.isogeo.keyword.create(
                keyword=keyword_new_2, thesaurus_id=thesaurus_id, check_exists=1
            )

            # check
            self.assertEqual(keyword_new_2_created.text, keyword_text)
            self.assertIsInstance(keyword_new_2_created, Keyword)

            # compare
            self.assertTrue(keyword_new_1_created._id == keyword_new_2_created._id)

    # -- GET --
    def test_keywords_list_metadata(self):
        """GET :resources/{metadata_uuid}/keywords/}"""
        # retrieve metadata keywords from keywords api module
        keywords_metadata = self.isogeo.keyword.metadata(
            metadata_id=METADATA_TEST_FIXTURE_UUID
        )
        self.assertIsInstance(keywords_metadata, list)

        # retrieve metadata keywords from metadata api module (shortut)
        metadata_keywords = self.isogeo.metadata.keywords(
            metadata=self.metadata_fixture_existing
        )
        self.assertIsInstance(metadata_keywords, list)

        # compare both
        self.assertEqual(keywords_metadata, metadata_keywords)

    def test_keywords_search_workgroup(self):
        """GET :groups/{workgroup_uuid}/keywords/search}"""
        # retrieve workgroup keywords
        wg_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, whole_results=0, page_size=20
        )

        if wg_keywords.total > 20:
            self.assertEqual(len(wg_keywords.results), 20)
        else:
            self.assertEqual(wg_keywords.total, len(wg_keywords.results))

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

    def test_keywords_search_workgroup_whole_results(self):
        """GET :groups/{workgroup_uuid}/keywords/search}"""
        # retrieve workgroup keywords
        wg_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, whole_results=1, page_size=20
        )

        self.assertEqual(len(wg_keywords.results), wg_keywords.total)

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

    def test_keywords_search_thesaurus(self):
        """GET :thesauri/{thesauri_uuid}/keywords/search}"""

        # retrieve thesauri keywords
        for thesaurus_id in [ISOGEO_THESAURUS_ID, GROUPTHEME_THESAURUS_ID]:
            th_keywords = self.isogeo.keyword.thesaurus(
                thesaurus_id=thesaurus_id, whole_results=False, page_size=20
            )
            if th_keywords.total > 20:
                self.assertEqual(len(th_keywords.results), 20)
            else:
                self.assertEqual(th_keywords.total, len(th_keywords.results))
            # parse and test object loader
            for i in th_keywords.results:
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

    def test_keywords_search_thesaurus_whole_results(self):
        """GET :thesauri/{thesauri_uuid}/keywords/search}"""

        # retrieve thesauri keywords
        th_keywords = self.isogeo.keyword.thesaurus(
            thesaurus_id=ISOGEO_THESAURUS_ID, whole_results=True, query="eau"
        )
        self.assertEqual(len(th_keywords.results), th_keywords.total)

        li_matching_kw = [kw for kw in th_keywords.results if kw.get("text") == "eau"]
        self.assertTrue(len(li_matching_kw) == 1)
        self.assertTrue(li_matching_kw[0].get("text") == "eau")

        # parse and test object loader
        for i in th_keywords.results:
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

    def test_keyword_detailed(self):
        """GET :keywords/{keyword_uuid}"""

        # retrieve a random thesauri keywords
        for thesaurus_id in [ISOGEO_THESAURUS_ID, GROUPTHEME_THESAURUS_ID]:
            thesaurus_keywords = self.isogeo.keyword.thesaurus(
                thesaurus_id=thesaurus_id, page_size=50, include=("_abilities", "count", "thesaurus")
            )
            # pick one randomly
            random_keyword_dict = sample(thesaurus_keywords.results, 1)[0]
            random_keyword = self.isogeo.keyword.get(random_keyword_dict.get("_id"))
            # tests attributes structure
            self.assertTrue(hasattr(random_keyword, "_abilities"))
            self.assertTrue(hasattr(random_keyword, "_id"))
            self.assertTrue(hasattr(random_keyword, "_tag"))
            self.assertTrue(hasattr(random_keyword, "code"))
            self.assertTrue(hasattr(random_keyword, "count"))
            self.assertTrue(hasattr(random_keyword, "description"))
            self.assertTrue(hasattr(random_keyword, "text"))
            self.assertTrue(hasattr(random_keyword, "thesaurus"))
            self.assertEqual(random_keyword_dict.get("_abilities"), random_keyword._abilities)
            self.assertEqual(random_keyword_dict.get("_id"), random_keyword._id)
            self.assertEqual(random_keyword_dict.get("_tag"), random_keyword._tag)
            self.assertEqual(random_keyword_dict.get("code"), random_keyword.code)
            self.assertEqual(random_keyword_dict.get("count"), random_keyword.count)
            self.assertEqual(random_keyword_dict.get("description"), random_keyword.description)
            self.assertEqual(random_keyword_dict.get("text"), random_keyword.text)
            self.assertEqual(random_keyword_dict.get("thesaurus"), random_keyword.thesaurus)

    def test_associate_and_dissociate_workgroup_groupTheme(self):
        """POST :group/{workgroup_uuid}/keywords/{keyword_uuid}"""
        # fetch fixture workgroup
        workgroup_test_fixture = self.isogeo.workgroup.get(WORKGROUP_TEST_FIXTURE_UUID)

        # pick a random groupTheme that is not already associated with fixture workgroup
        groupTheme_thesaurus_keywords = self.isogeo.keyword.thesaurus(
            thesaurus_id=GROUPTHEME_THESAURUS_ID, page_size=100
        )
        groupTheme_workgroup_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=workgroup_test_fixture._id, thesaurus_id=GROUPTHEME_THESAURUS_ID, whole_results=True
        )
        if groupTheme_workgroup_keywords.results and len(groupTheme_workgroup_keywords.results):
            groupTheme_workgroup_tags = [kw.get("_tag") for kw in groupTheme_workgroup_keywords.results]
            randow_keyword_dict = sample(
                [kw_dict for kw_dict in groupTheme_thesaurus_keywords.results if kw_dict.get("_tag") not in groupTheme_workgroup_tags],
                1
            )[0]
        else:
            groupTheme_workgroup_tags = []
            randow_keyword_dict = sample(groupTheme_thesaurus_keywords.results, 1)[0]
        random_keyword = Keyword(**randow_keyword_dict)

        # check that random_keyword is not already associated with fixture workgroup
        self.assertFalse(random_keyword._tag in groupTheme_workgroup_tags)

        # associate random_keyword with fixture workgroup
        self.assertEqual(
            self.isogeo.keyword.associate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword
            ).status_code,
            204
        )
        # check random_keyword is actually associated with fixture workgroup
        groupTheme_workgroup_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=workgroup_test_fixture._id, thesaurus_id=GROUPTHEME_THESAURUS_ID, whole_results=True
        )
        self.assertTrue(any(kw_dict.get("_tag") == random_keyword._tag for kw_dict in groupTheme_workgroup_keywords.results))
        self.assertTrue(any(kw_dict.get("text") == random_keyword.text for kw_dict in groupTheme_workgroup_keywords.results))
        self.assertTrue(any(kw_dict.get("_id") == random_keyword._id for kw_dict in groupTheme_workgroup_keywords.results))

        # try to associate random_keyword with fixture workgroup again
        # with check_exists=True
        self.assertEqual(
            self.isogeo.keyword.associate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=True
            ),
            (True, "already done")
        )
        # with check_exists=False
        self.assertEqual(
            self.isogeo.keyword.associate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=False
            ),
            (True, 409)
        )

        # dissociate random_keyword from fixture workgroup
        self.isogeo.keyword.dissociate_workgroup(
            workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=False
        )
        # check random_keyword is actually dissociated from fixture workgroup
        groupTheme_workgroup_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=workgroup_test_fixture._id, thesaurus_id=GROUPTHEME_THESAURUS_ID, whole_results=True
        )
        if groupTheme_workgroup_keywords.results and len(groupTheme_workgroup_keywords.results):
            self.assertTrue(all(kw_dict.get("_tag") != random_keyword._tag for kw_dict in groupTheme_workgroup_keywords.results))
            self.assertTrue(all(kw_dict.get("text") != random_keyword.text for kw_dict in groupTheme_workgroup_keywords.results))
            self.assertTrue(all(kw_dict.get("_id") != random_keyword._id for kw_dict in groupTheme_workgroup_keywords.results))
        else:
            pass

        # try to dissociate random_keyword from fixture workgroup again
        # with check_exists=True
        self.assertEqual(
            self.isogeo.keyword.dissociate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=True
            ),
            (True, "already done")
        )
        # with check_exists=False
        self.assertEqual(
            self.isogeo.keyword.dissociate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=False
            ),
            (True, 404)
        )

    def test_associate_and_dissociate_workgroup_isogeo(self):
        """POST :group/{workgroup_uuid}/keywords/{keyword_uuid}"""

        # pick a random isogeo keyword
        random_keyword = Keyword(
            **sample(
                self.isogeo.keyword.thesaurus(
                    thesaurus_id=ISOGEO_THESAURUS_ID, page_size=100
                ).results,
                1
            )[0]
        )
        # fetch fixture workgroup
        workgroup_test_fixture = self.isogeo.workgroup.get(WORKGROUP_TEST_FIXTURE_UUID)

        # set workgroup.areKeywordsRestricted object propertie to false
        workgroup_test_fixture.areKeywordsRestricted = False

        # check that it won't even try to associate a keyword
        self.assertEqual(
            self.isogeo.keyword.associate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword
            ),
            (True, "not necessary")
        )

        # check that it won't even try to dissociate a keyword
        self.assertEqual(
            self.isogeo.keyword.dissociate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword
            ),
            (True, "not necessary")
        )

        # set workgroup.areKeywordsRestricted to True for real this time
        workgroup_test_fixture.areKeywordsRestricted = True
        self.isogeo.workgroup.update(workgroup_test_fixture)

        # pick a random isogeo keyword that is not already associated with fixture workgroup
        isogeo_thesaurus_keywords = self.isogeo.keyword.thesaurus(
            thesaurus_id=ISOGEO_THESAURUS_ID, page_size=100
        )
        isogeo_workgroup_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=workgroup_test_fixture._id, thesaurus_id=ISOGEO_THESAURUS_ID, whole_results=True
        )
        if isogeo_workgroup_keywords.results and len(isogeo_workgroup_keywords.results):
            isogeo_workgroup_tags = [kw.get("_tag") for kw in isogeo_workgroup_keywords.results]
            randow_keyword_dict = sample(
                [kw_dict for kw_dict in isogeo_thesaurus_keywords.results if kw_dict.get("_tag") not in isogeo_workgroup_tags],
                1
            )[0]
        else:
            isogeo_workgroup_tags = []
            randow_keyword_dict = sample(isogeo_thesaurus_keywords.results, 1)[0]
        random_keyword = Keyword(**randow_keyword_dict)

        # check that random_keyword is not already associated with fixture workgroup
        self.assertFalse(random_keyword._tag in isogeo_workgroup_tags)

        # associate random_keyword with fixture workgroup
        self.isogeo.keyword.associate_workgroup(
            workgroup=workgroup_test_fixture, keyword=random_keyword
        )
        # check random_keyword is actually associated with fixture workgroup
        isogeo_workgroup_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=workgroup_test_fixture._id, thesaurus_id=ISOGEO_THESAURUS_ID, whole_results=True
        )
        self.assertTrue(any(kw_dict.get("_tag") == random_keyword._tag for kw_dict in isogeo_workgroup_keywords.results))
        self.assertTrue(any(kw_dict.get("text") == random_keyword.text for kw_dict in isogeo_workgroup_keywords.results))
        self.assertTrue(any(kw_dict.get("_id") == random_keyword._id for kw_dict in isogeo_workgroup_keywords.results))

        # try to associate random_keyword with fixture workgroup again
        # with check_exists=True
        self.assertEqual(
            self.isogeo.keyword.associate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=True
            ),
            (True, "already done")
        )
        # with check_exists=False
        self.assertEqual(
            self.isogeo.keyword.associate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=False
            ),
            (True, 409)
        )

        # dissociate random_keyword from fixture workgroup
        self.isogeo.keyword.dissociate_workgroup(
            workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=False
        )
        # check random_keyword is actually dissociated from fixture workgroup
        isogeo_workgroup_keywords = self.isogeo.keyword.workgroup(
            workgroup_id=workgroup_test_fixture._id, thesaurus_id=ISOGEO_THESAURUS_ID, whole_results=True
        )
        if isogeo_workgroup_keywords.results and len(isogeo_workgroup_keywords.results):
            self.assertTrue(all(kw_dict.get("_tag") != random_keyword._tag for kw_dict in isogeo_workgroup_keywords.results))
            self.assertTrue(all(kw_dict.get("text") != random_keyword.text for kw_dict in isogeo_workgroup_keywords.results))
            self.assertTrue(all(kw_dict.get("_id") != random_keyword._id for kw_dict in isogeo_workgroup_keywords.results))
        else:
            pass

        # try to dissociate random_keyword from fixture workgroup again
        # with check_exists=True
        self.assertEqual(
            self.isogeo.keyword.dissociate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=True
            ),
            (True, "already done")
        )
        # with check_exists=False
        self.assertEqual(
            self.isogeo.keyword.dissociate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword, check_exists=False
            ),
            (True, 404)
        )

        # set workgroup.areKeywordsRestricted to True for real this time
        workgroup_test_fixture.areKeywordsRestricted = False
        self.isogeo.workgroup.update(workgroup_test_fixture)

    def test_associate_and_dissociate_workgroup_otherThesaurus(self):
        """POST :group/{workgroup_uuid}/keywords/{keyword_uuid}"""

        # pick a random inspire keyword
        random_keyword = Keyword(
            **sample(
                self.isogeo.keyword.thesaurus(
                    thesaurus_id=INSPIRE_THESAURUS_ID, whole_results=True
                ).results,
                1
            )[0]
        )
        # fetch fixture workgroup
        workgroup_test_fixture = self.isogeo.workgroup.get(WORKGROUP_TEST_FIXTURE_UUID)

        # check that it will raise an error trying to associate an inspire keyword
        with self.assertRaises(ValueError):
            self.isogeo.keyword.associate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword
            )
        # check that it will raise an error trying to dissociate an inspire keyword
        with self.assertRaises(ValueError):
            self.isogeo.keyword.dissociate_workgroup(
                workgroup=workgroup_test_fixture, keyword=random_keyword
            )


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
