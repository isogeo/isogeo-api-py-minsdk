# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_contacts
    # for specific
    python -m unittest tests.test_contacts.TestContacts.test_contacts_create
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from socket import gethostname
from sys import exit
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv
from oauthlib.oauth2 import LegacyApplicationClient

# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Contact


# #############################################################################
# ######## Globals #################
# ##################################

load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
app_script_id = environ.get("ISOGEO_API_USER_CLIENT_ID")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
platform = environ.get("ISOGEO_PLATFORM", "qa")
user_email = environ.get("ISOGEO_USER_NAME")
user_password = environ.get("ISOGEO_USER_PASSWORD")
workgroup_test = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Classes ###############
# ##################################


class TestContacts(unittest.TestCase):
    """Test Contact model of Isogeo API."""

    if not app_script_id or not app_script_secret:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(hostname, strftime("%Y-%m-%d_%H%M%S", gmtime()))
        self.li_contacts_to_delete = []
        # API connection
        self.isogeo = IsogeoSession(
            client=LegacyApplicationClient(client_id=app_script_id),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            client_secret=app_script_secret,
            platform=platform
        )

        # getting a token
        self.isogeo.connect(username=user_email, password=user_password)

    def tearDown(self):
        """Executed after each test."""
        # clean created contacts
        if len(self.li_contacts_to_delete):
            for i in self.li_contacts_to_delete:
                self.isogeo.contact_delete(workgroup_id=workgroup_test, contact_id=i)
        # close sessions
        self.isogeo.close()

    # -- ALL APPS ------------------------------------------------------------
    def test_contacts_create_basic(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        ct = Contact(name="TEST_UNIT_AUTO {}".format(self.discriminator))
        new_ct = self.isogeo.contact_create(workgroup_id=workgroup_test, contact=ct)

        # checks
        self.assertEqual(new_ct.get("name"), "TEST_UNIT_AUTO {}".format(self.discriminator))
        self.assertTrue(self.isogeo.contact_exists(new_ct.get("_id")))

        # add created contact to deletion
        self.li_contacts_to_delete.append(new_ct.get("_id"))

    def test_contacts_create_complete(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        ct = Contact(
            addressLine1="26 rue du faubourg Saint-Antoine",
            addressLine2="4è étage",
            addressLine3="Porte rouge",
            name="TEST_UNIT_AUTO {}".format(self.discriminator),
            city="Paris",
            email="test@isogeo.fr",
            fax="+33987654321",
            organization="Isogeo",
            phone="+33789456123",
            countryCode="FR",
            zipCode="75012",
        )
        new_ct = self.isogeo.contact_create(workgroup_id=workgroup_test, contact=ct)

        # checks
        self.assertEqual(new_ct.get("name"), "TEST_UNIT_AUTO {}".format(self.discriminator))
        self.assertEqual(new_ct.get("type"), "custom")
        self.assertTrue(self.isogeo.contact_exists(new_ct.get("_id")))

        # add created contact to deletion
        self.li_contacts_to_delete.append(new_ct.get("_id"))

    def test_contacts_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # create a contact
        ct = Contact(
            name="TEST_UNIT_AUTO {}".format(self.discriminator),
            email="test@isogeo.fr",
        )
        new_ct_1 = self.isogeo.contact_create(
            workgroup_id=workgroup_test,
            check_exists=0,
            contact=ct
        )
        # try to create a contact with the same email = False
        ct = Contact(
            name="TEST_UNIT_AUTO {}".format(self.discriminator),
            email="test2@isogeo.fr",
        )
        new_ct_2 = self.isogeo.contact_create(
            workgroup_id=workgroup_test,
            check_exists=1,
            contact=ct
        )

        # check the result
        self.assertEqual(new_ct_2, False)

        # add created contact to deletion
        self.li_contacts_to_delete.append(new_ct_1.get("_id"))

    def test_contacts_create_checking_email(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # create a contact
        ct = Contact(
            name="TEST_UNIT_AUTO {}".format(self.discriminator),
            email="test@isogeo.fr",
        )
        new_ct_1 = self.isogeo.contact_create(
            workgroup_id=workgroup_test,
            check_exists=0,
            contact=ct
        )
        # try to create a contact with the same email = False
        ct = Contact(
            name="TEST_UNIT_AUTO {}_2".format(self.discriminator),
            email="test@isogeo.fr",
        )
        new_ct_2 = self.isogeo.contact_create(
            workgroup_id=workgroup_test,
            check_exists=2,
            contact=ct
        )

        # check the result
        self.assertEqual(new_ct_2, False)

        # add created contact to deletion
        self.li_contacts_to_delete.append(new_ct_1.get("_id"))

    def test_contacts_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/contacts}"""
        # retrieve workgroup contacts
        wg_contacts = self.isogeo.workgroup_contacts(
            workgroup_id=workgroup_test,
            caching=0
        )
        # parse and test object loader
        for i in wg_contacts:
            ct = Contact(**i)
            yield (
                ct._id,
                ct._tag,
                ct._addressLine1,
                ct._addressLine2,
                ct._addressLine3,
                ct._city,
                ct._count,
                ct.name
            )

    def test_contacts_update(self):
        """PUT :groups/{workgroup_uuid}/contacts/{contact_uuid}}"""
        # create a new contact
        cat = Contact(name="TEST_UNIT_UPDATE {}".format(self.discriminator))
        new_cat_created = Contact(**self.isogeo.contact_create(workgroup_id=workgroup_test, contact=cat))
        # set a different name
        new_cat_created.name = "TEST_UNIT_UPDATE_OTRO {}".format(self.discriminator)
        # update the contact
        cat_updated = self.isogeo.contact_update(workgroup_test, new_cat_created)
        # check if the change is effective
        self.assertEqual(cat_updated.get("name"), "TEST_UNIT_UPDATE_OTRO {}".format(self.discriminator))
        # # add created contact to deletion
        self.li_contacts_to_delete.append(cat_updated.get("_id"))


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
