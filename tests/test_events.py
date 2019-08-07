# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_events
    # for specific
    python -m unittest tests.test_events.TestEvents.test_events_create_basic
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
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Event, Metadata


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
    return "TEST_PySDK - Events {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestEvents(unittest.TestCase):
    """Test Event model of Isogeo API."""

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
        # clean created metadata
        cls.isogeo.metadata.delete(cls.metadata_fixture_created._id)
        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.metadata.events.delete(event=i)
                pass
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_events_create_basic(self):
        """POST :groups/{workgroup_uuid}/events/}"""
        # var
        event_date = strftime("%Y-%m-%d", gmtime())
        event_kind_creation = "creation"
        event_kind_update = "update"
        event_description = "{} - {}".format(get_test_marker(), self.discriminator)

        # create object locally
        event_new_creation = Event(
            date=event_date,
            kind=event_kind_creation,
            description=event_description,
            parent_resource=self.metadata_fixture_created._id,
        )
        event_new_update = Event(
            date=event_date,
            kind=event_kind_update,
            description=event_description,
            parent_resource=self.metadata_fixture_created._id,
        )

        # create it online
        event_new_creation = self.isogeo.metadata.events.create(
            metadata=self.metadata_fixture_created, event=event_new_creation
        )
        event_new_update = self.isogeo.metadata.events.create(
            metadata=self.metadata_fixture_created, event=event_new_update
        )

        # checks
        self.assertEqual(event_new_creation.kind, event_kind_creation)
        self.assertEqual(event_new_update.kind, event_kind_update)
        self.assertEqual(event_new_creation.description, None)
        self.assertEqual(event_new_update.description, event_description)

    # def test_events_create_checking_name(self):
    #     """POST :groups/{workgroup_uuid}/events/}"""
    #     # vars
    #     name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

    #     # create local object
    #     event_local = Event(name=name_to_be_unique)

    #     # create it online
    #     event_new_1 = self.isogeo.event.event_create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, event=event_local, check_exists=0
    #     )

    #     # try to create a event with the same name
    #     event_new_2 = self.isogeo.event.event_create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, event=event_local, check_exists=1
    #     )

    #     # check if object has not been created
    #     self.assertEqual(event_new_2, False)

    #     # add created event to deletion
    #     self.li_fixtures_to_delete.append(event_new_1._id)

    # -- GET --
    def test_events_listing(self):
        """GET :resources/{metadata_uuid}/events/}"""
        # retrieve workgroup events
        md_events = self.isogeo.metadata.events.listing(self.metadata_fixture_existing)
        # parse and test object loader
        for i in md_events:
            # load it
            event = Event(**i)
            # tests attributes structure
            self.assertTrue(hasattr(event, "_id"))
            self.assertTrue(hasattr(event, "date"))
            self.assertTrue(hasattr(event, "description"))
            self.assertTrue(hasattr(event, "kind"))
            self.assertTrue(hasattr(event, "parent_resource"))
            # tests attributes value
            self.assertEqual(event._id, i.get("_id"))
            self.assertEqual(event.date, i.get("date"))
            self.assertEqual(event.kind, i.get("kind"))
            self.assertEqual(event.parent_resource, i.get("parent_resource"))

    def test_event_detailed(self):
        """GET :resources/{metadata_uuid}/events/{event_uuid}"""
        # retrieve event
        md_events = self.isogeo.metadata.events.listing(self.metadata_fixture_existing)
        # pick one randomly
        random_event = sample(md_events, 1)[0]
        # get
        online_event = self.isogeo.metadata.events.event(
            metadata_id=self.metadata_fixture_existing._id,
            event_id=random_event.get("_id"),
        )
        # check
        self.assertIsInstance(online_event, Event)

    # -- PUT/PATCH --
    # def test_events_update(self):
    #     """PUT :groups/{workgroup_uuid}/events/{event_uuid}}"""
    #     # create a new event
    #     event_fixture = Event(name="{}".format(get_test_marker()))
    #     event_fixture = self.isogeo.event.event_create(
    #         workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, event=event_fixture, check_exists=0
    #     )

    #     # modify local object
    #     event_fixture.name = "{} - {}".format(get_test_marker(), self.discriminator)
    #     event_fixture.scan = True

    #     # update the online event
    #     event_fixture = self.isogeo.event.event_update(event_fixture)

    #     # check if the change is effective
    #     event_fixture_updated = self.isogeo.event.event(
    #         event_fixture.owner.get("_id"), event_fixture._id
    #     )
    #     self.assertEqual(
    #         event_fixture_updated.name,
    #         "{} - {}".format(get_test_marker(), self.discriminator),
    #     )
    #     self.assertEqual(event_fixture_updated.scan, True)

    #     # add created event to deletion
    #     self.li_fixtures_to_delete.append(event_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
