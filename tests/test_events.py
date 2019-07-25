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
from os import environ
import logging
from pathlib import Path
from random import sample
from socket import gethostname
from sys import exit, _getframe
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Event


# #############################################################################
# ######## Globals #################
# ##################################


if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
WG_TEST_FIXTURE = environ.get("ISOGEO_WORKGROUP_TEST_UUID")
MD_TEST_FIXTURE = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_UNIT_PythonSDK - {}".format(_getframe(1).f_code.co_name)


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
        logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

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
        cls.metadata_fixture = cls.isogeo.metadata.get(metadata_id=MD_TEST_FIXTURE)

    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(
            hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
        )

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
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
        event_kind = "update"
        event_description = "{} - {}".format(get_test_marker(), self.discriminator)

        # create object locally
        event_new = Event(
            date=event_date,
            kind=event_kind,
            description=event_description,
            parent_resource=self.metadata_fixture._id,
        )

        # create it online
        event_new = self.isogeo.metadata.events.create(
            metadata=self.metadata_fixture, event=event_new
        )

        # checks
        self.assertEqual(event_new.kind, event_kind)
        self.assertEqual(event_new.description, event_description)

        # add created event to deletion
        self.li_fixtures_to_delete.append(event_new)

    # def test_events_create_checking_name(self):
    #     """POST :groups/{workgroup_uuid}/events/}"""
    #     # vars
    #     name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

    #     # create local object
    #     event_local = Event(name=name_to_be_unique)

    #     # create it online
    #     event_new_1 = self.isogeo.event.event_create(
    #         workgroup_id=WG_TEST_FIXTURE, event=event_local, check_exists=0
    #     )

    #     # try to create a event with the same name
    #     event_new_2 = self.isogeo.event.event_create(
    #         workgroup_id=WG_TEST_FIXTURE, event=event_local, check_exists=1
    #     )

    #     # check if object has not been created
    #     self.assertEqual(event_new_2, False)

    #     # add created event to deletion
    #     self.li_fixtures_to_delete.append(event_new_1._id)

    # -- GET --
    def test_events_listing(self):
        """GET :resources/{metadata_uuid}/events/}"""
        # retrieve workgroup events
        md_events = self.isogeo.metadata.events.listing(self.metadata_fixture)
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
        md_events = self.isogeo.metadata.events.listing(self.metadata_fixture)
        # pick one randomly
        random_event = sample(md_events, 1)[0]
        # get
        online_event = self.isogeo.metadata.events.event(
            metadata_id=self.metadata_fixture._id, event_id=random_event.get("_id")
        )
        # check
        self.assertIsInstance(online_event, Event)

    # -- PUT/PATCH --
    # def test_events_update(self):
    #     """PUT :groups/{workgroup_uuid}/events/{event_uuid}}"""
    #     # create a new event
    #     event_fixture = Event(name="{}".format(get_test_marker()))
    #     event_fixture = self.isogeo.event.event_create(
    #         workgroup_id=WG_TEST_FIXTURE, event=event_fixture, check_exists=0
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
