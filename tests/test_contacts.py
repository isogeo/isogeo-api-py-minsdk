# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Usage from the repo root folder:

```python
# for whole test
python -m unittest tests.test_contacts
# for specific
python -m unittest tests.test_contacts.TestContacts.test_contacts_create_basic
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
from isogeo_pysdk import Isogeo, Contact


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
    return "TEST_PySDK - Contacts - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestContacts(unittest.TestCase):
    """Test Contact model of Isogeo API."""

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
        # clean created contacts
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.contact.delete(
                    workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, contact_id=i
                )
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_contacts_create_basic(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # var
        contact_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        contact_new = Contact(name=contact_name)

        # create it online
        contact_new = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            contact=contact_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(contact_new.name, contact_name)
        self.assertTrue(self.isogeo.contact.exists(contact_new._id))

        # add created specification to deletion
        self.li_fixtures_to_delete.append(contact_new._id)

    def test_contacts_create_complete(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # var
        contact_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create a complete local object
        contact_new = Contact(
            addressLine1="26 rue du faubourg Saint-Antoine",
            addressLine2="4è étage",
            addressLine3="Porte rouge",
            name=contact_name,
            city="Paris",
            email="test@isogeo.fr",
            fax="+33987654321",
            organization="Isogeo",
            phone="+33789456123",
            countryCode="FR",
            zipCode="75012",
        )
        contact_new = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, contact=contact_new
        )

        # checks
        self.assertEqual(contact_new.name, contact_name)
        self.assertEqual(contact_new.type, "custom")
        self.assertTrue(self.isogeo.contact.exists(contact_new._id))

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_new._id)

    def test_contacts_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        contact_local = Contact(name=name_to_be_unique)

        # create it online
        contact_new_1 = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            contact=contact_local,
            check_exists=0,
        )

        # try to create a contact with the same name
        contact_new_2 = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            contact=contact_local,
            check_exists=1,
        )

        # check if object has not been created
        self.assertIsInstance(contact_new_2, Contact)
        self.assertEqual(contact_new_1._id, contact_new_2._id)

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_new_1._id)

    def test_contacts_create_checking_email(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # vars
        email_to_be_unique = "test@isogeo.fr"
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        contact_local = Contact(email=email_to_be_unique, name=name_to_be_unique)

        # create it online
        contact_new_1 = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            contact=contact_local,
            check_exists=0,
        )

        # try to create a contact with the same email
        contact_new_2 = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            contact=contact_local,
            check_exists=2,
        )

        # check if object has not been created
        self.assertIsInstance(contact_new_2, Contact)
        self.assertEqual(contact_new_1._id, contact_new_2._id)

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_new_1._id)

    # -- GET --
    def test_contacts_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/contacts}"""
        # retrieve workgroup contacts
        wg_contacts = self.isogeo.contact.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
        )
        self.assertIsInstance(wg_contacts, list)
        # parse and test object loader
        for i in wg_contacts:
            contact = Contact(**i)
            # tests attributes structure
            self.assertTrue(hasattr(contact, "_abilities"))
            self.assertTrue(hasattr(contact, "_id"))
            self.assertTrue(hasattr(contact, "_tag"))
            self.assertTrue(hasattr(contact, "_addressLine1"))
            self.assertTrue(hasattr(contact, "_addressLine2"))
            self.assertTrue(hasattr(contact, "_addressLine3"))
            self.assertTrue(hasattr(contact, "_city"))
            self.assertTrue(hasattr(contact, "_count"))
            self.assertTrue(hasattr(contact, "name"))
            self.assertTrue(hasattr(contact, "owner"))
            self.assertTrue(hasattr(contact, "zipCode"))
            # tests attributes value
            self.assertEqual(contact.addressLine1, i.get("addressLine1"))
            self.assertEqual(contact.name, i.get("name"))
            self.assertEqual(contact.zipCode, i.get("zipCode"))

    def test_contact_detailed(self):
        """GET :contacts/{contact_uuid}"""
        # ensure the workgroup has got a contact
        contact_name = "{} - {}".format(get_test_marker(), self.discriminator)
        contact_new = Contact(name=contact_name)
        contact_new = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            contact=contact_new,
            check_exists=0,
        )

        # retrieve workgroup contacts
        wg_contacts = self.isogeo.contact.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=0
        )

        # pick one contact
        contact_workgroup = sample(wg_contacts, 1)[0]

        # check both exist
        self.assertTrue(self.isogeo.contact.exists(contact_workgroup.get("_id")))

        # get and check
        contact_workgroup = self.isogeo.contact.get(contact_workgroup.get("_id"))

        self.assertIsInstance(contact_workgroup, Contact)

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_new._id)

    # -- PUT/PATCH --
    def test_contacts_update(self):
        """PUT :groups/{workgroup_uuid}/contacts/{contact_uuid}}"""
        # create a new contact
        contact_fixture = Contact(
            name="{} - {}".format(get_test_marker(), self.discriminator)
        )
        contact_fixture = self.isogeo.contact.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            contact=contact_fixture,
            check_exists=0,
        )

        # modify local object
        contact_fixture.name = "{} - UPDATED - {}".format(
            get_test_marker(), self.discriminator
        )

        # update the online contact
        contact_fixture = self.isogeo.contact.update(contact_fixture)

        # check if the change is effective
        contact_fixture_updated = self.isogeo.contact.get(contact_fixture._id)
        self.assertEqual(
            contact_fixture_updated.name,
            "{} - UPDATED - {}".format(get_test_marker(), self.discriminator),
        )

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
