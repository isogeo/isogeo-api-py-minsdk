# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

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
from isogeo_pysdk import Isogeo, Metadata, Specification


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
    """Returns the function name."""
    return "TEST_PySDK - Specifications - {}".format(_getframe(1).f_code.co_name)


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

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created metadata
        cls.isogeo.metadata.delete(cls.fixture_metadata._id)

        # clean created specifications
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.specification.delete(
                    workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, specification_id=i
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
        specification_new = self.isogeo.specification.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            specification=specification_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(specification_new.name, specification_name)
        self.assertTrue(self.isogeo.specification.exists(specification_new._id))

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
        specification_new = self.isogeo.specification.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            specification=specification_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(
            specification_new.name,
            "{} - {}".format(get_test_marker(), self.discriminator),
        )
        self.assertTrue(self.isogeo.specification.exists(specification_new._id))

        # add created specification to deletion
        self.li_fixtures_to_delete.append(specification_new._id)

    def test_specifications_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/specifications/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        specification_local = Specification(name=name_to_be_unique)

        # create it online
        specification_new_1 = self.isogeo.specification.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            specification=specification_local,
            check_exists=0,
        )

        # try to create a specification with the same name
        specification_new_2 = self.isogeo.specification.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            specification=specification_local,
            check_exists=1,
        )

        # check if object has not been created
        self.assertEqual(specification_new_2, False)

        # add created specification to deletion
        self.li_fixtures_to_delete.append(specification_new_1._id)

    def test_specifications_association(self):
        """POST :resources/{metadata_uuid}/specifications/"""
        # retrieve workgroup specifications
        wg_specifications = self.isogeo.specification.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=0
        )

        # pick one
        specification_isogeo = Specification(**sample(wg_specifications, 1)[0])

        # associate it
        self.isogeo.specification.associate_metadata(
            metadata=self.fixture_metadata,
            specification=specification_isogeo,
            conformity=1,
        )

        # refresh fixture metadata
        self.fixture_metadata = self.isogeo.metadata.get(
            metadata_id=self.fixture_metadata._id, include=("specifications",)
        )

        # try to associate the same specification = error
        self.isogeo.specification.associate_metadata(
            metadata=self.fixture_metadata,
            specification=specification_isogeo,
            conformity=1,
        )

        # # -- dissociate
        # refresh fixture metadata
        self.fixture_metadata = self.isogeo.metadata.get(
            metadata_id=self.fixture_metadata._id, include=("specifications",)
        )
        for specification in self.fixture_metadata.specifications:
            self.isogeo.specification.dissociate_metadata(
                metadata=self.fixture_metadata,
                specification_id=specification.get("specification").get("_id"),
            )

    # -- GET --
    def test_specifications_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/specifications}"""
        # retrieve workgroup specifications
        wg_specifications = self.isogeo.specification.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
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
        wg_specifications = self.isogeo.specification.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=0
        )

        # split 'isogeo' specifications from workgroup specifications
        li_specifications_isogeo = [
            specification
            for specification in wg_specifications
            if "isogeo" in specification.get("_tag")
        ]
        li_specifications_workgroup = [
            specification
            for specification in wg_specifications
            if "isogeo" not in specification.get("_tag")
        ]

        # pick two licenses: one locked by Isogeo, one workgroup specific
        specification_isogeo = sample(li_specifications_isogeo, 1)[0]
        specification_specific = sample(li_specifications_workgroup, 1)[0]

        # check both exist
        self.assertTrue(
            self.isogeo.specification.exists(specification_isogeo.get("_id"))
        )
        self.assertTrue(
            self.isogeo.specification.exists(specification_specific.get("_id"))
        )

        # get and check both
        specification_isogeo = self.isogeo.specification.get(
            specification_isogeo.get("_id")
        )
        specification_specific = self.isogeo.specification.get(
            specification_specific.get("_id")
        )
        # check object
        self.assertIsInstance(specification_isogeo, Specification)
        self.assertIsInstance(specification_specific, Specification)

        # check isLocked status
        self.assertTrue(specification_isogeo.isLocked)
        self.assertFalse(specification_specific.isLocked)

    # -- PUT/PATCH --
    def test_specifications_update(self):
        """PUT :groups/{workgroup_uuid}/specifications/{specification_uuid}}"""
        # create a new specification
        specification_fixture = Specification(
            name="{} - {}".format(get_test_marker(), self.discriminator)
        )
        specification_fixture = self.isogeo.specification.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
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
        specification_fixture = self.isogeo.specification.update(specification_fixture)

        # check if the change is effective
        specification_fixture_updated = self.isogeo.specification.get(
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
