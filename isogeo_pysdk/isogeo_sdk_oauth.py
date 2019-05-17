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
from isogeo_pysdk.models import (
    Application,
    Catalog,
    Contact,
    Event,
    License,
    Link,
    Metadata,
    Specification,
    Thesaurus,
    User,
    Workgroup,
)
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

        # caching
        self._applications_names = {}  # workgroup applications by names
        self._user = {}  # authenticated user profile
        self._wg_contacts_emails = {}  # workgroup contacts by emails
        self._wg_contacts_names = {}  # workgroup contacts by names
        self._wg_catalogs_names = {}  # workgroup catalogs by names
        self._wg_licenses_names = {}  # workgroup licenses by names
        self._wg_specifications_names = {}  # workgroup specifications by names

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

        # setting locale according to the language passed
        try:
            if opersys == "win32":
                if lang.lower() == "fr":
                    locale.setlocale(locale.LC_ALL, str("fra_fra"))
                else:
                    locale.setlocale(locale.LC_ALL, str("uk_UK"))
            else:
                if lang.lower() == "fr":
                    locale.setlocale(locale.LC_ALL, str("fr_FR.utf8"))
                else:
                    locale.setlocale(locale.LC_ALL, str("en_GB.utf8"))
        except locale.Error as e:
            logging.error(
                "Selected locale ({}) is not installed: {}".format(lang.lower(), e)
            )

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

        # load routes as subclass
        self.api = api
        self.account = api.ApiAccount(self)
        self.application = api.ApiApplication(self)
        self.catalog = api.ApiCatalog(self)
        self.contact = api.ApiContact(self)
        self.license = api.ApiLicense(self)
        # self.api.metadata = self.api.ApiResource(self)
        self.specification = api.ApiSpecification(self)

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
                logging.debug("Token was about to expire, so has been renewed.")
            else:
                logging.debug("Token is still valid.")
                pass

            # let continue running the original function
            return decorated_func(self, *args, **kwargs)

        return wrapper

    # -- METADATA = RESOURCE --------------------------------------------------
    @_check_bearer_validity
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
            hooks={
                "response": [
                    self.custom_hooks.check_for_error,
                    # self.custom_hooks.autofix_attributes_resource,
                ]
            },
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # handle bad JSON attribute
        metadata = resource_req.json()
        metadata["coordinateSystem"] = metadata.pop("coordinate-system", list)
        metadata["featureAttributes"] = metadata.pop("feature-attributes", list)

        # end of method
        return metadata

    @_check_bearer_validity
    def md_exists(self, resource_id: str) -> bool:
        """Check if the specified metadata exists or is available for the authenticated user.

        :param str resource_id: identifier of the resource to verify
        """
        url_md_check = "{}{}".format(
            utils.get_request_base_url("resources"), resource_id
        )

        return checker.check_api_response(self.get(url_md_check))

    @_check_bearer_validity
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

    @_check_bearer_validity
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

    @_check_bearer_validity
    def md_update(self, metadata: Metadata) -> Metadata:
        """Update a metadata from Isogeo database.

        :param Metadata metadata: metadata (resource) to edit
        """
        # check metadata UUID
        # if not checker.check_is_uuid(workgroup_id):
        #     raise ValueError("Workgroup ID is not a correct UUID.")
        # else:
        #     pass

        # URL
        url_metadata_update = utils.get_request_base_url(
            route="resources/{}".format(metadata._id)
        )

        # request
        req_metadata_update = self.patch(
            url=url_metadata_update,
            json=metadata.to_dict_creation(),
            headers=self.header,
            proxies=self.proxies,
            timeout=self.timeout,
            verify=self.ssl,
        )

        # method ending
        return Metadata(**req_metadata_update.json())

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

    @_check_bearer_validity
    def md_associate_events(
        self,
        metadata: Metadata,
        event_date: str or datetime,
        event_comment: str = None,
        event_kind: str = "update",
    ) -> dict:
        """Associate an event to a metadata.

        :param Metadata metadata: metadata (resource) to edit
        :param str event_date: date of the event. Must be in the format `YYYY-MM-DD`
        :param str event_kind: kind of event. Must be one of: creation, update, publication
        :param str event_comment: text to associate to the event. Not possible for event_kind=='creation'
        """
        # check params
        if event_kind not in ("creation", "update", "publication"):
            raise ValueError(
                "'event_kind' must be one of: creation, update, publication"
            )

        if isinstance(event_date, str):
            datetime.strptime(event_date, "%Y-%m-%d")
        elif isinstance(event_date, datetime):
            event_date = event_date.strftime("%Y-%m-%d")
        else:
            raise TypeError("'event_date' must be a str or a datetime")

        # ensure that a creation date doesn't already exist
        if event_kind == "creation":
            # retrieve metadata events
            metadata_events = self.resource(metadata._id, include=["events"])
            # filter on creation events
            events_creation = list(
                filter(
                    lambda d: d["kind"] in ["creation"], metadata_events.get("events")
                )
            )
            if events_creation:
                logger.warning(
                    "A creation event already exist. A metadata can only have one creation event. Use event_update instead."
                )
                return self.event(metadata._id, events_creation[0].get("_id"))

        # ensure removing event_comment for creation dates
        if event_kind == "creation" and event_comment:
            event_comment = None
            logger.warning("Event comments are not allowed for creation dates")

        # URL
        url_metadata_asso_event = utils.get_request_base_url(
            route="resources/{}/events/".format(metadata._id)
        )

        # request
        req_metadata_asso_event = self.post(
            url=url_metadata_asso_event,
            json={"date": event_date, "description": event_comment, "kind": event_kind},
            headers=self.header,
            proxies=self.proxies,
            timeout=self.timeout,
            verify=self.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_asso_event)
        if isinstance(req_check, tuple):
            return req_check

        # method ending
        return req_metadata_asso_event.json()

    @_check_bearer_validity
    def md_remove_events(self, metadata: Metadata, event_id: str) -> dict:
        """Associate an event to a metadata.

        :param Metadata metadata: metadata (resource) to edit
        :param str event_id: UUID of the event to remove
        """
        # check event UUID
        if not checker.check_is_uuid(event_id):
            raise ValueError("Event ID is not a correct UUID.")
        else:
            pass
        # URL
        url_metadata_del_event = utils.get_request_base_url(
            route="resources/{}/events/{}".format(metadata._id, event_id)
        )

        # request
        req_metadata_del_event = self.delete(
            url=url_metadata_del_event,
            headers=self.header,
            proxies=self.proxies,
            timeout=self.timeout,
            verify=self.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_del_event)
        if isinstance(req_check, tuple):
            return req_check

        # method ending
        return req_metadata_del_event

    # -- KEYWORDS -----------------------------------------------------------
    @_check_bearer_validity
    def thesauri(self, include: list = ["_abilities"]) -> list:
        """Get available thesauri.
        """
        # handling request parameters
        payload = {"_include": include}

        # request URL
        url_thesauri = utils.get_request_base_url(route="thesauri")

        # request
        req_thesauri = self.get(
            url_thesauri,
            params=payload,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_thesauri)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_thesauri.json()

    @_check_bearer_validity
    def thesaurus(
        self,
        thez_id: str = "1616597fbc4348c8b11ef9d59cf594c8",
        include: list = ["_abilities"],
    ) -> Thesaurus:
        """Get a thesaurus.

        :param str thez_id: thesaurus UUID
        """
        # handling request parameters
        payload = {"_include": include}

        # request url
        url_thesaurus = utils.get_request_base_url(route="thesauri/{}".format(thez_id))

        # request
        req_thesaurus = self.get(
            url_thesaurus,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_thesaurus)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return Thesaurus(**req_thesaurus.json())

    @_check_bearer_validity
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

    # -- EVENTS --------------------------------------------------
    @_check_bearer_validity
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

    @_check_bearer_validity
    def workgroup_create(
        self, workgroup: Workgroup, check_exists: int = 1
    ) -> Workgroup:
        """Add a new workgroup to Isogeo.

        :param class workgroup: Workgroup object to create.
        :param int check_exists: check if a workgroup already exists into Isogeo:

        - 0 = no check
        - 1 = compare name [DEFAULT]
        - 2 = compare email
        """
        # check if object has a correct contact
        if not hasattr(workgroup, "contact") or not isinstance(
            workgroup.contact, Contact
        ):
            logging.debug("MMMMM bad workgroup")

        # check if workgroup already exists in workgroup
        if check_exists == 1:
            logging.debug(NotImplemented)
        #     # retrieve workgroup workgroups
        #     if not self._wg_contacts_names:
        #         self.workgroup_workgroups(workgroup_id=workgroup_id, include=[])
        #     # check
        #     if workgroup.name in self._wg_contacts_names:
        #         logging.debug(
        #             "Workgroup with the same name already exists: {}. Use 'workgroup_update' instead.".format(
        #                 workgroup.name
        #             )
        #         )
        #         return False
        # elif check_exists == 2:
        #     # retrieve workgroup workgroups
        #     if not self._wg_contacts_emails:
        #         self.workgroup_workgroups(workgroup_id=workgroup_id, include=[])
        #     # check
        #     if workgroup.email in self._wg_contacts_emails:
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

    @_check_bearer_validity
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
    def workgroup_applications(self, workgroup_id: str, caching: bool = 1) -> dict:
        """List workgroup applications.

        :param str workgroup_id: identifier of the owner workgroup
        :param bool caching: option to cache the response
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # build request url
        url_app_list = utils.get_request_base_url(
            route="groups/{}/applications".format(workgroup_id)
        )

        wg_applications = self.get(
            url_app_list, proxies=self.proxies, verify=self.ssl, timeout=self.timeout
        )

        wg_applications = wg_applications.json()

        # if caching use or store the workgroup applications
        if caching and not self._wg_apps_names:
            self._wg_apps_names = {i.get("name"): i.get("_id") for i in wg_applications}

        return wg_applications

    @_check_bearer_validity
    def workgroup_keywords(
        self, workgroup_id: str, include: list = ["count"], caching: bool = 1
    ) -> list:
        """List workgroup keywords.

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
        # include = checker._check_filter_includes(include, "keyword")

        # build request url
        url_ct_list = utils.get_request_base_url(
            route="groups/{}/keywords/search".format(workgroup_id)
        )

        # request
        req_wg_keywords = self.get(
            url_ct_list,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
            timeout=self.timeout,
        )

        # check response
        req_check = checker.check_api_response(req_wg_keywords)
        if isinstance(req_check, tuple):
            return req_check
        wg_keywords = req_wg_keywords.json()

        return wg_keywords

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

    @_check_bearer_validity
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
        client=LegacyApplicationClient(client_id=credentials.get("client_id")),
        auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
        client_secret=credentials.get("client_secret"),
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
