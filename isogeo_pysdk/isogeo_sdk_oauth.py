# -*- coding: UTF-8 -*-
#! python3

# -----------------------------------------------------------------------------
# Name:         Isogeo
# Purpose:      Python minimalist SDK to use Isogeo API
#
# Author:       Julien Moura (@geojulien) for Isogeo
#
# Python:       3.6.x
# Created:      22/12/2015
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import locale
import logging
from datetime import datetime
from sys import platform as opersys

# 3rd party library
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

# modules
from isogeo_pysdk import api, version
from isogeo_pysdk.api_hooks import IsogeoHooks
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.models import User
from isogeo_pysdk.utils import IsogeoUtils

# ##############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()

# #############################################################################
# ########## Classes ###############
# ##################################


class IsogeoSession(OAuth2Session):

    # -- ATTRIBUTES -----------------------------------------------------------
    AUTH_MODES = {"group", "user_private", "user_public"}

    def __init__(
        self,
        client_id=None,
        auto_refresh_url=None,
        redirect_uri=None,
        scope=None,
        state=None,
        token=None,
        token_updater=None,
        # custom
        app_name: str = "isogeo-pysdk-writer/{}".format(version),
        auth_mode: str = "user_private",
        client_secret: str = None,
        lang: str = "en",
        platform: str = "qa",
        proxy: dict = None,
        timeout: tuple = (15, 45),
        # additional
        **kwargs,
    ):

        # custom hooks
        self.custom_hooks = IsogeoHooks()

        self.app_name = app_name
        self.client_secret = client_secret
        self.timeout = (
            timeout
        )  # default timeout (see: https://2.python-requests.org/en/master/user/advanced/#timeouts)

        # -- CACHE
        # platform
        self._applications_names = {}  # Isogeo applications by names
        self._coordinate_systems = []  # Isogeo coordinate-systems
        self._directives = {}  # EU environment directives used as INSPIRE limitations
        self._formats_geo = []  # Isogeo formats for geographic data
        self._formats_nogeo = []  # Isogeo formats for non-geographic data
        self._links_kinds_actions = []  # Isogeo matrix for links kind/action
        self._shares_names = {}  # Isogeo applications by names
        self._thesauri_codes = {}  # Isogeo thesauri by codes
        self._workgroups_names = {}  # Isogeo workgroups by names
        # user
        self._user = User()  # authenticated user profile
        # workgroup
        self._wg_applications_names = {}  # workgroup applications by names
        self._wg_catalogs_names = {}  # workgroup catalogs by names
        self._wg_contacts_emails = {}  # workgroup contacts by emails
        self._wg_contacts_names = {}  # workgroup contacts by names
        self._wg_coordinate_systems = []  # workgroup coordinate-systems
        self._wg_datasources_names = {}  # workgroup datasources by names
        self._wg_datasources_urls = {}  # workgroup datasources by urls (location)
        self._wg_licenses_names = {}  # workgroup licenses by names
        self._wg_shares_names = {}  # workgroup shares by names
        self._wg_specifications_names = {}  # workgroup specifications by names

        # checking internet connection
        if not checker.check_internet_connection():
            raise EnvironmentError("Internet connection issue.")
        else:
            pass

        # testing parameters
        if not checker.check_is_uuid(client_id.split("-")[-1]):
            logger.error("Client ID structure length issue: it should be 64 chars.")
            raise ValueError(
                "Client ID isn't good: part after name is expected to be a valid UUID."
            )
        else:
            pass
        if len(client_secret) != 64:
            logger.error("App secret length issue: it should be 64 chars.")
            raise ValueError(1, "Client Secret isn't good: it must be 64 chars.")
        else:
            pass

        # auth mode
        if auth_mode not in self.AUTH_MODES:
            logger.error("Auth mode value is not good: {}".format(auth_mode))
            raise ValueError(
                "Mode value must be one of: {}".format(" | ".join(self.AUTH_MODES))
            )
        else:
            self.auth_mode = auth_mode

        # platform to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            platform
        )
        # setting language
        if lang.lower() not in ("fr", "en"):
            logger.warning(
                "Isogeo API is only available in English ('en', "
                "default) or French ('fr'). "
                "Language has been set on English."
            )
            self.lang = "en"
        else:
            self.lang = lang.lower()

        # setting locale according to the language passed
        # try:
        #     if opersys == "win32":
        #         if lang.lower() == "fr":
        #             locale.setlocale(locale.LC_ALL, str("fra_fra"))
        #         else:
        #             locale.setlocale(locale.LC_ALL, str("uk_UK"))
        #     else:
        #         if lang.lower() == "fr":
        #             locale.setlocale(locale.LC_ALL, str("fr_FR.utf8"))
        #         else:
        #             locale.setlocale(locale.LC_ALL, str("en_GB.utf8"))
        # except locale.Error as e:
        #     logger.error(
        #         "Selected locale ({}) is not installed: {}".format(lang.lower(), e)
        #     )

        # handling proxy parameters
        # see: http://docs.python-requests.org/en/latest/user/advanced/#proxies
        if proxy and isinstance(proxy, dict) and "http" in proxy:
            logger.debug("Proxy enabled")
            self.proxies = proxy
        elif proxy and not isinstance(proxy, dict):
            raise TypeError(
                "Proxy syntax error. Must be a dict:"
                "{ 'protocol': "
                "'http://user:password@proxy_url:port' }."
                " e.g.: "
                "{'http': 'http://martin:1234@10.1.68.1:5678',"
                "'https': 'http://martin:p4ssW0rde@10.1.68.1:5678'}"
            )
        else:
            self.proxies = {}
            logger.debug("No proxy set. Use default configuration.")
            pass

        # set client
        self.auto_refresh_kwargs = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        self.client = LegacyApplicationClient(client_id=client_id)

        # load routes as subclass
        self.account = api.ApiAccount(self)
        self.application = api.ApiApplication(self)
        self.catalog = api.ApiCatalog(self)
        self.contact = api.ApiContact(self)
        self.coordinate_system = self.srs = api.ApiCoordinateSystem(self)
        self.datasource = api.ApiDatasource(self)
        self.directive = api.ApiDirective(self)
        self.formats = api.ApiFormat(self)
        self.keyword = api.ApiKeyword(self)
        self.invitation = api.ApiInvitation(self)
        self.license = api.ApiLicense(self)
        self.metadata = api.ApiMetadata(self)
        self.services = api.ApiService(self)
        self.share = api.ApiShare(self)
        self.specification = api.ApiSpecification(self)
        self.thesaurus = api.ApiThesaurus(self)
        self.user = api.ApiUser(self)
        self.workgroup = api.ApiWorkgroup(self)

        return super().__init__(
            client_id=client_id,
            client=self.client,
            auto_refresh_url=auto_refresh_url,
            auto_refresh_kwargs=self.auto_refresh_kwargs,
            scope=scope,
            redirect_uri=redirect_uri,
            token=token,
            state=state,
            token_updater=token_updater,
            **kwargs,
        )

    def connect(self, username: str, password: str):
        """Authenticate application with user credentials and get token.

        Isogeo API uses oAuth 2.0 protocol (https://tools.ietf.org/html/rfc6749)
        see: http://help.isogeo.com/api/fr/authentication/concepts.html

        :param str username: user login (email)
        :param str password: user password
        """
        # get token
        self.token = self.fetch_token(
            token_url=self.auto_refresh_url,
            username=username,
            password=password,
            client_id=self.client_id,
            client_secret=self.client_secret,
            verify=self.ssl,
        )

        # get authenticated user informations
        self.account.account()

    # -- PROPERTIES -----------------------------------------------------------
    @property
    def header(self) -> dict:
        if self.auth_mode == "group":
            return {
                "Authorization": "Bearer {}".format(self.token.get("access_token")),
                "user-agent": self.app_name,
            }
        elif self.auth_mode == "user_private":
            return {
                "Accept-Encoding": "gzip, deflate, br",
                "User-Agent": self.app_name,
                # "Content-Type": "application/json; charset=utf-8",
                # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        else:
            pass


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    # ------------ Specific imports ----------------
    from dotenv import load_dotenv
    from logging.handlers import RotatingFileHandler
    from os import environ
    import pprint
    from time import sleep, gmtime, strftime
    import urllib3

    from isogeo_pysdk.models import Keyword, Share

    # ------------ Log & debug ----------------
    logger = logging.getLogger()
    logging.captureWarnings(True)
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)

    log_format = logging.Formatter(
        "%(asctime)s || %(levelname)s "
        "|| %(module)s - %(lineno)d ||"
        " %(funcName)s || %(message)s"
    )

    # debug to the file
    log_file_handler = RotatingFileHandler("dev_debug.log", "a", 3000000, 1)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(log_format)

    # info to the console
    log_console_handler = logging.StreamHandler()
    log_console_handler.setLevel(logging.INFO)
    log_console_handler.setFormatter(log_format)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_console_handler)

    # ------------ Real start ----------------
    # get user ID as environment variables
    load_dotenv("dev.env")

    # ignore warnings related to the QA self-signed cert
    if environ.get("ISOGEO_PLATFORM").lower() == "qa":
        urllib3.disable_warnings()

    # instanciate
    isogeo = IsogeoSession(
        client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
        client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
        auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
        platform=environ.get("ISOGEO_PLATFORM", "qa"),
    )

    # getting a token
    isogeo.connect(
        username=environ.get("ISOGEO_USER_NAME"),
        password=environ.get("ISOGEO_USER_PASSWORD"),
    )

    # misc
    discriminator = strftime("%Y-%m-%d_%H%M%S", gmtime())
    METADATA_TEST_FIXTURE_UUID = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE")
    WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

    # -- END -------
    isogeo.close()  # close session
