# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_limitations
# for specific
python -m unittest tests.test_limitations.TestLimitations.test_limitations_create_basic
```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import urllib3
import unittest
from os import environ
from pathlib import Path
from random import sample
from socket import gethostname
from sys import _getframe, exit
from time import gmtime, sleep, strftime

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import Isogeo, Limitation, Metadata


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
    return "TEST_PySDK - Limitations {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestLimitations(unittest.TestCase):
    """Test Limitation model of Isogeo API."""

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

        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.metadata_fixture_created = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md
        )
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
        # clean created limitations
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.limitations.delete(limitation=i)

        # clean created metadata
        cls.isogeo.metadata.delete(cls.metadata_fixture_created._id)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_limitations_create_basic(self):
        """POST :resources/{metadata_uuid}/limitations/}"""
        # var
        limitation_description = "{} - {}".format(get_test_marker(), self.discriminator)

        # create object locally
        limitation_new_legal = Limitation(
            type="legal", restriction="patent", description=limitation_description
        )
        limitation_new_security = Limitation(
            type="security",
            description=limitation_description,
            parent_resource=self.metadata_fixture_created._id,
        )

        # create it online
        limitation_new_legal = self.isogeo.metadata.limitations.create(
            metadata=self.metadata_fixture_created, limitation=limitation_new_legal
        )
        limitation_new_security = self.isogeo.metadata.limitations.create(
            metadata=self.metadata_fixture_created, limitation=limitation_new_security
        )

        # checks
        self.assertEqual(limitation_new_legal.type, "legal")
        self.assertEqual(limitation_new_security.type, "security")
        self.assertEqual(limitation_new_legal.description, limitation_description)
        # self.assertEqual(limitation_new_security.description, limitation_description)

        self.li_fixtures_to_delete.append(limitation_new_legal)
        self.li_fixtures_to_delete.append(limitation_new_security)

    def test_limitations_create_with_directive(self):
        """POST :resources/{metadata_uuid}/limitations/}"""
        # vars
        random_directive = sample(self.isogeo.directive.listing(0), 1)[0]
        limitation_description = "{} - {}".format(get_test_marker(), self.discriminator)

        # create object locally
        limitation_new_with_directive = Limitation(
            type="legal",
            restriction="patent",
            description=limitation_description,
            directive=random_directive,
        )

        # create it online
        limitation_new_with_directive = self.isogeo.metadata.limitations.create(
            metadata=self.metadata_fixture_created,
            limitation=limitation_new_with_directive,
        )

        # add created limitation to deletion
        self.li_fixtures_to_delete.append(limitation_new_with_directive)

    # -- GET --
    def test_limitations_listing(self):
        """GET :resources/{metadata_uuid}/limitations/}"""
        # retrieve workgroup limitations
        md_limitations = self.isogeo.metadata.limitations.listing(
            self.metadata_fixture_existing
        )
        # parse and test object loader
        for i in md_limitations:
            # load it
            limitation = Limitation(**i)
            # tests attributes structure
            self.assertTrue(hasattr(limitation, "_id"))
            self.assertTrue(hasattr(limitation, "description"))
            self.assertTrue(hasattr(limitation, "directive"))
            self.assertTrue(hasattr(limitation, "type"))

            # tests attributes value
            self.assertEqual(limitation._id, i.get("_id"))
            self.assertEqual(limitation.directive, i.get("directive"))
            self.assertEqual(limitation.type, i.get("type"))

    def test_limitation_detailed(self):
        """GET :resources/{metadata_uuid}/limitations/{limitation_uuid}"""
        # retrieve limitation
        md_limitations = self.isogeo.metadata.limitations.listing(
            self.metadata_fixture_existing
        )
        # pick one randomly
        random_limitation = sample(md_limitations, 1)[0]
        # get
        online_limitation = self.isogeo.metadata.limitations.get(
            metadata_id=self.metadata_fixture_existing._id,
            limitation_id=random_limitation.get("_id"),
        )
        # check
        self.assertIsInstance(online_limitation, Limitation)

    # -- PUT/PATCH --
    def test_limitations_update(self):
        """PUT :resources/{metadata_uuid}/limitations/{limitation_uuid}"""
        # vars
        random_directive = sample(self.isogeo.directive.listing(0), 1)[0]
        limitation_description = "{} - {}".format(get_test_marker(), self.discriminator)

        # create object locally
        limitation_new_with_directive = Limitation(
            type="legal",
            restriction="patent",
            description=limitation_description,
            directive=random_directive,
        )

        # create it online
        limitation_new_with_directive = self.isogeo.metadata.limitations.create(
            metadata=self.metadata_fixture_created,
            limitation=limitation_new_with_directive,
        )

        # modify local object
        limitation_new_with_directive.description = "{} - EDITED DESCRIPTION".format(
            get_test_marker()
        )

        # update the online limitation
        limitation_fixture_updated = self.isogeo.metadata.limitations.update(
            limitation_new_with_directive
        )

        # check if the change is effective
        self.assertEqual(
            limitation_fixture_updated.description,
            "{} - EDITED DESCRIPTION".format(get_test_marker()),
        )

        # add created limitation to deletion
        self.li_fixtures_to_delete.append(limitation_fixture_updated)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
