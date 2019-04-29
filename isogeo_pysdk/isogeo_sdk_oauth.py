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
    from . import checker
    from .models import Contact, Event, Link, Specification, Workgroup
    from . import utils
    from . import version
except (ImportError, ValueError, SystemError):
    import checker
    from models.contact import Contact
    from models.event import Event
    from models.link import Link
    from models.specification import Specification
    from models.workgroup import Workgroup
    import utils
    from isogeo_sdk import version

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

    # -- METADATA = RESOURCE --------------------------------------------------
    def resource(
        self,
        id_resource: str = None,
        subresource=None,
        include: list = [],
        prot: str = "https",
    ) -> dict:
        """Get complete or partial metadata about one specific resource.

        :param str id_resource: metadata UUID to get
        :param list include: subresources that should be included.
         Must be a list of strings. Available values: 'isogeo.SUBRESOURCES'
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # if subresource route
        if isinstance(subresource, str):
            subresource = "/{}".format(checker._check_subresource(subresource))
        else:
            subresource = ""
            # _includes specific parsing
            include = checker._check_filter_includes(include)

        # handling request parameters
        payload = {"id": id_resource, "_include": include}
        # resource search
        md_url = "{}{}{}".format(
            utils.get_request_base_url(route="resources"), id_resource, subresource
        )

        resource_req = self.get(
            md_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
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
        abstract: str,
        series: bool = 0,
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

        data = {
            "title": title,
            "abstract": abstract,
            "type": resource_type,
            "series": series,
        }

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

    # -- CONTACTS --------------------------------------------------
    def contact(
        self, id_contact: str, include: list = ["count"], prot: str = "https"
    ) -> dict:
        """Get a contact.

        :param str id_contact: contact UUID to get
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # handle include
        include = checker._check_filter_includes(include, "contact")
        # handling request parameters
        payload = {"_include": include}

        # contact  search
        contact_url = "{}{}".format(
            utils.get_request_base_url(route="contacts"), id_contact
        )

        resource_req = self.get(
            contact_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
        )
        checker.check_api_response(resource_req)

        # end of method
        return resource_req.json()

    def contact_create(
        self, workgroup_id: str, check_exists: int = 0, contact: object = Contact()
    ) -> dict:
        """Add a new contact to a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param int check_exists: check if a contact already exists inot the workgroup:

        - 0 = no check [DEFAULT]
        - 1 = compare name
        - 2 = compare email

        :param class contact: Contact model object to create
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # check if contact already exists in workgroup
        if check_exists:
            logging.debug(NotImplemented)

        # build request url
        url_ct_create = utils.get_request_base_url(
            route="groups/{}/contacts".format(workgroup_id)
        )

        new_ct = self.post(
            url_ct_create,
            data=contact.to_dict_creation(),
            proxies=self.proxies,
            verify=self.ssl,
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
        )

        return ct_update.json()

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

    def license(self, license_id: str, prot: str = "https") -> dict:
        """Get details about a specific license.

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

    # -- SPECIFICATIONS --------------------------------------------------
    def specification(
        self, id_specification: str, include: list = ["count"], prot: str = "https"
    ) -> dict:
        """Get a specification.

        :param str id_specification: specification UUID to get
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # handle include
        # include = checker._check_filter_includes(include, "specification")
        # handling request parameters
        payload = {"_include": include}

        # specification  search
        specification_url = "{}{}".format(
            utils.get_request_base_url(route="specifications"), id_specification
        )

        specification_req = self.get(
            specification_url,
            headers=self.header,
            params=payload,
            proxies=self.proxies,
            verify=self.ssl,
        )
        checker.check_api_response(specification_req)

        # end of method
        return specification_req.json()

    # -- EVENTS --------------------------------------------------
    def event(
        self, id_metadata: str, id_event: str, prot: str = "https"
    ) -> dict:
        """Get an event.

        :param str id_event: event UUID to get
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # check metadata UUID
        if not checker.check_is_uuid(id_metadata):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(id_metadata)
            )
        else:
            pass

        # check contact UUID
        if not checker.check_is_uuid(id_event):
            raise ValueError("Event ID is not a correct UUID: {}".format(id_event))
        else:
            pass

        # request URL
        url_event = utils.get_request_base_url(
            route="resources/{}/events/{}".format(id_metadata, id_event)
        )

        event_req = self.get(
            url_event,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
        )

        checker.check_api_response(event_req)

        # add parent resource id to keep tracking
        event_augmented = event_req.json()
        event_augmented["parent_resource"] = id_metadata

        # end of method
        return event_augmented

    # -- LINKS --------------------------------------------------
    def link(
        self, id_metadata: str, id_link: str, prot: str = "https"
    ) -> dict:
        """Get an link.

        :param str id_link: link UUID to get
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # check metadata UUID
        if not checker.check_is_uuid(id_metadata):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(id_metadata)
            )
        else:
            pass

        # check contact UUID
        if not checker.check_is_uuid(id_link):
            raise ValueError("Link ID is not a correct UUID: {}".format(id_link))
        else:
            pass

        # request URL
        url_link = utils.get_request_base_url(
            route="resources/{}/links/{}".format(id_metadata, id_link)
        )

        link_req = self.get(
            url_link,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
        )

        checker.check_api_response(link_req)

        # add parent resource id to keep tracking
        link_augmented = link_req.json()
        link_augmented["parent_resource"] = id_metadata

        # end of method
        return link_augmented

    # -- LINKS --------------------------------------------------
    def workgroup(
        self, id_workgroup: str, prot: str = "https"
    ) -> dict:
        """Get an workgroup.

        :param str id_workgroup: workgroup UUID to get
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # check contact UUID
        if not checker.check_is_uuid(id_workgroup):
            raise ValueError("Workgroup ID is not a correct UUID: {}".format(id_workgroup))
        else:
            pass

        # request URL
        url_workgroup = utils.get_request_base_url(
            route="/groups/{}".format(id_workgroup)
        )

        workgroup_req = self.get(
            url_workgroup,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
        )

        checker.check_api_response(workgroup_req)

        # end of method
        return workgroup_req.json()

    def workgroup_stats(
        self, id_workgroup: str, prot: str = "https"
    ) -> dict:
        """Retruns statistics for the specified workgroup.

        :param str id_workgroup: workgroup UUID to get
        :param str prot: https [DEFAULT] or http
         (use it only for dev and tracking needs).
        """
        # check contact UUID
        if not checker.check_is_uuid(id_workgroup):
            raise ValueError("Workgroup ID is not a correct UUID: {}".format(id_workgroup))
        else:
            pass

        # request URL
        url_workgroup = utils.get_request_base_url(
            route="/groups/{}/statistics".format(id_workgroup)
        )

        workgroup_req = self.get(
            url_workgroup,
            headers=self.header,
            proxies=self.proxies,
            verify=self.ssl,
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
