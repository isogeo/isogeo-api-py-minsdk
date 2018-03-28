# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from six import string_types as str
from sys import exit
import unittest
from six.moves.urllib.parse import urlparse

# module target
from isogeo_pysdk import IsogeoUtils, __version__ as pysdk_version

# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get('ISOGEO_API_DEV_ID')
app_token = environ.get('ISOGEO_API_DEV_SECRET')

# #############################################################################
# ########## Classes ###############
# ##################################


class Search(unittest.TestCase):
    """Test search to Isogeo API."""
    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        # """Executed before each test."""
        self.utils = IsogeoUtils()
        self.uuid_hex = "0269803d50c446b09f5060ef7fe3e22b"
        self.uuid_urn4122 = "urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"
        self.uuid_urnIsogeo = "urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"

    def tearDown(self):
        """Executed after each test."""
        pass

    #  -  Isogeo components versions -----------------------------------------
    def test_get_isogeo_version_api(self):
        """"""
        version_api = self.utils.get_isogeo_version(component="api")
        version_api_naive = self.utils.get_isogeo_version()
        self.assertIsInstance(version_api, str)
        self.assertIsInstance(version_api_naive, str)
        self.assertEqual(version_api, version_api_naive)

    def test_get_isogeo_version_app(self):
        """"""
        version_app = self.utils.get_isogeo_version(component="app")
        self.assertIsInstance(version_app, str)

    def test_get_isogeo_version_db(self):
        """Check res"""
        version_db = self.utils.get_isogeo_version(component="db")
        self.assertIsInstance(version_db, str)

    def test_get_isogeo_version_bad_parameter(self):
        """Raise error if component parameter is bad."""
        with self.assertRaises(ValueError):
            self.utils.get_isogeo_version(component="youpi")

    # -- Base URLs -----------------------------------------------------------
    def test_set_base_url(self):
        """"""
        platform, base_url = self.utils.set_base_url()
        self.assertIsInstance(platform, str)
        self.assertIsInstance(base_url, str)

    def test_set_base_url_bad_parameter(self):
        """Raise error if platform parameter is bad."""
        with self.assertRaises(ValueError):
            self.utils.set_base_url(platform="skynet")

    # -- URLs Builders - edit (app) ------------------------------------------
    def test_get_edit_url_ok(self):
        """Test URL builder for edition link on APP"""
        url = self.utils.get_edit_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                      md_type="vector-dataset",
                                      owner_id="32f7e95ec4e94ca3bc1afda960003882",
                                      tab="identification")
        self.assertIsInstance(url, str)
        self.assertIn("https://app.isogeo.com", url)
        self.assertIn("groups", url)
        urlparse(url)

    def test_get_edit_url_bad_md_uuid(self):
        """Must raise an error if metadata/resource UUID check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(md_id="oh_my_bad_i_m_not_a_correct_uuid",
                                    md_type="vector-dataset",
                                    owner_id="32f7e95ec4e94ca3bc1afda960003882",
                                    tab="identification")

    def test_get_edit_url_bad_md_type(self):
        """Must raise an error if metadata/resource type check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    md_type="bad_md_type",
                                    owner_id="32f7e95ec4e94ca3bc1afda960003882",
                                    tab="identification")

    def test_get_edit_url_bad_wg_uuid(self):
        """Must raise an error if workgroup UUID check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    md_type="vector-dataset",
                                    owner_id="oh_my_bad_i_m_not_a_correct_uuid",
                                    tab="identification")

    def test_get_edit_url_bad_tab(self):
        """Must raise an error if tab check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    md_type="raster-dataset",
                                    owner_id="32f7e95ec4e94ca3bc1afda960003882",
                                    tab="attributes")

    # -- URLs Builders - view on web app -------------------------------------
    def test_get_view_url_ok(self):
        """Test URL builder for OpenCatalog and PixupPortal links."""
        # OpenCatalog
        oc_url = self.utils.get_view_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                         webapp="oc",
                                         share_id="1e07910d365449b59b6596a9b428ecd9",
                                         oc_token="TokenOhDearToken")
        self.assertEqual(oc_url, "https://open.isogeo.com/s/1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken/r/0269803d50c446b09f5060ef7fe3e22b")
        # PixUp portal - demo.isogeo.net sample
        pixup_url = self.utils.get_view_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                            webapp="pixup_portal",
                                            portal_url="demo.isogeo.net")
        self.assertEqual(pixup_url, "http://demo.isogeo.net/?muid=0269803d50c446b09f5060ef7fe3e22b")

    def test_get_view_url_bad(self):
        """Test URL builder for web app with bad parameters."""
        with self.assertRaises(ValueError):
            self.utils.get_view_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    webapp="my_imaginary_webapp",
                                    portal_url="demo.isogeo.net")

    def test_register_webapp_custom_ok(self):
        """Test register a custom webapp and use it ot build view url."""
        # register
        self.assertNotIn("PPIGE v3", self.utils.WEBAPPS)
        self.utils.register_webapp(webapp_name="PPIGE v3",
                                   webapp_args=["md_id", ],
                                   webapp_url="https://www.ppige-npdc.fr/portail/geocatalogue?uuid={md_id}")
        self.assertIn("PPIGE v3", self.utils.WEBAPPS)
        # use it
        custom_url = self.utils.get_view_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                             webapp="PPIGE v3")
        self.assertEqual(custom_url, "https://www.ppige-npdc.fr/portail/geocatalogue?uuid=0269803d50c446b09f5060ef7fe3e22b")

    def test_register_webapp_bad(self):
        """Must raise an error if web app arg is not in url."""
        with self.assertRaises(ValueError):
            self.utils.register_webapp(webapp_name="PPIGE v3",
                                       webapp_args=["md_id", ],
                                       webapp_url="https://www.ppige-npdc.fr/portail/geocatalogue?uuid=")

    # -- UUID converter - from HEX -------------------------------------------
    def test_hex_to_hex(self):
        """Test UUID converter from HEX to HEX"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_hex,
                                           mode=0)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_hex)
        self.assertNotIn(":", uuid_out)

    def test_hex_to_urn4122(self):
        """Test UUID converter from HEX to URN (RFC4122)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_hex,
                                           mode=1)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urn4122)
        self.assertNotIn("isogeo:metadata", uuid_out)

    def test_hex_to_urnIsogeo(self):
        """Test UUID converter from HEX to URN (Isogeo style)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_hex,
                                           mode=2)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urnIsogeo)
        self.assertIn("isogeo:metadata", uuid_out)

    # UUID converter - from URN (RFC4122)
    def test_urn4122_to_hex(self):
        """Test UUID converter from URN (RFC4122) to HEX"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urn4122,
                                           mode=0)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_hex)
        self.assertNotIn(":", uuid_out)

    def test_urn4122_to_urn4122(self):
        """Test UUID converter from URN (RFC4122) to URN (RFC4122)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urn4122,
                                           mode=1)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urn4122)
        self.assertNotIn("isogeo:metadata", uuid_out)

    def test_urn4122_to_urnIsogeo(self):
        """Test UUID converter from URN (RFC4122) to URN (Isogeo style)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urn4122,
                                           mode=2)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urnIsogeo)
        self.assertIn("isogeo:metadata", uuid_out)

    # UUID converter - from URN (Isogeo style)
    def test_urnIsogeo_to_hex(self):
        """Test UUID converter from URN (Isogeo style) to HEX"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo,
                                           mode=0)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_hex)
        self.assertNotIn(":", uuid_out)

    def test_urnIsogeo_to_urn4122(self):
        """Test UUID converter from URN (Isogeo style) to URN (RFC4122)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo,
                                           mode=1)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urn4122)
        self.assertNotIn("isogeo:metadata", uuid_out)

    def test_urnIsogeo_to_urnIsogeo(self):
        """Test UUID converter from URN (Isogeo style) to URN (Isogeo style)"""
        uuid_out = self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo,
                                           mode=2)
        self.assertIsInstance(uuid_out, str)
        self.assertEqual(uuid_out, self.uuid_urnIsogeo)
        self.assertIn("isogeo:metadata", uuid_out)

    # UUID converter
    def test_uuid_converter_bad_parameter(self):
        """Raise error if one parameter is bad."""
        with self.assertRaises(ValueError):
            self.utils.convert_uuid(in_uuid="oh_my_bad_i_m_not_a_correct_uuid")
        with self.assertRaises(TypeError):
            self.utils.convert_uuid(in_uuid=2)
            self.utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b",
                                    mode="ups_not_an_int")
            self.utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b",
                                    mode=3)
            self.utils.convert_uuid(in_uuid="0269803d50c446b09f5060ef7fe3e22b",
                                    mode=True)
