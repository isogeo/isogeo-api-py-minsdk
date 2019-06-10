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
from functools import wraps
from sys import platform as opersys

# 3rd party library
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

# modules
from isogeo_pysdk import api, version
from isogeo_pysdk.api_hooks import IsogeoHooks
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.models import Metadata
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
        timeout: tuple = (5, 30),
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
        self._thesauri_codes = {}  # Isogeo thesauri by names
        self._workgroups_names = {}  # Isogeo workgroups by names
        # user
        self._user = {}  # authenticated user profile
        # workgroup
        self._wg_applications_names = {}  # workgroup applications by names
        self._wg_catalogs_names = {}  # workgroup catalogs by names
        self._wg_contacts_emails = {}  # workgroup contacts by emails
        self._wg_contacts_names = {}  # workgroup contacts by names
        self._wg_datasources_names = {}  # workgroup datasources by names
        self._wg_datasources_urls = {}  # workgroup datasources by urls (location)
        self._wg_licenses_names = {}  # workgroup licenses by names
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
                "Mode value must be one of: ".format(" | ".join(self.AUTH_MODES))
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
        # self.api = api
        self.account = api.ApiAccount(self)
        self.application = api.ApiApplication(self)
        self.catalog = api.ApiCatalog(self)
        self.contact = api.ApiContact(self)
        self.datasource = api.ApiDatasource(self)
        self.keyword = api.ApiKeyword(self)
        self.license = api.ApiLicense(self)
        self.metadata = api.ApiResource(self)
        self.specification = api.ApiSpecification(self)
        self.thesaurus = api.ApiThesaurus(self)
        self.workgroup = api.ApiWorkgroup(self)

        # get API version
        logger.debug("Isogeo API version: {}".format(utils.get_isogeo_version()))
        logger.debug("Isogeo DB version: {}".format(utils.get_isogeo_version("db")))

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
            return {"Accept-Encoding": "gzip, deflate", "User-Agent": self.app_name}
        else:
            pass

    # -- DECORATORS -----------------------------------------------------------
    def _check_bearer_validity(decorated_func):
        """Check API Bearer token validity and refresh it if needed.

        Isogeo ID delivers authentication bearers which are valid during
        a certain time. So this decorator checks the validity of the token
        comparing with actual datetime (UTC) and renews it if necessary.
        See: https://tools.ietf.org/html/rfc6750#section-2

        :param decorated_func token: original function to execute after check
        """

        @wraps(decorated_func)
        def wrapper(self, *args, **kwargs):
            # compare token expiration date and ask for a new one if it's expired
            if datetime.now() < datetime.utcfromtimestamp(self.token.get("expires_at")):
                self.refresh_token(token_url=self.auto_refresh_url)
                logger.debug("Token was about to expire, so has been renewed.")
            else:
                logger.debug("Token is still valid.")
                pass

            # let continue running the original function
            return decorated_func(self, *args, **kwargs)

        return wrapper

    # -- METADATA = RESOURCE --------------------------------------------------
    # @_check_bearer_validity
    # def md_exists(self, resource_id: str) -> bool:
    #     """Check if the specified metadata exists or is available for the authenticated user.

    #     :param str resource_id: identifier of the resource to verify
    #     """
    #     url_md_check = "{}{}".format(
    #         utils.get_request_base_url("resources"), resource_id
    #     )

    #     return checker.check_api_response(self.get(url_md_check))

    # @_check_bearer_validity
    # def md_create(
    #     self,
    #     workgroup_id: str,
    #     resource_type: str,
    #     title: str,
    #     abstract: str = None,
    #     series: bool = 0,
    # ) -> dict:
    #     """Create a metadata from Isogeo database.

    #     :param str workgroup_id: identifier of the owner workgroup
    #     :param str resource_type: data type. Must be one of...
    #     :param str title: title
    #     :param str abstract: abstract (description)
    #     :param bool series: set if metadata is a series or not
    #     """
    #     # check metadata UUID
    #     if not checker.check_is_uuid(workgroup_id):
    #         raise ValueError("Workgroup ID is not a correct UUID.")
    #     else:
    #         pass

    #     # prepare metadata
    #     data = {
    #         "title": title,
    #         "abstract": abstract,
    #         "type": resource_type,
    #         "series": series,
    #     }

    #     # resource route
    #     url_md_create = utils.get_request_base_url(
    #         route="groups/{}/resources/".format(workgroup_id)
    #     )

    #     # request
    #     new_md = self.post(
    #         url_md_create,
    #         data=data,
    #         proxies=self.proxies,
    #         verify=self.ssl,
    #         timeout=self.timeout,
    #     )

    #     return new_md.json()

    # @_check_bearer_validity
    # def md_delete(self, resource_id: str) -> dict:
    #     """Delete a metadata from Isogeo database.

    #     :param str resource_id: identifier of the resource to delete
    #     """
    #     # resource route
    #     url_md_del = utils.get_request_base_url(
    #         route="resources/{}".format(resource_id)
    #     )

    #     # request
    #     md_deletion = self.delete(url_md_del)

    #     return md_deletion

    # @_check_bearer_validity
    # def md_update(self, metadata: Metadata) -> Metadata:
    #     """Update a metadata from Isogeo database.

    #     :param Metadata metadata: metadata (resource) to edit
    #     """
    #     # check metadata UUID
    #     # if not checker.check_is_uuid(workgroup_id):
    #     #     raise ValueError("Workgroup ID is not a correct UUID.")
    #     # else:
    #     #     pass

    #     # URL
    #     url_metadata_update = utils.get_request_base_url(
    #         route="resources/{}".format(metadata._id)
    #     )

    #     # request
    #     req_metadata_update = self.patch(
    #         url=url_metadata_update,
    #         json=metadata.to_dict_creation(),
    #         headers=self.header,
    #         proxies=self.proxies,
    #         timeout=self.timeout,
    #         verify=self.ssl,
    #     )

    #     # method ending
    #     return Metadata(**req_metadata_update.json())

    @_check_bearer_validity
    def md_associate_contacts(
        self, metadata: Metadata, contact_id: str, role="pointOfContact"
    ) -> dict:
        """associate a contact to a metadata.

        :param Metadata metadata: metadata (resource) to edit
        :param str contact_id: UUID of the contact to associate. Must exist into Isogeo or workgroup address book
        :param str role: role to assign to the contact
        """
        # check contact UUID
        if not checker.check_is_uuid(contact_id):
            raise ValueError("Contact ID is not a correct UUID.")
        else:
            pass

        # URL
        url_metadata_asso_contact = utils.get_request_base_url(
            route="resources/{}/contacts/{}".format(metadata._id, contact_id)
        )

        # request
        req_metadata_asso_contact = self.put(
            url=url_metadata_asso_contact,
            json={"role": role},
            headers=self.header,
            proxies=self.proxies,
            timeout=self.timeout,
            verify=self.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_asso_contact)
        if isinstance(req_check, tuple):
            return req_check

        # method ending
        return req_metadata_asso_contact.json()

    # -- LINKS --------------------------------------------------
    @_check_bearer_validity
    def link(self, metadata_id: str, link_id: str) -> dict:
        """Get an link.

        :param str link_id: link UUID to get
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # check contact UUID
        if not checker.check_is_uuid(link_id):
            raise ValueError("Link ID is not a correct UUID: {}".format(link_id))
        else:
            pass

        # request URL
        url_link = utils.get_request_base_url(
            route="resources/{}/links/{}".format(metadata_id, link_id)
        )

        link_req = self.get(
            url_link,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        checker.check_api_response(link_req)

        # add parent resource id to keep tracking
        link_augmented = link_req.json()
        link_augmented["parent_resource"] = metadata_id

        # end of method
        return link_augmented

    # -- WORKGROUPS --------------------------------------------------
    @_check_bearer_validity
    def workgroup_metadata(
        self,
        workgroup_id: str,
        order_by: str = "_created",
        order_dir: str = "desc",
        page_size: int = 100,
        offset: int = 0,
    ) -> dict:
        """List workgroup metadata.

        :param str workgroup_id: identifier of the owner workgroup
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # request parameters
        payload = {
            # "_include": include,
            # "_lang": self.lang,
            "_limit": page_size,
            "_offset": offset,
            "ob": order_by,
            "od": order_dir,
            # "q": query,
            # "s": share,
        }

        # build request url
        url_metadata_list = utils.get_request_base_url(
            route="groups/{}/resources/search".format(workgroup_id)
        )

        wg_metadata = self.get(
            url_metadata_list,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        wg_metadata = wg_metadata.json()

        # # if caching use or store the workgroup metadata
        # if caching and not self._wg_apps_names:
        #     self._wg_apps_names = {i.get("name"): i.get("_id") for i in wg_metadata}

        return wg_metadata


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    # ------------ Specific imports ----------------
    from dotenv import load_dotenv
    from os import environ
    import pprint
    from time import sleep, gmtime, strftime
    import urllib3

    # ------------ Log & debug ----------------
    logger = logging.getLogger()
    logging.captureWarnings(True)
    logger.setLevel(logging.DEBUG)

    # ------------ Real start ----------------
    # load application credentials from downloaded file
    credentials = utils.credentials_loader("client_secrets_scripts.json")

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
        platform=environ.get("ISOGEO_PLATFORM"),
    )

    # getting a token
    isogeo.connect(
        username=environ.get("ISOGEO_USER_NAME"),
        password=environ.get("ISOGEO_USER_PASSWORD"),
    )

    # misc
    discriminator = strftime("%Y-%m-%d_%H%M%S", gmtime())
    WG_TEST_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

    # -- END -------
    isogeo.close()  # close session
