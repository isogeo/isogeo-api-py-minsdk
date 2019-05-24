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
        self, keyword_id: str, include: list = ["_abilities", "count", "thesaurus"]
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

    @ApiDecorators._check_bearer_validity
    def create(self, keyword: Keyword) -> Keyword:
        """Add a new keyword to the Isogeo thesaurus.

        If a keyword with the same text already exists, the Isogeo API returns a 409 HTTP code.
        Then this method will try to get the closest matching keyword and return it.

        :param Keyword keyword: Keyword model object to create
        """
        # URL
        url_keyword_create = utils.get_request_base_url(
            route="thesauri/1616597fbc4348c8b11ef9d59cf594c8/keywords"
        )

        # request
        req_new_keyword = self.api_client.post(
            url=url_keyword_create,
            json=keyword.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_new_keyword)
        if isinstance(req_check, tuple):
            # handle conflict (see: https://developer.mozilla.org/fr/docs/Web/HTTP/Status/409)
            if req_check[1] == 409:
                # log conflict
                logger.info(
                    "A keyword with the same text already exists: '{}'. Isogeo API doesn't allow to create duplicates (HTTP {} - {}). Let's try to get the closes matching keyword...".format(
                        keyword.text, req_check[1], req_new_keyword.reason
                    )
                )
                # try to return the most probably matching keyword
                search_for_closest_keyword = self.thesaurus(
                    caching=0,
                    include=[],
                    order_dir="asc",
                    page_size=1,
                    query=keyword.text,
                )
                if search_for_closest_keyword.results:
                    logger.info(
                        "Returning the closest matching keyword for: 'thesauri/keywords/search?query={}'".format(
                            keyword.text
                        )
                    )
                    return Keyword(**search_for_closest_keyword.results[0])
                else:
                    logger.info(
                        "No match for: 'thesauri/keywords/search?query={}'".format(
                            keyword.text
                        )
                    )

            # if other error, then return it
            return req_check

        # end of method
        return Keyword(**req_new_keyword.json())

    @ApiDecorators._check_bearer_validity
    def delete(self, keyword: Keyword):
        """Delete a keyword from Isogeo database.

        :param Keyword keyword: Keyword model object to create
        """
        # check keyword UUID
        if not checker.check_is_uuid(keyword._id):
            raise ValueError("Keyword ID is not a correct UUID: {}".format(keyword._id))
        else:
            pass

        # URL
        url_keyword_delete = utils.get_request_base_url(
            route="thesauri/1616597fbc4348c8b11ef9d59cf594c8/keywords/{}".format(
                keyword._id
            )
        )

        # request
        req_keyword_deletion = self.api_client.delete(
            url=url_keyword_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_keyword_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_keyword_deletion


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_keyword = ApiKeyword()
