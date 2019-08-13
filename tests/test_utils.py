# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:
    
    ```python
    # for whole test
    python -m unittest tests.test_utils
    # for specific
    python -m unittest tests.test_utils.TestIsogeoUtils.test_get_edit_url_ok
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from pathlib import Path
from urllib.parse import urlparse

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


class TestIsogeoUtils(unittest.TestCase):
    """Test utils for Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.utils = IsogeoUtils()

    # standard methods
    def setUp(self):
        """ Fixtures prepared before each test."""
        pass

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
        platform, api_url, app_url, csw_url, mng_url, oc_url, ssl = self.utils.set_base_url(
            platform="qa"
        )
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
        platform, api_url, app_url, csw_url, mng_url, oc_url, ssl = self.utils.set_base_url(
            platform="qa"
        )
        version_app_qa = self.utils.get_isogeo_version(component="app")
        # check
        self.assertIsInstance(version_app_prod, str)
        self.assertIsInstance(version_app_qa, str)

    def test_get_isogeo_version_db(self):
        """Check DB version"""
        # prod
        version_db_prod = self.utils.get_isogeo_version(component="db")
        # qa
        platform, api_url, app_url, csw_url, mng_url, oc_url, ssl = self.utils.set_base_url(
            platform="qa"
        )
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
        platform, api_url, app_url, csw_url, mng_url, oc_url, ssl = (
            self.utils.set_base_url()
        )
        self.assertIsInstance(platform, str)
        self.assertIsInstance(api_url, str)
        self.assertIsInstance(ssl, bool)
        self.assertEqual(platform, "prod")
        self.assertEqual(api_url, self.utils.API_URLS.get("prod"))
        self.assertEqual(ssl, True)
        # qa
        platform, api_url, app_url, csw_url, mng_url, oc_url, ssl = self.utils.set_base_url(
            platform="qa"
        )
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
        url = self.utils.get_edit_url(
            md_id="0269803d50c446b09f5060ef7fe3e22b",
            md_type="vector-dataset",
            owner_id="32f7e95ec4e94ca3bc1afda960003882",
            tab="identification",
        )
        self.assertIsInstance(url, str)
        self.assertIn("app", url)
        self.assertIn("groups", url)
        urlparse(url)
        # again with type extracted from metadata model
        url = self.utils.get_edit_url(
            md_id="0269803d50c446b09f5060ef7fe3e22b",
            md_type="vectorDataset",
            owner_id="32f7e95ec4e94ca3bc1afda960003882",
            tab="identification",
        )

    def test_get_edit_url_bad_md_uuid(self):
        """Must raise an error if metadata/resource UUID check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(
                md_id="oh_my_bad_i_m_not_a_correct_uuid",
                md_type="vector-dataset",
                owner_id="32f7e95ec4e94ca3bc1afda960003882",
                tab="identification",
            )

    def test_get_edit_url_bad_md_type(self):
        """Must raise an error if metadata/resource type check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(
                md_id="0269803d50c446b09f5060ef7fe3e22b",
                md_type="bad_md_type",
                owner_id="32f7e95ec4e94ca3bc1afda960003882",
                tab="identification",
            )

    def test_get_edit_url_bad_wg_uuid(self):
        """Must raise an error if workgroup UUID check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(
                md_id="0269803d50c446b09f5060ef7fe3e22b",
                md_type="vector-dataset",
                owner_id="oh_my_bad_i_m_not_a_correct_uuid",
                tab="identification",
            )

    def test_get_edit_url_bad_tab(self):
        """Must raise an error if tab check fails."""
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(
                md_id="0269803d50c446b09f5060ef7fe3e22b",
                md_type="raster-dataset",
                owner_id="32f7e95ec4e94ca3bc1afda960003882",
                tab="attributes",
            )
        with self.assertRaises(ValueError):
            self.utils.get_edit_url(
                md_id="0269803d50c446b09f5060ef7fe3e22b",
                md_type="raster-dataset",
                owner_id="32f7e95ec4e94ca3bc1afda960003882",
                tab="what_a_tab_name",
            )

    # -- URLs Builders - request -------------------------------------
    def test_get_request_base_url(self):
        """Test URL request builder."""
        resource_url = self.utils.get_request_base_url("resources")
        self.assertEqual(
            resource_url, "https://{}.isogeo.com/resources/".format(self.utils.api_url)
        )

    # -- URLs Builders - view on web app -------------------------------------
    def test_get_view_url_ok(self):
        """Test URL builder for OpenCatalog and PixupPortal links."""
        # OpenCatalog
        oc_url = self.utils.get_view_url(
            webapp="oc",
            md_id="0269803d50c446b09f5060ef7fe3e22b",
            share_id="1e07910d365449b59b6596a9b428ecd9",
            share_token="TokenOhDearToken",
        )
        self.assertEqual(
            oc_url,
            "https://open.isogeo.com/s/1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken/r/0269803d50c446b09f5060ef7fe3e22b",
        )

        # PixUp portal - demo.isogeo.net sample
        pixup_url = self.utils.get_view_url(
            webapp="pixup_portal",
            md_id="0269803d50c446b09f5060ef7fe3e22b",
            portal_url="demo.isogeo.net",
        )
        self.assertEqual(
            pixup_url, "http://demo.isogeo.net/?muid=0269803d50c446b09f5060ef7fe3e22b"
        )

        # CSW - GetCapapabilities
        csw_getcap_url = self.utils.get_view_url(
            webapp="csw_getcap",
            share_id="1e07910d365449b59b6596a9b428ecd9",
            share_token="TokenOhDearToken",
        )
        self.assertEqual(
            csw_getcap_url,
            "https://services.api.isogeo.com/ows/s/1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken?"
            "service=CSW&version=2.0.2&request=GetCapabilities",
        )

        # CSW - GetRecordById
        csw_getrecordbyid_url = self.utils.get_view_url(
            webapp="csw_getrec",
            md_uuid_urn="urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b",
            share_id="1e07910d365449b59b6596a9b428ecd9",
            share_token="TokenOhDearToken",
        )
        self.assertEqual(
            csw_getrecordbyid_url,
            "https://services.api.isogeo.com/ows/s/"
            "1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken?service=CSW"
            "&version=2.0.2&request=GetRecordById"
            "&id=urn:isogeo:metadata:uuid:0269803d-50c4-46b0-9f50-60ef7fe3e22b"
            "&elementsetname=full&outputSchema=http://www.isotc211.org/2005/gmd",
        )

        # CSW - GetRecords #44
        csw_getrecords_url = self.utils.get_view_url(
            webapp="csw_getrecords",
            share_id="1e07910d365449b59b6596a9b428ecd9",
            share_token="TokenOhDearToken",
        )
        self.assertEqual(
            csw_getrecords_url,
            "https://services.api.isogeo.com/ows/s/"
            "1e07910d365449b59b6596a9b428ecd9/TokenOhDearToken?service=CSW"
            "&version=2.0.2&request=GetRecords&ResultType=results"
            "&ElementSetName=brief&maxRecords=20&OutputFormat=application/xml"
            "&OutputSchema=http://www.opengis.net/cat/csw/2.0.2"
            "&namespace=xmlns(csw=http://www.opengis.net/cat/csw/2.0.2)"
            "&TypeNames=csw:Record&startPosition=1",
        )

    def test_get_view_url_bad(self):
        """Test URL builder for web app with bad parameters."""
        with self.assertRaises(ValueError):
            self.utils.get_view_url(
                md_id="0269803d50c446b09f5060ef7fe3e22b",
                webapp="my_imaginary_webapp",
                portal_url="demo.isogeo.net",
            )
        with self.assertRaises(TypeError):
            self.utils.get_view_url(
                md_id="0269803d50c446b09f5060ef7fe3e22b",
                webapp="pixup_portal",
                my_nice_arg="a_nice_arg",
            )

    def test_register_webapp_custom_ok(self):
        """Test register a custom webapp and use it ot build view url."""
        # register
        self.assertNotIn("PPIGE v3", self.utils.WEBAPPS)
        self.utils.register_webapp(
            webapp_name="PPIGE v3",
            webapp_args=["md_id"],
            webapp_url="https://www.ppige-npdc.fr/portail/geocatalogue?uuid={md_id}",
        )
        self.assertIn("PPIGE v3", self.utils.WEBAPPS)
        # use it
        custom_url = self.utils.get_view_url(
            md_id="0269803d50c446b09f5060ef7fe3e22b", webapp="PPIGE v3"
        )
        self.assertEqual(
            custom_url,
            "https://www.ppige-npdc.fr/portail/geocatalogue?uuid=0269803d50c446b09f5060ef7fe3e22b",
        )

    def test_register_webapp_bad(self):
        """Must raise an error if web app arg is not in url."""
        with self.assertRaises(ValueError):
            self.utils.register_webapp(
                webapp_name="PPIGE v3",
                webapp_args=["md_id"],
                webapp_url="https://www.ppige-npdc.fr/portail/geocatalogue?uuid=",
            )

    # encoding -- see #32
    def test_decoding_rfc2047(self):
        """Test decoding func for filenames: """
        b = "=?UTF-8?B?VGhpcyBpcyBhIGhvcnNleTog8J+Qjg==?="
        self.utils.encoded_words_to_text(b)
        q = "=?UTF-8?Q?This is a horsey: =F0=9F=90=8E?="
        self.utils.encoded_words_to_text(q)
        d = q = '"=?UTF-8?Q?This is a horsey: =F0=9F=90=8E?="'
        self.utils.encoded_words_to_text(d)

    # pages counter
    def test_pages_counter(self):
        """Test search results pages counter to help pagination"""
        p_default = self.utils.pages_counter(total=50)
        self.assertEqual(p_default, 1)
        p_default = self.utils.pages_counter(total=50, page_size=10)
        self.assertEqual(p_default, 5)
        p_default = self.utils.pages_counter(total=156, page_size=22)
        self.assertEqual(p_default, 8)
