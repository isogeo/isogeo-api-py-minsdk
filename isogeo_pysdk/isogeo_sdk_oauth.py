# -*- coding: UTF-8 -*-
#! python3

# -----------------------------------------------------------------------------
# Name:         Isogeo
# Purpose:      Python minimalist SDK to use Isogeo API
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      22/12/2015
# Updated:      10/01/2016
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import locale
import logging
from math import ceil
import re
from sys import platform as opersys

# 3rd party library
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

# modules
try:
    from isogeo_sdk import version
    from . import checker
    from . import utils
except (ImportError, ValueError, SystemError):
    import checker
    import utils

# ##############################################################################
# ########## Globals ###############
# ##################################

checker = checker.IsogeoChecker()
utils = utils.IsogeoUtils()

# #############################################################################
# ########## Classes ###############
# ##################################


class IsogeoSession(OAuth2Session):

    # -- ATTRIBUTES -----------------------------------------------------------
    AUTH_MODES = {"group", "user_private", "user_public"}

    _THESAURI_DICT = {
        "isogeo": "1616597fbc4348c8b11ef9d59cf594c8",
        "inspire-theme": "926c676c380046d7af99bcae343ac813",
        "iso19115-topic": "926f969ee2bb470a84066625f68b96bb",
    }

    def __init__(
        self,
        client_id=None,
        client=None,
        auto_refresh_url=None,
        auto_refresh_kwargs=None,
        scope=None,
        redirect_uri=None,
        token=None,
        state=None,
        token_updater=None,
        # custom
        client_secret=None,
        proxy: dict = None,
        auth_mode: str = "user_private",
        platform: str = "prod",
        lang: str = "en",
        app_name: str = "isogeo-pysdk-writer/{}".format(version),
        # additional
        **kwargs,
    ):

        self.app_name = app_name
        self.client_secret = client_secret
        self.prot = "https"

        # checking internet connection
        if not checker.check_internet_connection():
            raise EnvironmentError("Internet connection issue.")
        else:
            pass

        # testing parameters
        if len(client_secret) != 64:
            logging.error("App secret length issue: it should be 64 chars.")
            raise ValueError(1, "Secret isn't good: it must be 64 chars.")
        else:
            pass

        # auth mode
        if auth_mode not in self.AUTH_MODES:
            logging.error("Auth mode value is not good: {}".format(auth_mode))
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
            logging.warning(
                "Isogeo API is only available in English ('en', "
                "default) or French ('fr'). "
                "Language has been set on English."
            )
            self.lang = "en"
        else:
            self.lang = lang.lower()

        # handling proxy parameters
        # see: http://docs.python-requests.org/en/latest/user/advanced/#proxies
        if proxy and isinstance(proxy, dict) and "http" in proxy:
            logging.debug("Proxy enabled")
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
            logging.debug("No proxy set. Use default configuration.")
            pass

        # get API version
        logging.debug("Isogeo API version: {}".format(utils.get_isogeo_version()))
        logging.debug("Isogeo DB version: {}".format(utils.get_isogeo_version("db")))

        return super().__init__(
            client_id=client_id,
            client=client,
            auto_refresh_url=auto_refresh_url,
            auto_refresh_kwargs=auto_refresh_kwargs,
            scope=scope,
            redirect_uri=redirect_uri,
            token=token,
            state=state,
            token_updater=token_updater,
            **kwargs,
        )

    def connect(self, username, password):

        return self.fetch_token(
            token_url=self.auto_refresh_url,
            username=username,
            password=password,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

    # -- PROPERTIES -----------------------------------------------------------
    @property
    def header(self) -> dict:
        if self.auth_mode == "group":
            return {
                "Authorization": "Bearer {}".format(self.token.get("access_token")),
                "user-agent": self.app_name,
            }
        elif self.auth_mode == "user_private":
            return {"user-agent": self.app_name}
        else:
            pass

    # -- KEYWORDS -----------------------------------------------------------

    def thesauri(self, token: dict = None, prot: str = "https") -> dict:
        """Get list of available thesauri.

        :param str token: API auth token
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # passing auth parameter
        thez_url = "{}://v1.{}.isogeo.com/thesauri".format(prot, self.api_url)
        thez_req = self.get(
            thez_url, headers=self.header, proxies=self.proxies, verify=self.ssl
        )

        # checking response
        checker.check_api_response(thez_req)

        # end of method
        return thez_req.json()

    def thesaurus(
        self,
        token: dict = None,
        thez_id: str = "1616597fbc4348c8b11ef9d59cf594c8",
        prot: str = "https",
    ) -> dict:
        """Get a thesaurus.

        :param str token: API auth token
        :param str thez_id: thesaurus UUID
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # handling request parameters
        payload = {"tid": thez_id}

        # passing auth parameter
        thez_url = "{}://v1.{}.isogeo.com/thesauri/{}".format(
            prot, self.api_url, thez_id
        )
        thez_req = self.get(
            thez_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
        )

        # checking response
        checker.check_api_response(thez_req)

        # end of method
        return thez_req.json()

    def keywords(
        self,
        token: dict = None,
        thez_id: str = "1616597fbc4348c8b11ef9d59cf594c8",
        query: str = "",
        offset: int = 0,
        order_by: str = "text",  # available values : count.group, count.isogeo, text
        order_dir: str = "desc",
        page_size: int = 20,
        specific_md: list = [],
        specific_tag: list = [],
        include: list = [],
        prot: str = "https",
    ) -> dict:
        """Search for keywords within a specific thesaurus.

        :param str token: API auth token
        :param str thez_id: thesaurus UUID
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # specific resources specific parsing
        specific_md = checker._check_filter_specific_md(specific_md)
        # sub resources specific parsing
        include = checker._check_filter_includes(include, "keyword")
        # specific tag specific parsing
        specific_tag = checker._check_filter_specific_tag(specific_tag)

        # handling request parameters
        payload = {
            "_id": specific_md,
            "_include": include,
            "_limit": page_size,
            "_offset": offset,
            "_tag": specific_tag,
            "tid": thez_id,
            "ob": order_by,
            "od": order_dir,
            "q": query,
        }

        # search request
        keywords_url = "{}://v1.{}.isogeo.com/thesauri/{}/keywords/search".format(
            prot, self.api_url, thez_id
        )

        kwds_req = self.get(
            keywords_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
        )

        # checking response
        checker.check_api_response(kwds_req)

        # end of method
        return kwds_req.json()

    # -- LICENCES ---------------------------------------------
    def licenses(
        self, token: dict = None, owner_id: str = None, prot: str = "https"
    ) -> dict:
        """Get information about licenses owned by a specific workgroup.

        :param str token: API auth token
        :param str owner_id: workgroup UUID
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # handling request parameters
        payload = {"gid": owner_id}

        # search request
        licenses_url = "{}://v1.{}.isogeo.com/groups/{}/licenses".format(
            prot, self.api_url, owner_id
        )
        licenses_req = self.get(
            licenses_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
        )

        # checking response
        req_check = checker.check_api_response(licenses_req)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return licenses_req.json()

    def license(self, license_id: str, token: dict = None, prot: str = "https") -> dict:
        """Get details about a specific license.

        :param str token: API auth token
        :param str license_id: license UUID
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # handling request parameters
        payload = {"lid": license_id}

        # search request
        license_url = "{}://v1.{}.isogeo.com/licenses/{}".format(
            prot, self.api_url, license_id
        )
        license_req = self.get(
            license_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
        )

        # checking response
        checker.check_api_response(license_req)

        # end of method
        return license_req.json()

    def create(
        self, workgroup_id: str, resource_type: str, title: str, abstract: str, series: bool = 0
    ) -> dict:
        """Create a metadata from Isogeo database.

        :param str workgroup_id: identifier of the owner workgroup
        :param str resource_type: type of metadata to create. Must be one of...
        :param str title: title of metadata to create
        :param bool series: set if metadata is a series or not
        """
        # check metadata UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        data = {"title": title, "abstract": abstract, "type": resource_type, "series": series}

        url_md_create = "{}://v1.{}.isogeo.com/groups/{}/resources/".format(
            self.prot, self.api_url, workgroup_id
        )

        new_md = self.post(
            url_md_create, data=data, proxies=self.proxies, verify=self.ssl
        )

        return new_md.json()

    def md_delete(self, resource_id: str) -> dict:
        """Delete a metadata from Isogeo database.

        :param str resource_id: identifier of the resource to delete
        """
        url_md_del = "{}://{}.isogeo.com/resources/{}".format(
            self.prot, self.api_url, resource_id
        )

        md_deletion = self.delete(url_md_del)

        return md_deletion


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    # ------------ Specific imports ----------------
    from os import environ
    from dotenv import load_dotenv

    # ------------ Log & debug ----------------
    logger = logging.getLogger()
    logging.captureWarnings(True)
    logger.setLevel(logging.INFO)

    # ------------ Real start ----------------
    # load application credentials from downloaded file
    credentials = utils.credentials_loader("client_secrets_scripts.json")

    # get user ID as environment variables
    load_dotenv("dev.env", verbose=1)

    # instanciate
    isogeo = IsogeoSession(
        client=LegacyApplicationClient(client_id=credentials.get("client_id")),
        auto_refresh_url="https://id.api.isogeo.com/oauth/token",
        client_secret=credentials.get("client_secret"),
    )

    # getting a token
    token = isogeo.connect(username=environ.get("ISOGEO_USER_NAME"),
                           password=environ.get("ISOGEO_USER_PASSWORD"))

    # licenses
    lics = isogeo.licenses(owner_id="32f7e95ec4e94ca3bc1afda960003882")
    print(lics)

    # memo : par défaut order_dir = asc
    k = isogeo.keywords(thez_id="1616597fbc4348c8b11ef9d59cf594c8",
                        order_by="count.isogeo",
                        order_dir="desc",
                        page_size=10,
                        include="all"
                        )
    print(k)
