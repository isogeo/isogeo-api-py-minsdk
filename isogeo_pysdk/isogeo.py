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
import logging

# 3rd party library
from oauthlib.oauth2 import BackendApplicationClient, LegacyApplicationClient
from requests_oauthlib import OAuth2Session

# modules
from isogeo_pysdk.__about__ import __version__ as version
from isogeo_pysdk import api
from isogeo_pysdk.api_hooks import IsogeoHooks
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.models import Application, User
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


class Isogeo(OAuth2Session):
    """Main class in Isogeo API Python wrapper. Manage authentication and requests to the REST API.
    Inherits from :class:`requests_oauthlib.OAuth2Session`.

    **Inherited:**

    :param str client_id: Client id obtained during registration
    :param str redirect_uri: Redirect URI you registered as callback
    :param list auto_refresh_url: Refresh token endpoint URL, must be HTTPS. Supply
                    this if you wish the client to automatically refresh
                    your access tokens.

    **Package specific:**

    :param str client_secret: application oAuth2 secret
    :param str auth_mode: oAuth2 authentication flow to use. Must be one of 'AUTH_MODES'
    :param str platform: to request production or quality assurance
    :param dict proxy: dictionary of proxy settings as described in `Requests <https://2.python-requests.org/en/master/user/advanced/#proxies>`_
    :param str lang: API localization ("en" or "fr"). Defaults to 'fr'.
    :param str app_name: to custom the application name and user-agent


    :returns: authenticated requests Session you can use to send requests to the API.
    :rtype: requests_oauthlib.OAuth2Session

    :Example:

    .. code-block:: python

        # using oAuth2 Password Credentials Grant (Legacy Application)
        #  (for scripts executed on the server-side with user credentials
        #  but without requiring user action)
        isogeo = Isogeo(
            client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
            auth_mode="user_legacy",
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )

        # getting a token
        isogeo.connect(
            username=environ.get("ISOGEO_USER_NAME"),
            password=environ.get("ISOGEO_USER_PASSWORD"),
        )

        # using oAuth2 Client Credentials Grant (Backend Application)
        #  (for scripts executed on the server-side with only application credentials
        #  but limited to read-only in Isogeo API)
        isogeo = Isogeo(
            client_id=environ.get("ISOGEO_API_DEV_ID"),
            client_secret=environ.get("ISOGEO_API_DEV_SECRET"),
            auth_mode="group",
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )

        # getting a token
        isogeo.connect()

    """

    # -- ATTRIBUTES -----------------------------------------------------------
    AUTH_MODES = {
        "group": {"client_id": str, "client_secret": str},
        "user_legacy": {
            "client_id": str,
            "client_secret": str,
            "auto_refresh_url": str,
        },
        "user_private": {
            "client_id": str,
            "client_secret": str,
            "auto_refresh_url": str,
            "redirect_uris": list,
        },
        "user_public": {
            "client_id": str,
            "client_secret": str,
            "auto_refresh_url": str,
            "redirect_uris": list,
        },
        "guess": {},
    }

    def __init__(
        self,
        # custom
        auth_mode: str = "group",
        client_secret: str = None,
        platform: str = "qa",
        proxy: dict = None,
        timeout: tuple = (15, 45),
        lang: str = "fr",
        app_name: str = "isogeo-pysdk/{}".format(version),
        # additional
        **kwargs,
    ):
        # some vars
        self.app_name = app_name  # custom settings
        client_id = kwargs.get("client_id")
        self.client_secret = client_secret
        self.custom_hooks = IsogeoHooks()  # custom hooks
        self.timeout = timeout  # default timeout

        # auth mode
        if auth_mode and auth_mode not in self.AUTH_MODES:
            raise ValueError(
                "Mode value must be one of: {}".format(" | ".join(self.AUTH_MODES))
            )
        else:
            self.auth_mode = auth_mode

        # -- CACHE
        # platform
        self._applications_names = {}  # Isogeo applications by names
        self._coordinate_systems = []  # Isogeo coordinate-systems
        self._directives = {}  # EU environment directives used as INSPIRE limitations
        self._formats_geo = []  # Isogeo formats for geographic data
        self._formats_nogeo = []  # Isogeo formats for non-geographic data
        self._links_kinds_actions = []  # Isogeo matrix for links kind/action
        self._shares = {}  # Isogeo applications by names
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
        self._wg_shares = {}  # workgroup shares
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

        # platform to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            platform
        )
        # setting language
        if lang.lower() not in ("fr", "en"):
            logger.warning(
                "Isogeo API is only available in English ('en', default) or French ('fr'). Language has been set on English."
            )
            self.lang = "en"
        else:
            self.lang = lang.lower()
        utils.set_lang_and_locale(self.lang)

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

        if auth_mode == "user_legacy":
            self.client = LegacyApplicationClient(client_id=client_id)
        elif auth_mode == "group":
            self.client = BackendApplicationClient(client_id=client_id)
        else:
            raise NotImplementedError(
                "Mode {} is not implemented yet.".format(auth_mode)
            )

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
        self.search = api.ApiSearch(self).search
        self.services = api.ApiService(self)
        self.share = api.ApiShare(self)
        self.specification = api.ApiSpecification(self)
        self.thesaurus = api.ApiThesaurus(self)
        self.user = api.ApiUser(self)
        self.workgroup = api.ApiWorkgroup(self)

        super().__init__(
            # client_id=client_id,
            client=self.client,
            # auto_refresh_url=kwargs.get("auto_refresh_url"),
            auto_refresh_kwargs=self.auto_refresh_kwargs,
            **kwargs,
        )

    def connect(self, username: str = None, password: str = None):
        """Authenticate application with user credentials and get token.

        Isogeo API uses oAuth 2.0 protocol (https://tools.ietf.org/html/rfc6749)
        see: http://help.isogeo.com/api/fr/authentication/concepts.html

        :param str username: user login (email)
        :param str password: user password
        """
        if self.auth_mode == "user_legacy":
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
            self.account.get()
        elif self.auth_mode == "group":
            # get token
            self.token = self.fetch_token(
                token_url=self.auto_refresh_url,
                client_id=self.client_id,
                client_secret=self.client_secret,
                verify=self.ssl,
            )
            # get authenticated application informations
            associated_shares = self.share.listing(caching=1)
            if not len(associated_shares):
                logger.warning("No shares are feeding this application.")
                self.app_properties = None
            else:
                # if application has associated shares, then retrieve informations
                logger.info(
                    "This application is feeded by {} share(s).".format(
                        len(associated_shares)
                    )
                )
                self.app_properties = Application(
                    **self.share.listing()[0].get("applications")[0]
                )

    # -- PROPERTIES -----------------------------------------------------------
    @property
    def header(self) -> dict:
        if self.auth_mode == "group":
            return {
                "Authorization": "Bearer {}".format(self.token.get("access_token")),
                "user-agent": self.app_name,
            }
        elif self.auth_mode == "user_legacy":
            return {
                "Accept-Encoding": "gzip, deflate, br",
                "User-Agent": self.app_name,
                # "Content-Type": "application/json; charset=utf-8",
                # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        else:
            pass

    @classmethod
    def guess_auth_mode(self):
        raise NotImplementedError


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

    # # for oAuth2 Legacy Flow
    # isogeo = Isogeo(
    #     auth_mode="user_legacy",
    #     client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
    #     client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
    #     auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
    #     platform=environ.get("ISOGEO_PLATFORM", "qa"),
    # )

    # # getting a token
    # isogeo.connect(
    #     username=environ.get("ISOGEO_USER_NAME"),
    #     password=environ.get("ISOGEO_USER_PASSWORD"),
    # )

    # for oAuth2 Backend (Client Credentials Grant) Flow
    isogeo = Isogeo(
        auth_mode="group",
        client_id=environ.get("ISOGEO_API_GROUP_CLIENT_ID"),
        client_secret=environ.get("ISOGEO_API_GROUP_CLIENT_SECRET"),
        auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
        platform=environ.get("ISOGEO_PLATFORM", "qa"),
    )

    # getting a token
    isogeo.connect()

    # misc
    discriminator = strftime("%Y-%m-%d_%H%M%S", gmtime())
    METADATA_TEST_FIXTURE_UUID = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE")
    WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

    from isogeo_pysdk import Metadata

    search_complete = isogeo.search(
        whole_results=1,
        query="type:dataset owner:f234550ff1d5412fb2c67ee98d826731",
        include="all",
        order_by="_modified",
        order_dir="desc",
    )

    # -- END -------
    isogeo.close()  # close session
