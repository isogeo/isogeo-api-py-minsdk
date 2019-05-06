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
from datetime import datetime, timedelta
from functools import wraps
from math import ceil
import re
from sys import platform as opersys

# 3rd party library
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

# modules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.models import (
    Catalog,
    Contact,
    Event,
    License,
    Link,
    Specification,
    User,
    Workgroup,
)
from isogeo_pysdk.utils import IsogeoUtils
from isogeo_pysdk import version


# ##############################################################################
# ########## Globals ###############
# ##################################

checker = IsogeoChecker()
utils = IsogeoUtils()

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
        app_name: str = "isogeo-pysdk-writer/{}".format(version),
        auth_mode: str = "user_private",
        client_secret: str = None,
        lang: str = "en",
        platform: str = "prod",
        proxy: dict = None,
        timeout: tuple = (5, 30),
        # additional
        **kwargs,
    ):

        self.app_name = app_name
        self.client_secret = client_secret
        self.timeout = (
            timeout
        )  # default timeout (see: https://2.python-requests.org/en/master/user/advanced/#timeouts)

        # caching
        self._user = {}             # authenticated user profile
        self._wg_cts_emails = {}    # workgroup contacts by emails
        self._wg_cts_names = {}     # workgroup contacts by names
        self._wg_cats_names = {}    # workgroup catalogs by names

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
        )

        # get authenticated user informations
        self.account()

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
                logging.debug("Token was about to expire, so has been renewed.")
            else:
                logging.debug("Token is still valid.")
                pass

            # let continue running the original function
            return decorated_func(self, *args, **kwargs)

        return wrapper

    # -- ACCOUNT AND MEMBERSHIPS -------------------------------------------------------
    def account(self, caching: bool = 1) -> User:
        """Get authenticated user account(= profile) informations.

        :param bool caching: option to cache the response
        """
        # request url
        url_account = utils.get_request_base_url(route="account")

        # build request
        account_req = self.get(
            url_account,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )
        # check request response
        checker.check_api_response(account_req)

        # if caching use or store the response
        if caching and not self._user:
            self._user = User(**account_req.json())

        # end of method
        return User(**account_req.json())

    def account_update(self, user_account: User) -> User:
        """Update authenticated user account(= profile) informations.

        :param class user_account: user account model object to update
        """
        # check account UUID
        if not checker.check_is_uuid(user_account._id):
            raise ValueError("User account ID is not a correct UUID: {}".format(user_account._id))
        else:
            pass

        # request url
        url_account = utils.get_request_base_url(route="account")

        # build request
        account_req = self.put(
            url=url_account,
            data=user_account.to_dict(),
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )
        # check request response
        checker.check_api_response(account_req)

        # if caching use or store the response
        self._user = User(**account_req.json())

        # end of method
        return User(**account_req.json())

    # -- METADATA = RESOURCE --------------------------------------------------
    def resource(
        self, resource_id: str = None, subresource=None, include: list = []
    ) -> dict:
        """Get complete or partial metadata about one specific resource.

        :param str resource_id: metadata UUID to get
        :param list include: subresources that should be included.
         Must be a list of strings. Available values: 'isogeo.SUBRESOURCES'
        """
        # if subresource route
        if isinstance(subresource, str):
            subresource = "/{}".format(checker._check_subresource(subresource))
        else:
            subresource = ""
            # _includes specific parsing
            include = checker._check_filter_includes(include)

        # handling request parameters
        payload = {"id": resource_id, "_include": include}
        # resource search
        md_url = "{}{}{}".format(
            utils.get_request_base_url(route="resources"), resource_id, subresource
        )

        resource_req = self.get(
            md_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )
        checker.check_api_response(resource_req)

        # end of method
        return resource_req.json()

    def md_exists(self, resource_id: str) -> bool:
        """Check if the specified metadata exists or is available for the authenticated user.

        :param str resource_id: identifier of the resource to verify
        """
        url_md_check = "{}{}".format(
            utils.get_request_base_url("resources"), resource_id
        )

        return checker.check_api_response(self.get(url_md_check))

    def md_create(
        self,
        workgroup_id: str,
        resource_type: str,
        title: str,
        abstract: str = None,
        series: bool = 0,
    ) -> dict:
        """Create a metadata from Isogeo database.

        :param str workgroup_id: identifier of the owner workgroup
        :param str resource_type: data type. Must be one of...
        :param str title: title
        :param str abstract: abstract (description)
        :param bool series: set if metadata is a series or not
        """
        # check metadata UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # prepare metadata
        data = {
            "title": title,
            "abstract": abstract,
            "type": resource_type,
            "series": series,
        }

        # resource route
        url_md_create = utils.get_request_base_url(
            route="groups/{}/resources/".format(workgroup_id)
        )

        # request
        new_md = self.post(
            url_md_create,
            data=data,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        return new_md.json()

    def md_delete(self, resource_id: str) -> dict:
        """Delete a metadata from Isogeo database.

        :param str resource_id: identifier of the resource to delete
        """
        # resource route
        url_md_del = utils.get_request_base_url(
            route="resources/{}".format(resource_id)
        )

        # request
        md_deletion = self.delete(url_md_del)

        return md_deletion

    # -- CATALOGS --------------------------------------------------
    def catalog(
        self, workgroup_id: str, catalog_id: str, include: list = ["count"]
    ) -> dict:
        """Get a catalog of a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param str catalog_id: catalog UUID to get
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # handle include
        # include = checker._check_filter_includes(include, "catalog")

        # handling request parameters
        payload = {"_include": include}

        # catalog route
        url_catalog = utils.get_request_base_url(
            route="groups/{}/catalogs/{}".format(workgroup_id, catalog_id)
        )

        # request
        req = self.get(
            url_catalog,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )
        checker.check_api_response(req)

        # handle bad JSON attribute
        catalog = req.json()
        catalog["scan"] = catalog.pop("$scan")

        # end of method
        return catalog

    def catalog_create(
        self, workgroup_id: str, check_exists: bool = 1, catalog: object = Catalog()
    ) -> dict:
        """Add a new catalog to a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param int check_exists: check if a catalog already exists inot the workgroup:

        - 0 = no check
        - 1 = compare name [DEFAULT]

        :param class catalog: Catalog model object to create
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # check if catalog already exists in workgroup
        if check_exists:
            # retrieve workgroup catalogs
            if not self._wg_cats_names:
                self.workgroup_catalogs(workgroup_id=workgroup_id, include=[])
            # check
            if catalog.name in self._wg_cats_names:
                logging.debug(
                    "Catalog with the same name already exists: {}. Use 'catalog_update' instead.".format(
                        catalog.name
                    )
                )
                return False

        # build request url
        url_cat_create = utils.get_request_base_url(
            route="groups/{}/catalogs".format(workgroup_id)
        )

        new_cat = self.post(
            url_cat_create,
            data=catalog.to_dict_creation(),
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # handle bad JSON attribute
        catalog = new_cat.json()
        catalog["scan"] = catalog.pop("$scan")

        return catalog

    def catalog_delete(self, workgroup_id: str, catalog_id: str) -> dict:
        """Delete a catalog from Isogeo database.

        :param str workgroup_id: identifier of the owner workgroup
        :param str catalog_id: identifier of the catalog to delete
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # check catalog UUID
        if not checker.check_is_uuid(catalog_id):
            raise ValueError("Catalog ID is not a correct UUID: {}".format(catalog_id))
        else:
            pass

        # request URL
        url_cat_delete = utils.get_request_base_url(
            route="groups/{}/catalogs/{}".format(workgroup_id, catalog_id)
        )

        cat_deletion = self.delete(url_cat_delete)

        return cat_deletion

    def catalog_exists(self, catalog_id: str) -> bool:
        """Check if the specified catalog exists and is available for the authenticated user.

        :param str catalog_id: identifier of the catalog to verify
        """
        url_cat_check = "{}{}".format(
            utils.get_request_base_url("catalogs"), catalog_id
        )

        return checker.check_api_response(self.get(url_cat_check))

    def catalog_update(self, workgroup_id: str, catalog: Catalog) -> dict:
        """Update a catalog into a workgroup address-book.

        :param str workgroup_id: identifier of the owner workgroup
        :param class catalog: Catalog model object to update
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # check catalog UUID
        if not checker.check_is_uuid(catalog._id):
            raise ValueError("Catalog ID is not a correct UUID: {}".format(catalog._id))
        else:
            pass

        # request route
        url_cat_update = utils.get_request_base_url(
            route="groups/{}/catalogs/{}".format(workgroup_id, catalog._id)
        )

        # request
        cat_update = self.put(
            url=url_cat_update,
            data=catalog.to_dict(),
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # handle bad JSON attribute
        catalog = cat_update.json()
        catalog["scan"] = catalog.pop("$scan")

        return catalog

    # -- CONTACTS --------------------------------------------------
    def contact(self, contact_id: str, include: list = ["count"]) -> dict:
        """Get a contact.

        :param str contact_id: contact UUID to get
        """
        # handle include
        include = checker._check_filter_includes(include, "contact")
        # handling request parameters
        payload = {"_include": include}

        # contact  search
        contact_url = "{}{}".format(
            utils.get_request_base_url(route="contacts"), contact_id
        )

        resource_req = self.get(
            contact_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )
        checker.check_api_response(resource_req)

        # end of method
        return resource_req.json()

    def contact_create(
        self, workgroup_id: str, check_exists: int = 1, contact: object = Contact()
    ) -> dict:
        """Add a new contact to a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param int check_exists: check if a contact already exists inot the workgroup:

        - 0 = no check
        - 1 = compare name [DEFAULT]
        - 2 = compare email

        :param class contact: Contact model object to create
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # check if contact already exists in workgroup
        if check_exists == 1:
            # retrieve workgroup contacts
            if not self._wg_cts_names:
                self.workgroup_contacts(workgroup_id=workgroup_id, include=[])
            # check
            if contact.name in self._wg_cts_names:
                logging.debug(
                    "Contact with the same name already exists: {}. Use 'contact_update' instead.".format(
                        contact.name
                    )
                )
                return False
        elif check_exists == 2:
            # retrieve workgroup contacts
            if not self._wg_cts_emails:
                self.workgroup_contacts(workgroup_id=workgroup_id, include=[])
            # check
            if contact.email in self._wg_cts_emails:
                logging.debug(
                    "Contact with the same email already exists: {}. Use 'contact_update' instead.".format(
                        contact.email
                    )
                )
                return False

        # build request url
        url_ct_create = utils.get_request_base_url(
            route="groups/{}/contacts".format(workgroup_id)
        )

        new_ct = self.post(
            url_ct_create,
            data=contact.to_dict_creation(),
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        return new_ct.json()

    def contact_delete(self, workgroup_id: str, contact_id: str) -> dict:
        """Delete a contact from Isogeo database.

        :param str workgroup_id: identifier of the owner workgroup
        :param str contact_id: identifier of the resource to delete
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # check contact UUID
        if not checker.check_is_uuid(contact_id):
            raise ValueError("Contact ID is not a correct UUID: {}".format(contact_id))
        else:
            pass

        # request URL
        url_ct_delete = utils.get_request_base_url(
            route="groups/{}/contacts/{}".format(workgroup_id, contact_id)
        )

        ct_deletion = self.delete(url_ct_delete)

        return ct_deletion

    def contact_exists(self, contact_id: str) -> bool:
        """Check if the specified contact exists and is available for the authenticated user.

        :param str contact_id: identifier of the contact to verify
        """
        url_ct_check = "{}{}".format(utils.get_request_base_url("contacts"), contact_id)

        return checker.check_api_response(self.get(url_ct_check))

    def contact_update(self, workgroup_id: str, contact: object) -> dict:
        """Update a contact into a workgroup address-book.

        :param str workgroup_id: identifier of the owner workgroup
        :param class contact: Contact model object to update
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # check contact UUID
        if not checker.check_is_uuid(contact._id):
            raise ValueError("Contact ID is not a correct UUID: {}".format(contact._id))
        else:
            pass

        # request URL
        url_ct_update = utils.get_request_base_url(
            route="groups/{}/contacts/{}".format(workgroup_id, contact._id)
        )

        ct_update = self.put(
            url=url_ct_update,
            data=contact.to_dict_creation(),
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        return ct_update.json()

    # -- KEYWORDS -----------------------------------------------------------
    def thesauri(self) -> dict:
        """Get available thesauri.
        """
        # request URL
        url_thesauri = utils.get_request_base_url(route="thesauri")

        # request
        thez_req = self.get(
            url_thesauri,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # checking response
        checker.check_api_response(thez_req)

        # end of method
        return thez_req.json()

    def thesaurus(self, thez_id: str = "1616597fbc4348c8b11ef9d59cf594c8") -> dict:
        """Get a thesaurus.

        :param str thez_id: thesaurus UUID
        """
        # handling request parameters
        payload = {"tid": thez_id}

        # request url
        url_thesaurus = utils.get_request_base_url(route="thesauri/{}".format(thez_id))

        # request
        thez_req = self.get(
            url_thesaurus,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # checking response
        checker.check_api_response(thez_req)

        # end of method
        return thez_req.json()

    def keywords(
        self,
        thez_id: str = "1616597fbc4348c8b11ef9d59cf594c8",
        query: str = "",
        offset: int = 0,
        order_by: str = "text",  # available values : count.group, count.isogeo, text
        order_dir: str = "desc",
        page_size: int = 20,
        specific_md: list = [],
        specific_tag: list = [],
        include: list = [],
    ) -> dict:
        """Search for keywords within a specific thesaurus.

        :param str thez_id: thesaurus UUID
        :param str query: search terms, equivalent of **q** parameter in API.
        :param int offset: offset to start page size from a specific results index
        :param str order_by: sorting results. Available values:

          * 'count.group': metadata creation date [DEFAULT if relevance is null]
          * 'count.isogeo': metadata last update
          * 'text': alphabetical order

        :param str order_dir: sorting direction. Available values:

          * 'desc': descending [DEFAULT]
          * 'asc': ascending

        :param int page_size: limits the number of results. Default: 20.
        :param list specific_md: list of metadata UUIDs to filter on
        :param list specific_tag: list of tags UUIDs to filter on
        :param list include: subresources that should be returned. Available values:

          * '_abilities'
          * 'count'
          * 'thesaurus'

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

        # keywords route
        url_keywords = utils.get_request_base_url(
            route="thesauri/{}/keywords/search".format(thez_id)
        )

        # request
        kwds_req = self.get(
            url=url_keywords,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # checking response
        checker.check_api_response(kwds_req)

        # end of method
        return kwds_req.json()

    # -- LICENCES ---------------------------------------------
    def licenses(self, workgroup_id: str = None, include: list = ["count"]) -> dict:
        """Get information about licenses owned by a specific workgroup.

        :param str workgroup_id: workgroup UUID
        """
        # handling request parameters
        payload = {"_include": include}

        # request URL
        url_licenses = utils.get_request_base_url(
            route="groups/{}/licenses".format(workgroup_id)
        )

        # request
        licenses_req = self.get(
            url_licenses,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # checking response
        req_check = checker.check_api_response(licenses_req)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return licenses_req.json()

    def license(self, license_id: str) -> dict:
        """Get details about a specific license.

        :param str license_id: license UUID
        """
        # handling request parameters
        payload = {"lid": license_id}

        # lciense route
        url_license = utils.get_request_base_url(route="licenses/{}".format(license_id))

        # request
        license_req = self.get(
            url_license,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # checking response
        checker.check_api_response(license_req)

        # end of method
        return license_req.json()

    # -- SPECIFICATIONS --------------------------------------------------
    def specification(self, specification_id: str, include: list = ["count"]) -> dict:
        """Get a specification.

        :param str specification_id: specification UUID to get
        """
        # handle include
        # include = checker._check_filter_includes(include, "specification")

        # handling request parameters
        payload = {"_include": include}

        # specification route
        specification_url = "{}{}".format(
            utils.get_request_base_url(route="specifications"), specification_id
        )

        # request
        specification_req = self.get(
            specification_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )
        checker.check_api_response(specification_req)

        # end of method
        return specification_req.json()

    # -- EVENTS --------------------------------------------------
    def event(self, metadata_id: str, event_id: str) -> dict:
        """Get an event.

        :param str event_id: event UUID to get
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # check contact UUID
        if not checker.check_is_uuid(event_id):
            raise ValueError("Event ID is not a correct UUID: {}".format(event_id))
        else:
            pass

        # request URL
        url_event = utils.get_request_base_url(
            route="resources/{}/events/{}".format(metadata_id, event_id)
        )

        event_req = self.get(
            url_event,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        checker.check_api_response(event_req)

        # add parent resource id to keep tracking
        event_augmented = event_req.json()
        event_augmented["parent_resource"] = metadata_id

        # end of method
        return event_augmented

    # -- LINKS --------------------------------------------------
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
    def workgroup(
        self, workgroup_id: str, include: list = ["_abilities", "limits"]
    ) -> dict:
        """Get an workgroup.

        :param str workgroup_id: workgroup UUID to get
        """
        # check UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # handle include
        # include = checker._check_filter_includes(include, "workgroup")
        # handling request parameters
        payload = {"_include": include}

        # request URL
        url_workgroup = utils.get_request_base_url(
            route="/groups/{}".format(workgroup_id)
        )

        workgroup_req = self.get(
            url_workgroup,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        checker.check_api_response(workgroup_req)

        # end of method
        return workgroup_req.json()

    def workgroup_create(
        self, workgroup: Workgroup, check_exists: int = 1
    ) -> dict:
        """Add a new workgroup to Isogeo.

        :param class workgroup: Workgroup object to create.
        :param int check_exists: check if a workgroup already exists into Isogeo:

        - 0 = no check
        - 1 = compare name [DEFAULT]
        - 2 = compare email
        """
        # check if workgroup already exists in workgroup
        if check_exists == 1:
            logging.debug(NotImplemented)
        #     # retrieve workgroup workgroups
        #     if not self._wg_cts_names:
        #         self.workgroup_workgroups(workgroup_id=workgroup_id, include=[])
        #     # check
        #     if workgroup.name in self._wg_cts_names:
        #         logging.debug(
        #             "Workgroup with the same name already exists: {}. Use 'workgroup_update' instead.".format(
        #                 workgroup.name
        #             )
        #         )
        #         return False
        # elif check_exists == 2:
        #     # retrieve workgroup workgroups
        #     if not self._wg_cts_emails:
        #         self.workgroup_workgroups(workgroup_id=workgroup_id, include=[])
        #     # check
        #     if workgroup.email in self._wg_cts_emails:
        #         logging.debug(
        #             "Workgroup with the same email already exists: {}. Use 'workgroup_update' instead.".format(
        #                 workgroup.email
        #             )
        #         )
        #         return False

        # build request url
        url_wg_create = utils.get_request_base_url(route="groups")

        # request
        new_wg = self.post(
            url_wg_create,
            data=workgroup.to_dict_creation(),
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        return Workgroup(**new_wg.json())

    def workgroup_delete(self, workgroup_id: str) -> dict:
        """Delete a workgroup from Isogeo database.

        :param str workgroup_id: identifier of the workgroup
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # request URL
        url_wg_delete = utils.get_request_base_url(
            route="groups/{}".format(workgroup_id)
        )

        wg_deletion = self.delete(url_wg_delete)

        return wg_deletion

    @_check_bearer_validity
    def workgroup_catalogs(
        self, workgroup_id: str, include: list = ["count"], caching: bool = 1
    ) -> dict:
        """List workgroup catalogs.

        :param str workgroup_id: identifier of the owner workgroup
        :param list include: identifier of the owner workgroup
        :param bool caching: option to cache the response
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        payload = {"_include": include}

        # handle include
        # include = checker._check_filter_includes(include, "catalog")

        # build request url
        url_ct_list = utils.get_request_base_url(
            route="groups/{}/catalogs".format(workgroup_id)
        )

        wg_catalogs = self.get(
            url_ct_list,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        wg_catalogs = wg_catalogs.json()

        # handle bad JSON attribute (invalid character)
        for i in wg_catalogs:
            i["scan"] = i.pop("$scan")

        # if caching use or store the workgroup catalogs
        if caching and not self._wg_cats_names:
            self._wg_cats_names = {i.get("name"): i.get("_id") for i in wg_catalogs}

        return wg_catalogs

    def workgroup_contacts(
        self, workgroup_id: str, include: list = ["count"], caching: bool = 1
    ) -> dict:
        """List workgroup contacts.

        :param str workgroup_id: identifier of the owner workgroup
        :param list include: identifier of the owner workgroup
        :param bool caching: option to cache the response
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass


        # handle include
        include = checker._check_filter_includes(include, "contact")
        payload = {"_include": include}

        # build request url
        url_ct_list = utils.get_request_base_url(
            route="groups/{}/contacts".format(workgroup_id)
        )

        wg_contacts = self.get(
            url_ct_list,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        wg_contacts = wg_contacts.json()

        # if caching use or store the workgroup contacts
        if caching and not self._wg_cts_emails and not self._wg_cts_names:
            for i in wg_contacts:
                self._wg_cts_emails[i.get("email")] = i.get("_id")
                self._wg_cts_names[i.get("name")] = i.get("_id")

        return wg_contacts

    def workgroup_stats(self, workgroup_id: str) -> dict:
        """Returns statistics for the specified workgroup.

        :param str workgroup_id: workgroup UUID to get
        """
        # check contact UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # request URL
        url_workgroup = utils.get_request_base_url(
            route="/groups/{}/statistics".format(workgroup_id)
        )

        workgroup_req = self.get(
            url_workgroup,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        checker.check_api_response(workgroup_req)

        # end of method
        return workgroup_req.json()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    # ------------ Specific imports ----------------
    from dotenv import load_dotenv
    from os import environ
    import pprint
    from time import sleep

    # ------------ Log & debug ----------------
    logger = logging.getLogger()
    logging.captureWarnings(True)
    logger.setLevel(logging.DEBUG)

    # ------------ Real start ----------------
    # load application credentials from downloaded file
    credentials = utils.credentials_loader("client_secrets_scripts.json")

    # get user ID as environment variables
    load_dotenv("dev.env")

    # instanciate
    isogeo = IsogeoSession(
        client=LegacyApplicationClient(client_id=credentials.get("client_id")),
        auto_refresh_url="https://id.api.isogeo.com/oauth/token",
        client_secret=credentials.get("client_secret"),
    )

    # getting a token
    token = isogeo.connect(
        username=environ.get("ISOGEO_USER_NAME"),
        password=environ.get("ISOGEO_USER_PASSWORD"),
    )

    # # licenses
    # lics = isogeo.licenses(owner_id="32f7e95ec4e94ca3bc1afda960003882")
    # print(lics)

    # # memo : par défaut order_dir = asc
    # k = isogeo.keywords(thez_id="1616597fbc4348c8b11ef9d59cf594c8",
    #                     order_by="count.isogeo",
    #                     order_dir="desc",
    #                     page_size=10,
    #                     include="all"
    #                     )
    # print(k)

    # md = isogeo.md_create(
    #     workgroup_id=WORKGROUP_UUID,
    #     resource_type="vectorDataset",
    #     title="Salut Simon",
    #     abstract="meuh",
    #     series=0
    # )

    # print(md)
    # print(md.get("_id"))

    # sleep(10)    # ensure that metadata has been created

    # deleted = isogeo.md_delete(resource_id="cd44a3cbabd347a2aba428d95b055697")
    # print(deleted)

    # md_ok = isogeo.md_exists("7d3f238a3aad411eb9fc9fca1da76bb3")
    # print(md_ok)

    # md = isogeo.resource(id_resource="196831cb153e4f30a220ae21512bcb5e")
    # pprint.pprint(md)

    ct = isogeo.contact(id_contact="49b248a4985041aebee7d5d6c337d82f")
    # pprint.pprint(ct)

    print(ct.get("_id"))
    t = Contact(**ct)
    # print(dir(t))

    # print(t._id)
    # print(t.to_dict())
    print(t.to_str())
