# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

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
from os import environ
import logging
from random import sample
from socket import gethostname
from sys import exit
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv
from oauthlib.oauth2 import LegacyApplicationClient

# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Specification


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


class TestSpecifications(unittest.TestCase):
    """Test Specification model of Isogeo API."""

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
        self.li_specifications_to_delete = []
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
        # clean created specifications
        if len(self.li_specifications_to_delete):
            for i in self.li_specifications_to_delete:
                self.isogeo.specification_delete(workgroup_id=workgroup_test, specification_id=i)
        # close sessions
        self.isogeo.close()

    # -- ALL APPS ------------------------------------------------------------
    def test_specifications_create_basic(self):
        """POST :groups/{workgroup_uuid}/specifications/}"""
        spec = Specification(
            name="TEST_UNIT_AUTO {}".format(self.discriminator),
            link="https://help.isogeo.com/api/fr/")
        new_spec = self.isogeo.specification_create(workgroup_id=workgroup_test, specification=spec)

        # checks
        self.assertEqual(new_spec.name, "TEST_UNIT_AUTO {}".format(self.discriminator))
        self.assertTrue(self.isogeo.specification_exists(new_spec._id))

        # add created specification to deletion
        self.li_specifications_to_delete.append(new_spec._id)
        print(new_spec._id)

    # def test_specifications_create_complete(self):
    #     """POST :groups/{workgroup_uuid}/specifications/}"""
    #     ct = Specification(
    #         addressLine1="26 rue du faubourg Saint-Antoine",
    #         addressLine2="4è étage",
    #         addressLine3="Porte rouge",
    #         name="TEST_UNIT_AUTO {}".format(self.discriminator),
    #         city="Paris",
    #         email="test@isogeo.fr",
    #         fax="+33987654321",
    #         organization="Isogeo",
    #         phone="+33789456123",
    #         countryCode="FR",
    #         zipCode="75012",
    #     )
    #     new_ct = self.isogeo.specification_create(workgroup_id=workgroup_test, specification=ct)

    #     # checks
    #     self.assertEqual(new_ct.get("name"), "TEST_UNIT_AUTO {}".format(self.discriminator))
    #     self.assertEqual(new_ct.get("type"), "custom")
    #     self.assertTrue(self.isogeo.specification_exists(new_ct.get("_id")))

    #     # add created specification to deletion
    #     self.li_specifications_to_delete.append(new_ct.get("_id"))

    # def test_specifications_create_checking_name(self):
    #     """POST :groups/{workgroup_uuid}/specifications/}"""
    #     # create a specification
    #     ct = Specification(
    #         name="TEST_UNIT_AUTO {}".format(self.discriminator)
    #     )
    #     new_ct_1 = self.isogeo.specification_create(
    #         workgroup_id=workgroup_test,
    #         check_exists=0,
    #         specification=ct
    #     )
    #     # try to create a specification with the same email = False
    #     ct = Specification(
    #         name="TEST_UNIT_AUTO {}".format(self.discriminator)
    #     )
    #     new_ct_2 = self.isogeo.specification_create(
    #         workgroup_id=workgroup_test,
    #         check_exists=1,
    #         specification=ct
    #     )

    #     # check the result
    #     self.assertEqual(new_ct_2, False)

    #     # add created specification to deletion
    #     self.li_specifications_to_delete.append(new_ct_1.get("_id"))

    # def test_specifications_get_workgroup(self):
    #     """GET :groups/{workgroup_uuid}/specifications}"""
    #     # retrieve workgroup specifications
    #     wg_specifications = self.isogeo.workgroup_specifications(
    #         workgroup_id=workgroup_test,
    #         caching=0
    #     )
    #     # parse and test object loader
    #     for i in wg_specifications:
    #         ct = Specification(**i)
    #         # tests attributes structure
    #         self.assertTrue(hasattr(ct, "_abilities"))
    #         self.assertTrue(hasattr(ct, "_created"))
    #         self.assertTrue(hasattr(ct, "_id"))
    #         self.assertTrue(hasattr(ct, "_modified"))
    #         self.assertTrue(hasattr(ct, "_tag"))
    #         self.assertTrue(hasattr(ct, "code"))
    #         self.assertTrue(hasattr(ct, "count"))
    #         self.assertTrue(hasattr(ct, "name"))
    #         self.assertTrue(hasattr(ct, "owner"))
    #         self.assertTrue(hasattr(ct, "scan"))
    #         # tests attributes value
    #         self.assertEqual(ct.code, i.get("code"))
    #         self.assertEqual(ct.name, i.get("name"))

    # def test_specifications_update(self):
    #     """PUT :groups/{workgroup_uuid}/specifications/{specification_uuid}}"""
    #     # create a new specification
    #     cat = Specification(name="TEST_UNIT_UPDATE {}".format(self.discriminator))
    #     new_cat_created = Specification(**self.isogeo.specification_create(workgroup_id=workgroup_test, specification=cat))
    #     # set a different name
    #     new_cat_created.name = "TEST_UNIT_UPDATE_OTRO {}".format(self.discriminator)
    #     # update the specification
    #     cat_updated = self.isogeo.specification_update(workgroup_test, new_cat_created)
    #     Specification(**cat_updated)
    #     # check if the change is effective
    #     self.assertEqual(cat_updated.get("name"), "TEST_UNIT_UPDATE_OTRO {}".format(self.discriminator))
    #     # # add created specification to deletion
    #     self.li_specifications_to_delete.append(cat_updated.get("_id"))


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
