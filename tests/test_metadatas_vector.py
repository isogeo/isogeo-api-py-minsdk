# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

    :Example:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_metadatas_vector
        # for specific
        python -m unittest tests.test_metadatas_vector.TestMetadatasVector.test_metadatas_create

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
METADATA_TEST_FIXTURE_UUID_ML = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE_ML")
WORKGROUP_TEST_FIXTURE_UUID_ML = environ.get("ISOGEO_WORKGROUP_TEST_UUID_ML")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name."""
    return "TEST_PySDK - Metadatas - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestMetadatasVector(unittest.TestCase):
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
        if environ.get("ISOGEO_PLATFORM").lower() in ["qa", "custom"]:
            urllib3.disable_warnings()

        # API connection
        if environ.get("ISOGEO_PLATFORM").lower() == "custom":
            isogeo_urls = {
                "api_url": environ.get("ISOGEO_API_URL")
            }
            cls.isogeo = Isogeo(
                client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
                client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
                auth_mode="user_legacy",
                auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
                platform=environ.get("ISOGEO_PLATFORM").lower(),
                isogeo_urls=isogeo_urls
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
        cls.isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )

        # fixture metadata
        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.fixture_metadata = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md
        )
        md.abstract = get_test_marker()
        cls.fixture_metadata_ml = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID_ML, metadata=md, lang="fr"
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
        cls.isogeo.metadata.delete(cls.fixture_metadata_ml._id)

        # clean created metadatas
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.delete(metadata_id=i)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- MODEL --
    def test_metadatas_title_or_name(self):
        """Model integrated method to retrieve title or name."""
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
        search = self.isogeo.search(group=WORKGROUP_TEST_FIXTURE_UUID, include="all")
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

    def test_metadatas_get_detailed_multilingual(self):
        """GET :resources/{metadata_uuid}"""
        # retrieve fixture metadata
        metadata = self.isogeo.metadata.get(
            METADATA_TEST_FIXTURE_UUID_ML, include="all"
        )
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
        # specific to multilingualism
        self.assertTrue(hasattr(metadata, "_fieldsLanguage"))
        self.assertTrue(hasattr(metadata, "translations"))
        self.assertIsInstance(metadata.translations, list)
        self.assertEqual(len(metadata.translations), 3)
        self.assertTrue(
            all(
                all(
                    key in trans for key in ["languageCode", "title", "abstract"]
                ) and all(
                    len(trans.get(key)) for key in ["languageCode", "title", "abstract"]
                ) for trans in metadata.translations
            )
        )
        # check method to dict
        md_as_dict = metadata.to_dict()
        self.assertIsInstance(md_as_dict, dict)
        # compare values
        self.assertEqual(md_as_dict.get("_id"), metadata._id)
        self.assertEqual(md_as_dict.get("_created"), metadata._created)
        self.assertEqual(md_as_dict.get("modified"), metadata.modified)
        self.assertEqual(md_as_dict.get("created"), metadata.created)
        self.assertEqual(md_as_dict.get("modified"), metadata.modified)

    def test_metadatas_get_detailed_multilingual_fr(self):
        """GET :resources/{metadata_uuid}"""
        # retrieve fixture metadata
        lang_code = "fr"
        expected_title = "Fiche complète"
        expected_abstract = "Résumé en français"
        metadata = self.isogeo.metadata.get(
            METADATA_TEST_FIXTURE_UUID_ML, include="all", lang=lang_code
        )

        self.assertEqual(metadata.title, expected_title)
        self.assertEqual(metadata.abstract, expected_abstract)
        self.assertEqual(metadata._fieldsLanguage, lang_code)
        translation = [
            trans for trans in metadata.translations
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)

    def test_metadatas_get_detailed_multilingual_en(self):
        """GET :resources/{metadata_uuid}"""
        # retrieve fixture metadata
        lang_code = "en"
        expected_title = "Title in english"
        expected_abstract = "English summary"
        metadata = self.isogeo.metadata.get(
            METADATA_TEST_FIXTURE_UUID_ML, include="all", lang=lang_code
        )

        self.assertEqual(metadata.title, expected_title)
        self.assertEqual(metadata.abstract, expected_abstract)
        self.assertEqual(metadata._fieldsLanguage, lang_code)
        translation = [
            trans for trans in metadata.translations
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)

    def test_metadatas_get_detailed_multilingual_es(self):
        """GET :resources/{metadata_uuid}"""
        # retrieve fixture metadata
        lang_code = "es"
        expected_title = "Hoja de metadatos completa"
        expected_abstract = "Resumen en español"
        metadata = self.isogeo.metadata.get(
            METADATA_TEST_FIXTURE_UUID_ML, include="all", lang=lang_code
        )

        self.assertEqual(metadata.title, expected_title)
        self.assertEqual(metadata.abstract, expected_abstract)
        self.assertEqual(metadata._fieldsLanguage, lang_code)
        translation = [
            trans for trans in metadata.translations
            if trans.get("languageCode") == lang_code
        ][0]
        self.assertEqual(translation.get("title"), expected_title)
        self.assertEqual(translation.get("abstract"), expected_abstract)

    def test_metadatas_create_basic(self):
        """POST :groups/{group_uuid}/resources"""
        # initiate metadata local object
        metadata_toCreate = Metadata(type="vectorDataset")
        metadata_title = "{} - {}".format(get_test_marker(), self.discriminator)
        workgroup_id = WORKGROUP_TEST_FIXTURE_UUID

        # assert ValueError is raised because there is no title
        with self.assertRaises(ValueError):
            self.isogeo.metadata.create(
                workgroup_id=workgroup_id,
                metadata=metadata_toCreate
            )

        # add a title to local object
        metadata_toCreate.title = metadata_title

        # create it online
        created_metadata = self.isogeo.metadata.create(
            workgroup_id=workgroup_id,
            metadata=metadata_toCreate
        )

        # checks
        self.assertIsInstance(created_metadata, Metadata)

        self.assertTrue(hasattr(created_metadata, "_id"))
        self.assertIsNot(created_metadata._id, None)
        self.assertIsInstance(created_metadata._id, str)
        self.assertIsNot(len(created_metadata._id), 0)

        self.li_fixtures_to_delete.append(created_metadata._id)

        self.assertTrue(hasattr(created_metadata, "_created"))
        self.assertIsNot(created_metadata._created, None)
        self.assertIsInstance(created_metadata._created, str)
        self.assertIsNot(len(created_metadata._created), 0)

        self.assertTrue(hasattr(created_metadata, "_creator"))
        self.assertIsNot(created_metadata._creator, None)
        self.assertIsInstance(created_metadata._creator, dict)
        self.assertIsNot(len(created_metadata._creator), 0)

        self.assertTrue(hasattr(created_metadata, "_modified"))
        self.assertIsNot(created_metadata._modified, None)
        self.assertIsInstance(created_metadata._modified, str)
        self.assertIsNot(len(created_metadata._modified), 0)

        self.assertEqual(created_metadata.editionProfile, "manual")
        self.assertEqual(created_metadata.title, metadata_title)

    def test_metadatas_create_complete(self):
        """POST :groups/{group_uuid}/resources"""
        # initiate metadata local object
        metadata_toCreate = Metadata(type="vectorDataset")
        metadata_title = "{} - {}".format(get_test_marker(), self.discriminator)
        workgroup_id = WORKGROUP_TEST_FIXTURE_UUID

        # assert ValueError is raised because there is no title
        with self.assertRaises(ValueError):
            self.isogeo.metadata.create(
                workgroup_id=workgroup_id,
                metadata=metadata_toCreate,
                return_basic_or_complete=1
            )

        # add a title to local object
        metadata_toCreate.title = metadata_title

        # create it online
        created_metadata = self.isogeo.metadata.create(
            workgroup_id=workgroup_id,
            metadata=metadata_toCreate,
            return_basic_or_complete=1
        )

        # checks
        self.assertIsInstance(created_metadata, Metadata)

        self.assertTrue(hasattr(created_metadata, "_id"))
        self.assertIsNot(created_metadata._id, None)
        self.assertIsInstance(created_metadata._id, str)
        self.assertIsNot(len(created_metadata._id), 0)

        self.li_fixtures_to_delete.append(created_metadata._id)

        self.assertTrue(hasattr(created_metadata, "_created"))
        self.assertIsNot(created_metadata._created, None)
        self.assertIsInstance(created_metadata._created, str)
        self.assertIsNot(len(created_metadata._created), 0)

        self.assertTrue(hasattr(created_metadata, "_creator"))
        self.assertIsNot(created_metadata._creator, None)
        self.assertIsInstance(created_metadata._creator, dict)
        self.assertIsNot(len(created_metadata._creator), 0)

        self.assertTrue(hasattr(created_metadata, "_modified"))
        self.assertIsNot(created_metadata._modified, None)
        self.assertIsInstance(created_metadata._modified, str)
        self.assertIsNot(len(created_metadata._modified), 0)

        self.assertTrue(hasattr(created_metadata, "groupId"))
        self.assertIsNot(created_metadata.groupId, None)
        self.assertIsInstance(created_metadata.groupId, str)
        self.assertEqual(created_metadata.groupId, created_metadata._creator.get("_id"))

        self.assertTrue(hasattr(created_metadata, "groupName"))
        self.assertIsNot(created_metadata.groupName, None)
        self.assertIsInstance(created_metadata.groupName, str)
        self.assertEqual(created_metadata.groupName, created_metadata._creator.get("contact").get("name"))

        self.assertEqual(created_metadata.editionProfile, "manual")

        self.assertEqual(created_metadata.title, metadata_title)

    def test_metadatas_create_basic_multilingual(self):
        """POST :groups/{group_uuid}/resources"""
        # initiate metadata local object
        metadata_title = "{} - {}".format(get_test_marker(), self.discriminator)
        metadata_abstract = f"{metadata_title} ABSTRACT"
        metadata_toCreate = Metadata(type="vectorDataset", abstract=metadata_abstract)
        workgroup_id = WORKGROUP_TEST_FIXTURE_UUID_ML
        lang_code = "fr"

        # assert ValueError is raised because there is no title
        with self.assertRaises(ValueError):
            self.isogeo.metadata.create(
                workgroup_id=workgroup_id,
                metadata=metadata_toCreate,
                lang=lang_code
            )

        # add a title to local object
        metadata_toCreate.title = metadata_title
        # create it online
        created_metadata = self.isogeo.metadata.create(
            workgroup_id=workgroup_id,
            metadata=metadata_toCreate,
            lang=lang_code
        )
        # fetch it with translations
        created_metadata_with_translations = self.isogeo.metadata.get(
            metadata_id=created_metadata._id,
            lang=lang_code,
            include=("translations",)
        )

        # checks
        self.assertIsInstance(created_metadata, Metadata)

        self.assertTrue(hasattr(created_metadata, "_id"))
        self.assertIsNot(created_metadata._id, None)
        self.assertIsInstance(created_metadata._id, str)
        self.assertIsNot(len(created_metadata._id), 0)

        self.li_fixtures_to_delete.append(created_metadata._id)

        self.assertTrue(hasattr(created_metadata, "_created"))
        self.assertIsNot(created_metadata._created, None)
        self.assertIsInstance(created_metadata._created, str)
        self.assertIsNot(len(created_metadata._created), 0)

        self.assertTrue(hasattr(created_metadata, "_creator"))
        self.assertIsNot(created_metadata._creator, None)
        self.assertIsInstance(created_metadata._creator, dict)
        self.assertIsNot(len(created_metadata._creator), 0)

        self.assertTrue(hasattr(created_metadata, "_modified"))
        self.assertIsNot(created_metadata._modified, None)
        self.assertIsInstance(created_metadata._modified, str)
        self.assertIsNot(len(created_metadata._modified), 0)

        self.assertEqual(created_metadata.editionProfile, "manual")
        self.assertEqual(created_metadata.title, metadata_title)
        self.assertEqual(created_metadata.abstract, metadata_abstract)

        self.assertEqual(created_metadata_with_translations._fieldsLanguage, lang_code)
        self.assertTrue(hasattr(created_metadata_with_translations, "translations"))
        self.assertIsNot(created_metadata_with_translations.translations, None)
        self.assertIsInstance(created_metadata_with_translations.translations, list)
        self.assertIsNot(len(created_metadata_with_translations.translations), 0)
        self.assertTrue(
            any(
                trans.get("languageCode") == lang_code and trans.get("title") == metadata_title and trans.get("abstract") == metadata_abstract
                for trans in created_metadata_with_translations.translations
            )
        )

    def test_metadatas_create_complete_multilingual(self):
        """POST :groups/{group_uuid}/resources"""
        # initiate metadata local object
        metadata_title = "{} - {}".format(get_test_marker(), self.discriminator)
        metadata_abstract = f"{metadata_title} ABSTRACT"
        metadata_toCreate = Metadata(type="vectorDataset", abstract=metadata_abstract)
        workgroup_id = WORKGROUP_TEST_FIXTURE_UUID_ML
        lang_code = "fr"

        # assert ValueError is raised because there is no title
        with self.assertRaises(ValueError):
            self.isogeo.metadata.create(
                workgroup_id=workgroup_id,
                metadata=metadata_toCreate,
                return_basic_or_complete=2,
                lang=lang_code
            )

        # add a title to local object
        metadata_toCreate.title = metadata_title

        # create it online
        created_metadata = self.isogeo.metadata.create(
            workgroup_id=workgroup_id,
            metadata=metadata_toCreate,
            return_basic_or_complete=2,
            lang=lang_code
        )

        # checks
        self.assertIsInstance(created_metadata, Metadata)

        self.assertTrue(hasattr(created_metadata, "_id"))
        self.assertIsNot(created_metadata._id, None)
        self.assertIsInstance(created_metadata._id, str)
        self.assertIsNot(len(created_metadata._id), 0)

        self.li_fixtures_to_delete.append(created_metadata._id)

        self.assertTrue(hasattr(created_metadata, "_created"))
        self.assertIsNot(created_metadata._created, None)
        self.assertIsInstance(created_metadata._created, str)
        self.assertIsNot(len(created_metadata._created), 0)

        self.assertTrue(hasattr(created_metadata, "_creator"))
        self.assertIsNot(created_metadata._creator, None)
        self.assertIsInstance(created_metadata._creator, dict)
        self.assertIsNot(len(created_metadata._creator), 0)

        self.assertTrue(hasattr(created_metadata, "_modified"))
        self.assertIsNot(created_metadata._modified, None)
        self.assertIsInstance(created_metadata._modified, str)
        self.assertIsNot(len(created_metadata._modified), 0)

        self.assertTrue(hasattr(created_metadata, "groupId"))
        self.assertIsNot(created_metadata.groupId, None)
        self.assertIsInstance(created_metadata.groupId, str)
        self.assertEqual(created_metadata.groupId, created_metadata._creator.get("_id"))

        self.assertTrue(hasattr(created_metadata, "groupName"))
        self.assertIsNot(created_metadata.groupName, None)
        self.assertIsInstance(created_metadata.groupName, str)
        self.assertEqual(created_metadata.groupName, created_metadata._creator.get("contact").get("name"))

        self.assertEqual(created_metadata.editionProfile, "manual")
        self.assertEqual(created_metadata.title, metadata_title)
        self.assertEqual(created_metadata.abstract, metadata_abstract)

        self.assertEqual(created_metadata._fieldsLanguage, lang_code)
        self.assertTrue(hasattr(created_metadata, "translations"))
        self.assertIsNot(created_metadata.translations, None)
        self.assertIsInstance(created_metadata.translations, list)
        self.assertIsNot(len(created_metadata.translations), 0)
        self.assertTrue(
            any(
                trans.get("languageCode") == lang_code and trans.get("title") == metadata_title and trans.get("abstract") == metadata_abstract
                for trans in created_metadata.translations
            )
        )

    def test_metadatas_update(self):
        """PUT :resources/{metadata_uuid}"""
        # retrieve fixture metadata
        metadata_toUpdate = self.isogeo.metadata.get(self.fixture_metadata._id)
        self.assertIsInstance(metadata_toUpdate, Metadata)

        # update object attributes values
        metadata_toUpdate.abstract = "Test abstract"
        metadata_toUpdate.geometry = "Point"

        # update metadata and check return
        self.assertIsInstance(
            self.isogeo.metadata.update(metadata=metadata_toUpdate), Metadata
        )

        # get the metadata updated
        updated_metadata = self.isogeo.metadata.get(
            self.fixture_metadata._id, include="all"
        )
        # check return
        self.assertIsInstance(updated_metadata, Metadata)

        # updated attributes
        self.assertEqual(updated_metadata.abstract, "Test abstract")
        self.assertEqual(updated_metadata.geometry, "Point")

    def test_metadatas_update_multilingual(self):
        """PUT :resources/{metadata_uuid}"""
        # retrieve fixture metadata
        metadata_toUpdate = self.isogeo.metadata.get(
            self.fixture_metadata_ml._id, ("translations",), "fr"
        )
        self.assertIsInstance(metadata_toUpdate, Metadata)
        self.assertEqual(metadata_toUpdate._fieldsLanguage, "fr")
        self.assertEqual(metadata_toUpdate.title, self.fixture_metadata_ml.title)
        french_translations = [
            trans for trans in metadata_toUpdate.translations
            if trans.get("languageCode") == "fr"
        ]
        self.assertEqual(len(french_translations), 1)
        french_translation = french_translations[0]
        self.assertEqual(french_translation.get("title"), self.fixture_metadata_ml.title)

        # FRENCH
        french_abstract = "Résumé en français"
        # update object attributes values
        metadata_toUpdate.abstract = french_abstract
        # update metadata and check return
        self.assertIsInstance(
            self.isogeo.metadata.update(metadata=metadata_toUpdate, _http_method="PUT", lang="fr"), Metadata
        )
        # get the metadata updated
        updated_metadata = self.isogeo.metadata.get(
            metadata_toUpdate._id, include=("translations",), lang="fr"
        )
        # check return
        self.assertIsInstance(updated_metadata, Metadata)
        # updated attributes
        self.assertEqual(updated_metadata.title, self.fixture_metadata_ml.title)
        self.assertEqual(updated_metadata.abstract, french_abstract)
        # multilingualism attributes
        self.assertEqual(updated_metadata._fieldsLanguage, "fr")
        french_translations = [
            trans for trans in updated_metadata.translations
            if trans.get("languageCode") == "fr"
        ]
        self.assertEqual(len(french_translations), 1)
        french_translation = french_translations[0]
        self.assertEqual(french_translation.get("title"), self.fixture_metadata_ml.title)
        self.assertEqual(french_translation.get("abstract"), french_abstract)

        # SPANISH
        spanish_title = "Título en español"
        # update object attributes values
        metadata_toUpdate.title = spanish_title
        metadata_toUpdate.abstract = None
        metadata_toUpdate.geometry = "Point"
        # update metadata and check return
        self.assertIsInstance(
            self.isogeo.metadata.update(metadata=metadata_toUpdate, _http_method="PUT", lang="es"), Metadata
        )
        # get the metadata updated
        updated_metadata = self.isogeo.metadata.get(
            metadata_toUpdate._id, include=("translations",), lang="es"
        )
        # check return
        self.assertIsInstance(updated_metadata, Metadata)
        # updated attributes
        self.assertEqual(updated_metadata.title, spanish_title)
        self.assertEqual(updated_metadata.geometry, "Point")
        # multilingualism attributes
        self.assertEqual(updated_metadata._fieldsLanguage, "es")
        spanish_translations = [
            trans for trans in updated_metadata.translations
            if trans.get("languageCode") == "es"
        ]
        self.assertEqual(len(spanish_translations), 1)
        spanish_translation = spanish_translations[0]
        self.assertEqual(spanish_translation.get("title"), spanish_title)
        self.assertIsNone(spanish_translation.get("abstract"))

        # ENGLISH
        english_title = "Title in English"
        english_abstract = "English summary"
        # update object attributes values
        metadata_toUpdate.title = english_title
        metadata_toUpdate.abstract = english_abstract
        metadata_toUpdate.features = 55
        # update metadata and check return
        self.assertIsInstance(
            self.isogeo.metadata.update(metadata=metadata_toUpdate, _http_method="PUT", lang="en"), Metadata
        )
        # get the metadata updated
        updated_metadata = self.isogeo.metadata.get(
            metadata_toUpdate._id, include=("translations",), lang="en"
        )
        # check return
        self.assertIsInstance(updated_metadata, Metadata)
        # updated attributes
        self.assertEqual(updated_metadata.title, english_title)
        self.assertEqual(updated_metadata.abstract, english_abstract)
        self.assertEqual(updated_metadata.features, 55)
        # multilingualism attributes
        self.assertEqual(updated_metadata._fieldsLanguage, "en")
        english_translations = [
            trans for trans in updated_metadata.translations
            if trans.get("languageCode") == "en"
        ]
        self.assertEqual(len(english_translations), 1)
        english_translation = english_translations[0]
        self.assertEqual(english_translation.get("title"), english_title)
        self.assertEqual(english_translation.get("abstract"), english_abstract)

        # final check
        self.assertEqual(len(updated_metadata.translations), 3)
