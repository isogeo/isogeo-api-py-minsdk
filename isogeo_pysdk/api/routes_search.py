# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Search

    See: http://help.isogeo.com/api/complete/index.html#definition-resource
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from functools import wraps
from urllib.parse import urlparse, parse_qs, urlunparse


# 3rd party
import requests
from requests.adapters import HTTPAdapter
from requests.models import Response

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import ResourceSearch
from isogeo_pysdk.utils import IsogeoUtils

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiSearch:
    """Routes as methods of Isogeo API used to manipulate metadatas (resources).
    """

    def __init__(self, api_client=None):
        if api_client is not None:
            self.api_client = api_client

        # store API client (Request [Oauthlib] Session) and pass it to the decorators
        self.api_client = api_client
        ApiDecorators.api_client = api_client

        # ensure platform to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            self.api_client.platform
        )

        # initialize
        super(ApiSearch, self).__init__()

    # -- Routes to search --------------------------------------------------------------
    @ApiDecorators._check_bearer_validity
    def search(
        self,
        # semantic and objects filters
        query: str = "",
        share: str = None,
        specific_md: list = [],
        # results model
        include: list = [],
        # geographic filters
        bbox: list = None,
        poly: str = None,
        georel: str = None,
        # sorting
        order_by: str = "_created",
        order_dir: str = "desc",
        # results size
        page_size: int = 20,
        offset: int = 0,
        # specific options of implemention
        augment: bool = False,
        check: bool = True,
        # tags_as_dicts: bool = False,
        whole_share: bool = False,
    ) -> ResourceSearch:
        """Search within the resources shared to the application. It's the mainly used method to retrieve metadata.

        :param str query: search terms and semantic filters. Equivalent of
         **q** parameter in Isogeo API. It could be a simple
         string like *oil* or a tag like *keyword:isogeo:formations*
         or *keyword:inspire-theme:landcover*. The *AND* operator
         is applied when various tags are passed.
        :param list bbox: Bounding box to limit the search. Must be a 4 list of coordinates in WGS84 (EPSG 4326). Could be associated with *georel*.
        :param str poly: Geographic criteria for the search, in WKT format. Could be associated with *georel*.
        :param str georel: geometric operator to apply to the `bbox` or `poly` parameters. Available values:

            * 'contains',
            * 'disjoint',
            * 'equals',
            * 'intersects' - [APPLIED BY API if NOT SPECIFIED]
            * 'overlaps',
            * 'within'.

        :param str order_by: sorting results. Available values:

            * '_created': metadata creation date [DEFAULT if relevance is null]
            * '_modified': metadata last update
            * 'title': metadata title
            * 'created': data creation date (possibly None)
            * 'modified': data last update date
            * 'relevance': relevance score calculated by API [DEFAULT].

        :param str order_dir: sorting direction. Available values:

            * 'desc': descending
            * 'asc': ascending

        :param int page_size: limits the number of results.
         Useful to paginate results display. Default value: 100.
        :param int offset: offset to start page size
         from a specific results index
        :param str share: share UUID to filter on
        :param list specific_md: list of metadata UUIDs to filter on
        :param list include: subresources that should be returned.
         Must be a list of strings. Available values: *isogeo.SUBRESOURCES*
        :param bool whole_share: option to return all results or only the
                                page size. *False* by DEFAULT.
        :param bool check: option to check query parameters and avoid erros.
         *True* by DEFAULT.
        :param bool augment: option to improve API response by adding
         some tags on the fly (like shares_id)
        :param bool tags_as_dicts: option to store tags as key/values by filter.
        """
        # handling request parameters
        payload = {
            "_id": checker._check_filter_specific_md(specific_md),
            "_include": checker._check_filter_includes(
                includes=include, entity="metadata"
            ),
            "_limit": page_size,
            "_offset": offset,
            "box": bbox,
            "geo": poly,
            "rel": georel,
            "ob": order_by,
            "od": order_dir,
            "q": query,
            "s": share,
        }

        # check query parameters
        if query and check:
            checker.check_request_parameters(payload)
        else:
            pass

        # URL
        url_resources_search = utils.get_request_base_url(route="resources/search")

        # request
        req_metadata_search = self.api_client.get(
            url=url_resources_search,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=(5, 200),
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_search)
        if isinstance(req_check, tuple):
            return req_check

        # store search response
        req_metadata_search = ResourceSearch(**req_metadata_search.json())

        # add shares to tags and query
        if augment:
            self.add_tags_shares(req_metadata_search.tags)
            if share:
                req_metadata_search.query["_shares"] = [share]
            else:
                req_metadata_search.query["_shares"] = []
        else:
            pass

        # end of method
        return req_metadata_search

    # -- UTILITIES -----------------------------------------------------------
    def add_tags_shares(self, tags: dict = dict()):
        """Add shares list to the tags attributes in search results.

        :param dict tags: tags dictionary from a search request
        """
        # check if shares_id have already been retrieved or not
        if not hasattr(self.api_client, "shares_id"):
            shares = self.api_client.share.listing()
            self.api_client.shares_id = {
                "share:{}".format(i.get("_id")): i.get("name") for i in shares
            }
        else:
            pass
        # update query tags
        tags.update(self.api_client.shares_id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_metadata = ApiSearch()
    print(api_metadata)
