# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_links
    # for specific
    python -m unittest tests.test_links.TestLinks.test_links_create_basic
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
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Link, Metadata


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
    return "TEST_PySDK - Links {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestLinks(unittest.TestCase):
    """Test Link model of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not environ.get("ISOGEO_API_USER_CLIENT_ID") or not environ.get(
            "ISOGEO_API_USER_CLIENT_SECRET"
        ):
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

        # API connection
        cls.isogeo = IsogeoSession(
            client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
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
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md, check_exists=0
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
        # clean created links
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.links.delete(link=i)

        # clean created metadata
        # cls.isogeo.metadata.delete(cls.metadata_fixture_created._id)
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_links_create_basic(self):
        """POST :resources/{metadata_uuid}/links/}"""
        # var
        link_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create object locally
        link_new_url = Link(
            actions=["download", "other"],
            kind="url",
            title=link_name,
            type="url",
            url="https://pypi.org/project/isogeo-pysdk/",
        )
        # link_new_security = Link(
        #     type="security",
        #     description=link_description,
        #     parent_resource=self.metadata_fixture_created._id,
        # )

        # create it online
        link_new_url = self.isogeo.metadata.links.create(
            metadata=self.metadata_fixture_created, link=link_new_url
        )
        # link_new_security = self.isogeo.metadata.links.create(
        #     metadata=self.metadata_fixture_created, link=link_new_security
        # )

        # checks
        self.assertEqual(link_new_url.type, "url")
        # self.assertEqual(link_new_security.type, "security")
        self.assertEqual(link_new_url.title, link_name)
        # # self.assertEqual(link_new_security.description, link_description)

        self.li_fixtures_to_delete.append(link_new_url)
        # self.li_fixtures_to_delete.append(link_new_security)

    # def test_links_create_with_directive(self):
    #     """POST :resources/{metadata_uuid}/links/}"""
    #     # vars
    #     random_directive = sample(self.isogeo.directive.listing(0), 1)[0]
    #     link_description = "{} - {}".format(get_test_marker(), self.discriminator)

    #     # create object locally
    #     link_new_with_directive = Link(
    #         type="legal",
    #         restriction="patent",
    #         description=link_description,
    #         directive=random_directive,
    #     )

    #     # create it online
    #     link_new_with_directive = self.isogeo.metadata.links.create(
    #         metadata=self.metadata_fixture_created,
    #         link=link_new_with_directive,
    #     )

    #     # add created link to deletion
    #     self.li_fixtures_to_delete.append(link_new_with_directive)

    # -- GET --
    def test_links_kinds_actions_listing(self):
        """GET :link-kinds/}"""
        # retrieve workgroup links
        links_kinds_actions = self.isogeo.metadata.links.kinds_actions()
        self.assertIsInstance(links_kinds_actions, list)

        self.assertEqual(len(links_kinds_actions), 8)

        # parse and test object loader
        for i in links_kinds_actions:
            # load it
            self.assertIsInstance(i, dict)
            # check structure
            self.assertListEqual(sorted(i.keys()), ["actions", "kind", "name"])

    def test_links_listing(self):
        """GET :resources/{metadata_uuid}/links/}"""
        # retrieve workgroup links
        md_links = self.isogeo.metadata.links.listing(self.metadata_fixture_existing)
        # parse and test object loader
        for i in md_links:
            # load it
            link = Link(**i)
            # tests attributes structure
            self.assertTrue(hasattr(link, "_id"))
            self.assertTrue(hasattr(link, "actions"))
            self.assertTrue(hasattr(link, "kind"))
            self.assertTrue(hasattr(link, "size"))
            self.assertTrue(hasattr(link, "title"))
            self.assertTrue(hasattr(link, "type"))
            self.assertTrue(hasattr(link, "url"))

            # tests attributes value
            self.assertEqual(link._id, i.get("_id"))
            self.assertEqual(link.type, i.get("type"))
            self.assertEqual(link.kind, i.get("kind"))

    def test_link_detailed(self):
        """GET :resources/{metadata_uuid}/links/{link_uuid}"""
        # retrieve link
        md_links = self.isogeo.metadata.links.listing(self.metadata_fixture_existing)
        # pick one randomly
        random_link = sample(md_links, 1)[0]
        # get
        online_link = self.isogeo.metadata.links.get(
            metadata_id=self.metadata_fixture_existing._id,
            link_id=random_link.get("_id"),
        )
        # check
        self.assertIsInstance(online_link, Link)

    # # -- PUT/PATCH --
    # def test_links_update(self):
    #     """PUT :resources/{metadata_uuid}/links/{link_uuid}"""
    #     # vars
    #     random_directive = sample(self.isogeo.directive.listing(0), 1)[0]
    #     link_description = "{} - {}".format(get_test_marker(), self.discriminator)

    #     # create object locally
    #     link_new_with_directive = Link(
    #         type="legal",
    #         restriction="patent",
    #         description=link_description,
    #         directive=random_directive,
    #     )

    #     # create it online
    #     link_new_with_directive = self.isogeo.metadata.links.create(
    #         metadata=self.metadata_fixture_created,
    #         link=link_new_with_directive,
    #     )

    #     # modify local object
    #     link_new_with_directive.description = "{} - EDITED DESCRIPTION".format(
    #         get_test_marker()
    #     )

    #     # update the online link
    #     link_fixture_updated = self.isogeo.metadata.links.update(
    #         link_new_with_directive
    #     )

    #     # check if the change is effective
    #     self.assertEqual(
    #         link_fixture_updated.description,
    #         "{} - EDITED DESCRIPTION".format(get_test_marker()),
    #     )

    #     # add created link to deletion
    #     self.li_fixtures_to_delete.append(link_fixture_updated)

    # -- OTHERS --
    def test_links_matrix_cleaner(self):
        """Using the links kind/actions cleaner."""
        cleaned_actions_data = self.isogeo.metadata.links.clean_kind_action_liability(
            link_kind="data", link_actions=["download", "other", "view"]
        )
        self.assertListEqual(cleaned_actions_data, ["download", "other"])


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
