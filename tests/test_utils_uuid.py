# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:
    
    ```python
    python -m unittest tests.test_utils
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from pathlib import Path

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import IsogeoUtils

# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestIsogeoUtilsUuid(unittest.TestCase):
    """Test search to Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.utils = IsogeoUtils()

    def setUp(self):
        """ Fixtures prepared before each test."""
        # uuid
        self.uuid_hex = "0269803d50c446b09f5060ef7fe3e22b"
        self.uuid_urn4122 = "urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"
        self.uuid_urnIsogeo = (
            "urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"
        )

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- UUID converter - from HEX -------------------------------------------
    def test_hex_to_hex(self):
        """Test UUID converter from HEX to HEX"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_hex, mode=0)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_hex)
        self.assertNotIn(":", uuid_out)

    def test_hex_to_urn4122(self):
        """Test UUID converter from HEX to URN (RFC4122)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_hex, mode=1)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urn4122)
        self.assertNotIn("isogeo:metadata", uuid_out)

    def test_hex_to_urnIsogeo(self):
        """Test UUID converter from HEX to URN (Isogeo style)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_hex, mode=2)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urnIsogeo)
        self.assertIn("isogeo:metadata", uuid_out)

    # UUID converter - from URN (RFC4122)
    def test_urn4122_to_hex(self):
        """Test UUID converter from URN (RFC4122) to HEX"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urn4122, mode=0)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_hex)
        self.assertNotIn(":", uuid_out)

    def test_urn4122_to_urn4122(self):
        """Test UUID converter from URN (RFC4122) to URN (RFC4122)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urn4122, mode=1)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urn4122)
        self.assertNotIn("isogeo:metadata", uuid_out)

    def test_urn4122_to_urnIsogeo(self):
        """Test UUID converter from URN (RFC4122) to URN (Isogeo style)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urn4122, mode=2)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urnIsogeo)
        self.assertIn("isogeo:metadata", uuid_out)

    # UUID converter - from URN (Isogeo style)
    def test_urnIsogeo_to_hex(self):
        """Test UUID converter from URN (Isogeo style) to HEX"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo, mode=0)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_hex)
        self.assertNotIn(":", uuid_out)

    def test_urnIsogeo_to_urn4122(self):
        """Test UUID converter from URN (Isogeo style) to URN (RFC4122)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo, mode=1)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urn4122)
        self.assertNotIn("isogeo:metadata", uuid_out)

    def test_urnIsogeo_to_urnIsogeo(self):
        """Test UUID converter from URN (Isogeo style) to URN (Isogeo style)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo, mode=2)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urnIsogeo)
        self.assertIn("isogeo:metadata", uuid_out)

    # UUID converter - bad boys
    def test_uuid_converter_bad_value(self):
        """Raise error if one parameter value is bad."""
        with self.assertRaises(ValueError):
            self.utils.convert_uuid(in_uuid="oh_my_bad_i_m_not_a_correct_uuid")
        with self.assertRaises(ValueError):
            self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo, mode=4)

    def test_uuid_converter_bad_type(self):
        """Raise error if one parameter type is bad."""
        with self.assertRaises(TypeError):
            self.utils.convert_uuid(in_uuid=2)
        with self.assertRaises(TypeError):
            self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo, mode="ups_not_an_int")
