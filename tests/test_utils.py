# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

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
import json
import logging
from os import environ, path
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


class TestIsogeoUtils(unittest.TestCase):
    """Test search to Isogeo API."""
    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        """ Fixtures prepared before each test."""
        self.utils = IsogeoUtils()
        # uuid
        self.uuid_hex = "0269803d50c446b09f5060ef7fe3e22b"
        self.uuid_urn4122 = "urn:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"
        self.uuid_urnIsogeo = "urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"
        # credentials
        self.credentials_group_json = path.normpath(r"tests/fixtures/client_secrets_group.json")
        self.credentials_user_json = path.normpath(r"tests/fixtures/client_secrets_user.json")
        self.credentials_user_bad_json = path.normpath(r"tests/fixtures/client_secrets_user_bad.json")
        self.credentials_ini = path.normpath(r"tests/fixtures/client_secrets.ini")
        self.credentials_ini_bad = path.normpath(r"tests/fixtures/client_secrets_bad.ini")
        self.credentials_group_txt = path.normpath(r"tests/fixtures/client_secrets_group.txt")
        # API response samples
        self.tags_sample = path.normpath(r"tests/fixtures/api_response_tests_tags.json")

    def tearDown(self):
        """Executed after each test."""
        pass

    #  -  Isogeo components versions -----------------------------------------
    def test_get_isogeo_version_api(self):
        """Check API version"""
        # prod
        version_api_prod = self.utils.get_isogeo_version(component="api")
        version_api_naive_prod = self.utils.get_isogeo_version()
        # qa
        platform, api_url, app_url, csw_url, mng_url,\
            oc_url, ssl = self.utils.set_base_url(platform="qa")
        version_api_qa = self.utils.get_isogeo_version(component="api")
        version_api_naive_qa = self.utils.get_isogeo_version()
        # check
        self.assertIsInstance(version_api_prod, str)
        self.assertIsInstance(version_api_naive_prod, str)
        self.assertIsInstance(version_api_qa, str)
        self.assertIsInstance(version_api_naive_qa, str)
        self.assertEqual(version_api_prod, version_api_naive_prod)
        self.assertEqual(version_api_qa, version_api_naive_prod)

    def test_get_isogeo_version_app(self):
        """Check APP version"""
        # prod
        version_app_prod = self.utils.get_isogeo_version(component="app")
        # qa
        platform, api_url, app_url, csw_url, mng_url,\
            oc_url, ssl = self.utils.set_base_url(platform="qa")
        version_app_qa = self.utils.get_isogeo_version(component="app")
        # check
        self.assertIsInstance(version_app_prod, str)
        self.assertIsInstance(version_app_qa, str)

    def test_get_isogeo_version_db(self):
        """Check DB version"""
        # prod
        version_db_prod = self.utils.get_isogeo_version(component="db")
        # qa
        platform, api_url, app_url, csw_url, mng_url,\
            oc_url, ssl = self.utils.set_base_url(platform="qa")
        version_db_qa = self.utils.get_isogeo_version(component="db")
        # check
        self.assertIsInstance(version_db_prod, str)
        self.assertIsInstance(version_db_qa, str)

    def test_get_isogeo_version_bad_parameter(self):
        """Raise error if component parameter is bad."""
        with self.assertRaises(ValueError):
            self.utils.get_isogeo_version(component="youpi")

    # -- Base URLs -----------------------------------------------------------
    def test_set_base_url(self):
        """Set base URLs"""
        # by default platform = prod
        platform, api_url, app_url, csw_url, mng_url,\
            oc_url, ssl = self.utils.set_base_url()
        self.assertIsInstance(platform, str)
        self.assertIsInstance(api_url, str)
        self.assertIsInstance(ssl, bool)
        self.assertEqual(platform, "prod")
        self.assertEqual(api_url, self.utils.API_URLS.get("prod"))
        self.assertEqual(ssl, True)
        # qa
        platform, api_url, app_url, csw_url, mng_url,\
            oc_url, ssl = self.utils.set_base_url(platform="qa")
        self.assertIsInstance(platform, str)
        self.assertIsInstance(api_url, str)
        self.assertIsInstance(ssl, bool)
        self.assertEqual(platform, "qa")
        self.assertEqual(api_url, self.utils.API_URLS.get("qa"))
        self.assertEqual(ssl, False)

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
        # again with type extracted from metadata model
        url = self.utils.get_edit_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                        md_type="vectorDataset",
                                        owner_id="32f7e95ec4e94ca3bc1afda960003882",
                                        tab="identification")

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
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    md_type="raster-dataset",
                                    owner_id="32f7e95ec4e94ca3bc1afda960003882",
                                    tab="what_a_tab_name")

    # -- URLs Builders - view on web app -------------------------------------
    def test_get_view_url_ok(self):
        """Test URL builder for OpenCatalog and PixupPortal links."""
        # OpenCatalog
        oc_url = self.utils.get_view_url(webapp="oc",
                                         md_id="0269803d50c446b09f5060ef7fe3e22b",
                                         share_id="1e07910d365449b59b6596a9b428ecd9",
                                         share_token="TokenOhDearToken")
        self.assertEqual(oc_url, "https://open.isogeo.com/s/1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken/r/0269803d50c446b09f5060ef7fe3e22b")

        # PixUp portal - demo.isogeo.net sample
        pixup_url = self.utils.get_view_url(webapp="pixup_portal",
                                            md_id="0269803d50c446b09f5060ef7fe3e22b",
                                            portal_url="demo.isogeo.net")
        self.assertEqual(pixup_url, "http://demo.isogeo.net/?muid=0269803d50c446b09f5060ef7fe3e22b")

        # CSW - GetCapapabilities
        csw_getcap_url = self.utils.get_view_url(webapp="csw_getcap",
                                                 share_id="1e07910d365449b59b6596a9b428ecd9",
                                                 share_token="TokenOhDearToken")
        self.assertEqual(csw_getcap_url,
                         "https://services.api.isogeo.com/ows/s/1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken?"
                         "service=CSW&version=2.0.2&request=GetCapabilities")

        # CSW - GetRecord
        csw_getrec_url = self.utils.get_view_url(webapp="csw_getrec",
                                                 md_uuid_urn=self.uuid_urnIsogeo,
                                                 share_id="1e07910d365449b59b6596a9b428ecd9",
                                                 share_token="TokenOhDearToken")
        self.assertEqual(csw_getrec_url,
                         "https://services.api.isogeo.com/ows/s/"
                         "1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken?service=CSW"
                         "&version=2.0.2&request=GetRecordById"
                         "&id=urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"
                         "&elementsetname=full&outputSchema=http://www.isotc211.org/2005/gmd")

    def test_get_view_url_bad(self):
        """Test URL builder for web app with bad parameters."""
        with self.assertRaises(ValueError):
            self.utils.get_view_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    webapp="my_imaginary_webapp",
                                    portal_url="demo.isogeo.net")
        with self.assertRaises(TypeError):
            self.utils.get_view_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    webapp="pixup_portal",
                                    my_nice_arg="a_nice_arg")

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

    # UUID converter - bad boys
    def test_uuid_converter_bad_value(self):
        """Raise error if one parameter value is bad."""
        with self.assertRaises(ValueError):
            self.utils.convert_uuid(in_uuid="oh_my_bad_i_m_not_a_correct_uuid")
        with self.assertRaises(ValueError):
            self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo,
                                    mode=4)

    def test_uuid_converter_bad_type(self):
        """Raise error if one parameter type is bad."""
        with self.assertRaises(TypeError):
            self.utils.convert_uuid(in_uuid=2)
        with self.assertRaises(TypeError):
            self.utils.convert_uuid(in_uuid=self.uuid_urnIsogeo,
                                    mode="ups_not_an_int")

    # -- Credentials loader -------------------------------------
    def test_credentials_loader_json_user(self):
        """Test credentials loader for an user application from a JSON file"""
        creds_json_user = self.utils.credentials_loader(self.credentials_user_json)
        # structure
        self.assertIsInstance(creds_json_user, dict)
        self.assertIn("auth_mode", creds_json_user)
        self.assertIn("client_id", creds_json_user)
        self.assertIn("client_secret", creds_json_user)
        self.assertIn("uri_auth", creds_json_user)
        self.assertIn("uri_base", creds_json_user)
        self.assertIn("uri_token", creds_json_user)
        self.assertIn("uri_redirect", creds_json_user)
        # values
        self.assertEqual(creds_json_user.get("auth_mode"), "user")
        self.assertEqual(creds_json_user.get("uri_auth"),
                         "https://id.api.isogeo.com/oauth/authorize")
        self.assertEqual(creds_json_user.get("uri_base"),
                         "https://api.isogeo.com")
        self.assertEqual(creds_json_user.get("uri_token"),
                         "https://id.api.isogeo.com/oauth/token")
        self.assertIsInstance(creds_json_user.get("uri_redirect"), list)

    def test_credentials_loader_json_group(self):
        """Test credentials loader for an group application from a JSON file"""
        creds_json_group = self.utils.credentials_loader(self.credentials_group_json)
        # structure
        self.assertIsInstance(creds_json_group, dict)
        self.assertIn("auth_mode", creds_json_group)
        self.assertIn("client_id", creds_json_group)
        self.assertIn("client_secret", creds_json_group)
        self.assertIn("uri_auth", creds_json_group)
        self.assertIn("uri_base", creds_json_group)
        self.assertIn("uri_token", creds_json_group)
        self.assertIn("uri_redirect", creds_json_group)
        # values
        self.assertEqual(creds_json_group.get("auth_mode"), "group")
        self.assertEqual(creds_json_group.get("uri_auth"),
                         "https://id.api.isogeo.com/oauth/authorize")
        self.assertEqual(creds_json_group.get("uri_token"),
                         "https://id.api.isogeo.com/oauth/token")
        self.assertEqual(creds_json_group.get("uri_base"),
                         "https://api.isogeo.com")
        self.assertIsNone(creds_json_group.get("uri_redirect"))

    def test_credentials_loader_ini(self):
        """Test credentials loader for an group application from an INI file"""
        creds_ini = self.utils.credentials_loader(
            self.credentials_ini)
        # structure
        self.assertIsInstance(creds_ini, dict)
        self.assertIn("auth_mode", creds_ini)
        self.assertIn("client_id", creds_ini)
        self.assertIn("client_secret", creds_ini)
        self.assertIn("uri_auth", creds_ini)
        self.assertIn("uri_base", creds_ini)
        self.assertIn("uri_token", creds_ini)
        self.assertIn("uri_redirect", creds_ini)
        # values
        self.assertEqual(creds_ini.get("auth_mode"), "group")
        self.assertEqual(creds_ini.get("uri_auth"),
                         "https://id.api.isogeo.com/oauth/authorize")
        self.assertEqual(creds_ini.get("uri_base"),
                         "https://api.isogeo.com")
        self.assertEqual(creds_ini.get("uri_token"),
                         "https://id.api.isogeo.com/oauth/token")

    def test_credentials_loader_bad_file_path(self):
        """Raise error if credentials file is not reachable."""
        with self.assertRaises(IOError):
            self.utils.credentials_loader(in_credentials=r"imaginary_file.json")

    def test_credentials_loader_bad_file_extension(self):
        """Raise error if extension is not one of accepted ones."""
        with self.assertRaises(ValueError):
            self.utils.credentials_loader(in_credentials=self.credentials_group_txt)

    def test_credentials_loader_bad_file_structure(self):
        """Raise error if file structure is not good."""
        with self.assertRaises(ValueError):
            self.utils.credentials_loader(in_credentials=self.credentials_user_bad_json)
        with self.assertRaises(ValueError):
            self.utils.credentials_loader(
                in_credentials=self.credentials_ini_bad)

    # -- Tags utils --------
    def test_tags_dictionarization(self):
        """Tags dictionarization bullet-proof."""
        with open(self.tags_sample, "r") as f:
            search = json.loads(f.read())
        self.utils.tags_to_dict(tags=search.get("tags"),
                                prev_query=search.get("query"))
        self.utils.tags_to_dict(tags=search.get("tags"),
                                prev_query=search.get("query"),
                                duplicated="merge")
        self.utils.tags_to_dict(tags=search.get("tags"),
                                prev_query=search.get("query"),
                                duplicated="rename")

    def test_tags_dictionarization_bad(self):
        """Tags dictionarization bullet-proof."""
        with open(self.tags_sample, "r") as f:
            search = json.loads(f.read())
        with self.assertRaises(ValueError):
            self.utils.tags_to_dict(search.get("tags"),
                                    duplicated="renam")
