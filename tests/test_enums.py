# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_enums
    # for specific
    python -m unittest tests.test_enums.TestEnums
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import unittest

# module target
from isogeo_pysdk.enums import (
    ApplicationKinds,
    ContactRoles,
    ContactTypes,
    EventKinds,
    KeywordCasing,
    LinkActions,
    LinkKinds,
    LinkTypes,
    MetadataTypes,
)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestEnums(unittest.TestCase):
    """Test Enum model of Isogeo API."""

    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- TESTS ---------------------------------------------------------

    def test_application_kinds(self):
        """Check metadata's types list"""
        self.assertEqual(len(ApplicationKinds), 2)
        self.assertTrue("group" in ApplicationKinds.__members__)
        self.assertFalse("User" in ApplicationKinds.__members__)
        for i in ApplicationKinds:
            self.assertIsInstance(i.value, int)

    def test_contact_roles(self):
        """Check contact's roles list"""
        self.assertEqual(len(ContactRoles), 11)
        self.assertTrue("author" in ContactRoles.__members__)
        self.assertFalse("Author" in ContactRoles.__members__)
        for i in ContactRoles:
            self.assertIsInstance(i.value, str)

    def test_contact_types(self):
        """Check contact's types list"""
        self.assertEqual(len(ContactTypes), 3)
        self.assertTrue("group" in ContactTypes.__members__)
        self.assertFalse("Custom" in ContactTypes.__members__)
        for i in ContactTypes:
            self.assertIsInstance(i.value, int)

    def test_event_kinds(self):
        """Check metadata's types list"""
        self.assertEqual(len(EventKinds), 3)
        self.assertTrue("creation" in EventKinds.__members__)
        self.assertFalse("Update" in EventKinds.__members__)
        for i in EventKinds:
            self.assertIsInstance(i.value, int)

    def test_keyword_casing(self):
        """Check keyword casing values list"""
        self.assertEqual(len(KeywordCasing), 4)
        self.assertTrue("capitalized" in KeywordCasing.__members__)
        self.assertFalse("Uppercase" in KeywordCasing.__members__)
        for i in KeywordCasing:
            self.assertIsInstance(i.value, int)

    def test_link_action(self):
        """Check link actions values list"""
        self.assertEqual(len(LinkActions), 3)
        self.assertTrue("download" in LinkActions.__members__)
        self.assertFalse("Other" in LinkActions.__members__)
        for i in LinkActions:
            self.assertIsInstance(i.value, int)

    def test_link_kind(self):
        """Check link kinds values list"""
        self.assertEqual(len(LinkKinds), 8)
        self.assertTrue("wms" in LinkKinds.__members__)
        self.assertFalse("EsriFeatureDataset" in LinkKinds.__members__)
        for i in LinkKinds:
            self.assertIsInstance(i.value, int)

    def test_link_type(self):
        """Check link types values list"""
        self.assertEqual(len(LinkTypes), 3)
        self.assertTrue("hosted" in LinkTypes.__members__)
        self.assertFalse("Link" in LinkTypes.__members__)
        for i in LinkTypes:
            self.assertIsInstance(i.value, int)

    def test_metadata_types(self):
        """Check metadata's types list"""
        self.assertEqual(len(MetadataTypes), 4)
        self.assertTrue("rasterDataset" in MetadataTypes.__members__)
        self.assertFalse("Service" in MetadataTypes.__members__)
        for i in MetadataTypes:
            self.assertIsInstance(i.value, str)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
