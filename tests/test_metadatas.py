# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_metadatas
# for specific
python -m unittest tests.test_metadatas.TestMetadatas.test_metadatas_create
```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import uuid
import unittest
from os import environ
from pathlib import Path
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv
import urllib3

# module target
from isogeo_pysdk import Isogeo, IsogeoUtils, Metadata, Workgroup

# #############################################################################
# ######## Globals #################
# ##################################

utils = IsogeoUtils()

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
    """Returns the function name."""
    return "TEST_PySDK - Metadatas - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestMetadatas(unittest.TestCase):
    """Test Metadata model of Isogeo API."""

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

        # fixture metadata
        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.fixture_metadata = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md
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
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created metadata
        cls.isogeo.metadata.delete(cls.fixture_metadata._id)

        # clean created metadatas
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.delete(metadata_id=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- MODEL --
    def test_metadatas_title_or_name(self):
        """Model integrated method to retrive title or name."""
        # title but no name
        md_title_no_name = Metadata(
            title="BD Topo® - My title really inspires the masses - Villenave d'Ornon"
        )
        self.assertEqual(
            md_title_no_name.title_or_name(),
            "BD Topo® - My title really inspires the masses - Villenave d'Ornon",
        )
        self.assertEqual(
            md_title_no_name.title_or_name(1),
            "bd-topo-my-title-really-inspires-the-masses-villenave-dornon",
        )

        # no title but name - 1
        md_no_title_name = Metadata(name="reference.roads_primary")
        self.assertEqual(md_no_title_name.title_or_name(), "reference.roads_primary")

        # no title but name - 2
        md_no_title_name = Metadata(name="reference chemins de forêt.shp")
        self.assertEqual(
            md_no_title_name.title_or_name(1), "reference-chemins-de-foretshp"
        )

        # no title nor name
        md_no_title_no_name = Metadata()
        self.assertIsNone(md_no_title_no_name.title_or_name(0))
        self.assertIsNone(md_no_title_no_name.title_or_name(1))

    # -- GET --
    def test_metadatas_exists(self):
        """GET :resources/{metadata_uuid}"""
        # must be true
        exists = self.isogeo.metadata.exists(resource_id=self.fixture_metadata._id)
        self.assertIsInstance(exists, bool)
        self.assertEqual(exists, True)

        # must be false
        fake_uuid = uuid.uuid4()
        exists = self.isogeo.metadata.exists(resource_id=fake_uuid.hex)
        self.assertIsInstance(exists, bool)
        self.assertEqual(exists, False)

    def test_metadatas_in_search_results(self):
        """GET :resources/search."""
        search = self.isogeo.search(include="all")
        if isinstance(search, tuple):
            logging.warning(
                "Search request failed: {} - {}".format(search[0], search[1])
            )
            return
        for md in search.results:
            metadata = Metadata.clean_attributes(md)
            # compare values
            self.assertEqual(md.get("_id"), metadata._id)
            self.assertEqual(md.get("_created"), metadata._created)
            self.assertEqual(md.get("modified"), metadata.modified)
            self.assertEqual(md.get("created"), metadata.created)
            self.assertEqual(md.get("modified"), metadata.modified)

            # -- HELPERS
            # dates
            md_date_creation = utils.hlpr_datetimes(metadata._created)
            self.assertEqual(int(metadata._created[:4]), md_date_creation.year)
            md_date_modification = utils.hlpr_datetimes(metadata._modified)
            self.assertEqual(int(metadata._modified[:4]), md_date_modification.year)
            if metadata.created:
                ds_date_creation = utils.hlpr_datetimes(metadata.created)
                self.assertEqual(int(metadata.created[:4]), ds_date_creation.year)

            # admin url
            self.assertIsInstance(metadata.admin_url(self.isogeo.app_url), str)

            # group name and _id
            self.assertIsInstance(metadata.groupName, str)
            self.assertIsInstance(metadata.groupId, str)
            group = self.isogeo.workgroup.get(metadata.groupId, include=())
            self.assertIsInstance(group, Workgroup)
            self.assertEqual(metadata.groupId, group._id)
            self.assertEqual(metadata.groupName, group.name)

    # def test_search_specific_mds_bad(self):
    #     """Searches filtering on specific metadata."""
    #     # get random metadata within a small search
    #     search = self.isogeo.metadata.search(
    #         page_size=5,
    #         # whole_results=0
    #     )
    #     metadata_id = sample(search.results, 1)[0].get("_id")

    #     # # pass metadata UUID
    #     # with self.assertRaises(TypeError):
    #     #     self.isogeo.search(self.bearer,
    #     #                         page_size=0,
    #     #                         whole_results=0,
    #     #                         specific_md=md)

    def test_metadatas_get_detailed(self):
        """GET :resources/{metadata_uuid}"""
        # retrieve fixture metadata
        metadata = self.isogeo.metadata.get(METADATA_TEST_FIXTURE_UUID, include="all")
        # check object
        self.assertIsInstance(metadata, Metadata)
        # check attributes
        self.assertTrue(hasattr(metadata, "_id"))
        self.assertTrue(hasattr(metadata, "_created"))
        self.assertTrue(hasattr(metadata, "_creator"))
        self.assertTrue(hasattr(metadata, "_modified"))
        self.assertTrue(hasattr(metadata, "abstract"))
        self.assertTrue(hasattr(metadata, "created"))
        self.assertTrue(hasattr(metadata, "modified"))
        # specific to implementation
        self.assertTrue(hasattr(metadata, "groupId"))
        self.assertTrue(hasattr(metadata, "groupName"))

        # check method to dict
        md_as_dict = metadata.to_dict()
        self.assertIsInstance(md_as_dict, dict)
        # compare values
        self.assertEqual(md_as_dict.get("_id"), metadata._id)
        self.assertEqual(md_as_dict.get("_created"), metadata._created)
        self.assertEqual(md_as_dict.get("modified"), metadata.modified)
        self.assertEqual(md_as_dict.get("created"), metadata.created)
        self.assertEqual(md_as_dict.get("modified"), metadata.modified)
