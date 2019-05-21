# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Keywords entities

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import Keyword, KeywordSearch
from isogeo_pysdk.utils import IsogeoUtils

# #############################################################################
# ########## Global #############
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiKeyword:
    """Routes as methods of Isogeo API used to manipulate keywords (conditions).
    """

    def __init__(self, api_client=None):
        if api_client is not None:
            self.api_client = api_client

        # store API client (Request [Oauthlib] Session) and pass it to the decorators
        self.api_client = api_client
        ApiDecorators.api_client = api_client

        # ensure platform and others params to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            self.api_client.platform
        )
        # initialize
        super(ApiKeyword, self).__init__()

    @ApiDecorators._check_bearer_validity
    def thesaurus(
        self,
        thesaurus_id: str = "1616597fbc4348c8b11ef9d59cf594c8",
        query: str = "",
        offset: int = 0,
        order_by: str = "text",  # available values : count.group, count.isogeo, text
        order_dir: str = "desc",
        page_size: int = 20,
        specific_md: list = [],
        specific_tag: list = [],
        include: list = ["_abilities", "count"],
        caching: bool = 1,
    ) -> KeywordSearch:
        """Search for keywords within a specific thesaurus or a specific group.

        :param str thesaurus_id: thesaurus UUID
        :param str query: search terms, equivalent of **q** parameter in API.
        :param int offset: offset to start page size from a specific results index
        :param str order_by: sorting results. Available values:

          * 'count.isogeo': count of associated resources within Isogeo
          * 'text': alphabetical order  [DEFAULT if relevance is null]

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
            "ob": order_by,
            "od": order_dir,
            "q": query,
        }

        # URL
        url_thesauri_keywords = utils.get_request_base_url(
            route="thesauri/{}/keywords/search".format(thesaurus_id)
        )

        # request
        req_thesaurus_keywords = self.api_client.get(
            url=url_thesauri_keywords,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_thesaurus_keywords)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return KeywordSearch(**req_thesaurus_keywords.json())

    @ApiDecorators._check_bearer_validity
    def workgroup(
        self,
        workgroup_id: str = None,
        thesaurus_id: str = None,
        query: str = "",
        offset: int = 0,
        order_by: str = "text",  # available values : count.group, count.isogeo, text
        order_dir: str = "desc",
        page_size: int = 20,
        specific_md: list = [],
        specific_tag: list = [],
        include: list = ["_abilities", "count", "thesaurus"],
        caching: bool = 1,
    ) -> KeywordSearch:
        """Search for keywords within a specific group's used thesauri

        :param str thesaurus_id: thesaurus UUID to filter on
        :param str query: search terms, equivalent of **q** parameter in API.
        :param int offset: offset to start page size from a specific results index
        :param str order_by: sorting results. Available values:

          * 'count.group': count of associated resources within the specified group
          * 'count.isogeo': count of associated resources within Isogeo
          * 'text': alphabetical order  [DEFAULT]

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
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

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
            "tid": thesaurus_id,
            "ob": order_by,
            "od": order_dir,
            "q": query,
        }

        # URL
        url_workgroup_keywords = utils.get_request_base_url(
            route="groups/{}/keywords/search".format(workgroup_id)
        )

        # request
        req_thesaurus_keywords = self.api_client.get(
            url=url_workgroup_keywords,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_thesaurus_keywords)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return KeywordSearch(**req_thesaurus_keywords.json())

    @ApiDecorators._check_bearer_validity
    def keyword(
        self,
        # workgroup_id: str,
        keyword_id: str,
        include: list = ["_abilities", "count", "thesaurus"],
    ) -> Keyword:
        """Get details about a specific keyword.

        :param str workgroup_id: identifier of the owner workgroup
        :param str keyword_id: keyword UUID
        :param list include: additionnal subresource to include in the response
        """
        # check workgroup UUID
        # if not checker.check_is_uuid(workgroup_id):
        #     raise ValueError(
        #         "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
        #     )
        # else:
        #     pass

        # check keyword UUID
        if not checker.check_is_uuid(keyword_id):
            raise ValueError("Keyword ID is not a correct UUID.")
        else:
            pass

        # request parameter
        payload = {"_include": include}

        # keyword route
        url_keyword = utils.get_request_base_url(route="keywords/{}".format(keyword_id))

        # request
        req_keyword = self.api_client.get(
            url=url_keyword,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_keyword)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return Keyword(**req_keyword.json())

    # @ApiDecorators._check_bearer_validity
    # def keyword_create(
    #     self, workgroup_id: str, check_exists: int = 1, keyword: object = Keyword()
    # ) -> Keyword:
    #     """Add a new keyword to a workgroup.

    #     :param str workgroup_id: identifier of the owner workgroup
    #     :param int check_exists: check if a keyword already exists inot the workgroup:

    #     - 0 = no check
    #     - 1 = compare name [DEFAULT]

    #     :param class keyword: Keyword model object to create
    #     """
    #     # check workgroup UUID
    #     if not checker.check_is_uuid(workgroup_id):
    #         raise ValueError("Workgroup ID is not a correct UUID.")
    #     else:
    #         pass

    #     # check if keyword already exists in workgroup
    #     if check_exists == 1:
    #         # retrieve workgroup keywords
    #         if not self.api_client._wg_keywords_names:
    #             self.keywords(workgroup_id=workgroup_id, include=[])
    #         # check
    #         if keyword.name in self.api_client._wg_keywords_names:
    #             logger.debug(
    #                 "Keyword with the same name already exists: {}. Use 'keyword_update' instead.".format(
    #                     keyword.name
    #                 )
    #             )
    #             return False
    #     else:
    #         pass

    #     # build request url
    #     url_keyword_create = utils.get_request_base_url(
    #         route="groups/{}/keywords".format(workgroup_id)
    #     )

    #     # request
    #     req_new_keyword = self.api_client.post(
    #         url_keyword_create,
    #         data=keyword.to_dict_creation(),
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_new_keyword)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     # handle bad JSON attribute
    #     new_keyword = req_new_keyword.json()
    #     new_keyword["scan"] = new_keyword.pop("$scan")

    #     # load new keyword and save it to the cache
    #     new_keyword = Keyword(**new_keyword)
    #     self.api_client._wg_keywords_names[new_keyword.name] = new_keyword._id

    #     # end of method
    #     return new_keyword

    # @ApiDecorators._check_bearer_validity
    # def keyword_delete(self, workgroup_id: str, keyword_id: str):
    #     """Delete a keyword from Isogeo database.

    #     :param str workgroup_id: identifier of the owner workgroup
    #     :param str keyword_id: identifier of the resource to delete
    #     """
    #     # check workgroup UUID
    #     if not checker.check_is_uuid(workgroup_id):
    #         raise ValueError(
    #             "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
    #         )
    #     else:
    #         pass

    #     # check keyword UUID
    #     if not checker.check_is_uuid(keyword_id):
    #         raise ValueError("Keyword ID is not a correct UUID: {}".format(keyword_id))
    #     else:
    #         pass

    #     # request URL
    #     url_keyword_delete = utils.get_request_base_url(
    #         route="groups/{}/keywords/{}".format(workgroup_id, keyword_id)
    #     )

    #     # request
    #     req_keyword_deletion = self.api_client.delete(
    #         url_keyword_delete,
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_keyword_deletion)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     return req_keyword_deletion

    # @ApiDecorators._check_bearer_validity
    # def keyword_exists(self, workgroup_id: str, keyword_id: str) -> bool:
    #     """Check if the specified keyword exists and is available for the authenticated user.

    #     :param str workgroup_id: identifier of the owner workgroup
    #     :param str keyword_id: identifier of the keyword to verify
    #     """
    #     # check workgroup UUID
    #     if not checker.check_is_uuid(workgroup_id):
    #         raise ValueError(
    #             "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
    #         )
    #     else:
    #         pass
    #     # check keyword UUID
    #     if not checker.check_is_uuid(keyword_id):
    #         raise ValueError("Keyword ID is not a correct UUID: {}".format(keyword_id))
    #     else:
    #         pass

    #     # URL builder
    #     url_keyword_exists = utils.get_request_base_url(
    #         route="groups/{}/keywords/{}".format(workgroup_id, keyword_id)
    #     )

    #     # request
    #     req_keyword_exists = self.api_client.get(
    #         url=url_keyword_exists,
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_keyword_exists)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     return req_keyword_exists

    # @ApiDecorators._check_bearer_validity
    # def keyword_update(self, keyword: Keyword, caching: bool = 1) -> Keyword:
    #     """Update a keyword owned by a workgroup.

    #     :param class keyword: Keyword model object to update
    #     :param bool caching: option to cache the response
    #     """
    #     # check keyword UUID
    #     if not checker.check_is_uuid(keyword._id):
    #         raise ValueError("Keyword ID is not a correct UUID: {}".format(keyword._id))
    #     else:
    #         pass

    #     # URL
    #     url_keyword_update = utils.get_request_base_url(
    #         route="groups/{}/keywords/{}".format(keyword.owner.get("_id"), keyword._id)
    #     )

    #     # request
    #     req_keyword_update = self.api_client.put(
    #         url=url_keyword_update,
    #         json=keyword.to_dict_creation(),
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_keyword_update)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     # handle bad JSON attribute
    #     new_keyword = req_keyword_update.json()
    #     new_keyword["scan"] = new_keyword.pop("$scan")

    #     # load new keyword and save it to the cache
    #     new_keyword = Keyword(**new_keyword)
    #     if caching:
    #         self.api_client._wg_keywords_names[new_keyword.name] = new_keyword._id

    #     # end of method
    #     return new_keyword


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_keyword = ApiKeyword()
