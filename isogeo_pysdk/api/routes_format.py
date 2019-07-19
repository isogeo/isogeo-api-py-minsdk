# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Formats entities

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# 3rd party
from requests.models import Response

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import Format
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
class ApiFormat:
    """Routes as methods of Isogeo API used to manipulate formats.
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
        super(ApiFormat, self).__init__()

    # @ApiDecorators._check_bearer_validity
    # def search(
    #     self,
    #     formats_id: str = "1616597fbc4348c8b11ef9d59cf594c8",
    #     query: str = "",
    #     offset: int = 0,
    #     order_by: str = "text",  # available values : count.group, count.isogeo, text
    #     order_dir: str = "desc",
    #     page_size: int = 20,
    #     specific_md: list = [],
    #     specific_tag: list = [],
    #     include: list = ["_abilities", "count"],
    #     caching: bool = 1,
    # ) -> FormatSearch:
    #     """Search for formats within a specific formats or a specific group.

    #     :param str formats_id: formats UUID
    #     :param str query: search terms, equivalent of **q** parameter in API.
    #     :param int offset: offset to start page size from a specific results index
    #     :param str order_by: sorting results. Available values:

    #       * 'count.isogeo': count of associated resources within Isogeo
    #       * 'text': alphabetical order  [DEFAULT if relevance is null]

    #     :param str order_dir: sorting direction. Available values:

    #       * 'desc': descending [DEFAULT]
    #       * 'asc': ascending

    #     :param int page_size: limits the number of results. Default: 20.
    #     :param list specific_md: list of metadata UUIDs to filter on
    #     :param list specific_tag: list of tags UUIDs to filter on
    #     :param list include: subresources that should be returned. Available values:

    #       * '_abilities'
    #       * 'count'
    #       * 'formats'
    #     """
    #     # specific resources specific parsing
    #     specific_md = checker._check_filter_specific_md(specific_md)
    #     # sub resources specific parsing
    #     include = checker._check_filter_includes(include, "format")
    #     # specific tag specific parsing
    #     specific_tag = checker._check_filter_specific_tag(specific_tag)

    #     # handling request parameters
    #     payload = {
    #         "_id": specific_md,
    #         "_include": include,
    #         "_limit": page_size,
    #         "_offset": offset,
    #         "_tag": specific_tag,
    #         "ob": order_by,
    #         "od": order_dir,
    #         "q": query,
    #     }

    #     # URL
    #     url_thesauri_formats = utils.get_request_base_url(
    #         route="thesauri/{}/formats/search".format(formats_id)
    #     )

    #     # request
    #     req_formats_formats = self.api_client.get(
    #         url=url_thesauri_formats,
    #         headers=self.api_client.header,
    #         params=payload,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_formats_formats)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     # end of method
    #     return FormatSearch(**req_formats_formats.json())

    @ApiDecorators._check_bearer_validity
    def listing(self, caching: bool = 1) -> list:
        """List formats available in Isogeo API.

        >>> print(len(isogeo.format.listing()))
        32
        """
        # URL
        url_formats = utils.get_request_base_url(route="formats")

        # request
        req_formats = self.api_client.get(
            url=url_formats,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_formats)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_formats.json()

    # @ApiDecorators._check_bearer_validity
    # def format(
    #     self, format_id: str, include: list = ["_abilities", "count", "formats"]
    # ) -> Format:
    #     """Get details about a specific format.

    #     :param str workgroup_id: identifier of the owner workgroup
    #     :param str format_id: format UUID
    #     :param list include: additionnal subresource to include in the response
    #     """
    #     # check workgroup UUID
    #     # if not checker.check_is_uuid(workgroup_id):
    #     #     raise ValueError(
    #     #         "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
    #     #     )
    #     # else:
    #     #     pass

    #     # check format UUID
    #     if not checker.check_is_uuid(format_id):
    #         raise ValueError("Format ID is not a correct UUID.")
    #     else:
    #         pass

    #     # request parameter
    #     payload = {"_include": include}

    #     # format route
    #     url_format = utils.get_request_base_url(route="formats/{}".format(format_id))

    #     # request
    #     req_format = self.api_client.get(
    #         url=url_format,
    #         headers=self.api_client.header,
    #         params=payload,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_format)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     # end of method
    #     return Format(**req_format.json())

    # @ApiDecorators._check_bearer_validity
    # def create(self, format: Format) -> Format:
    #     """Add a new format to the Isogeo formats.

    #     If a format with the same text already exists, the Isogeo API returns a 409 HTTP code.
    #     Then this method will try to get the closest matching format and return it.

    #     :param Format format: Format model object to create
    #     """
    #     # URL
    #     url_format_create = utils.get_request_base_url(
    #         route="thesauri/1616597fbc4348c8b11ef9d59cf594c8/formats"
    #     )

    #     # request
    #     req_new_format = self.api_client.post(
    #         url=url_format_create,
    #         json=format.to_dict_creation(),
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         timeout=self.api_client.timeout,
    #         verify=self.api_client.ssl,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_new_format)
    #     if isinstance(req_check, tuple):
    #         # handle conflict (see: https://developer.mozilla.org/fr/docs/Web/HTTP/Status/409)
    #         if req_check[1] == 409:
    #             # log conflict
    #             logger.info(
    #                 "A format with the same text already exists: '{}'. Isogeo API doesn't allow to create duplicates (HTTP {} - {}). Let's try to get the closes matching format...".format(
    #                     format.text, req_check[1], req_new_format.reason
    #                 )
    #             )
    #             # try to return the most probably matching format
    #             search_for_closest_format = self.formats(
    #                 caching=0,
    #                 include=[],
    #                 order_dir="asc",
    #                 page_size=1,
    #                 query=format.text,
    #             )
    #             if search_for_closest_format.results:
    #                 logger.info(
    #                     "Returning the closest matching format for: 'thesauri/formats/search?query={}'".format(
    #                         format.text
    #                     )
    #                 )
    #                 return Format(**search_for_closest_format.results[0])
    #             else:
    #                 logger.info(
    #                     "No match for: 'thesauri/formats/search?query={}'".format(
    #                         format.text
    #                     )
    #                 )

    #         # if other error, then return it
    #         return req_check

    #     # end of method
    #     return Format(**req_new_format.json())

    # @ApiDecorators._check_bearer_validity
    # def delete(self, format: Format):
    #     """Delete a format from Isogeo database.

    #     :param Format format: Format model object to create
    #     """
    #     # check format UUID
    #     if not checker.check_is_uuid(format._id):
    #         raise ValueError("Format ID is not a correct UUID: {}".format(format._id))
    #     else:
    #         pass

    #     # URL
    #     url_format_delete = utils.get_request_base_url(
    #         route="thesauri/1616597fbc4348c8b11ef9d59cf594c8/formats/{}".format(
    #             format._id
    #         )
    #     )

    #     # request
    #     req_format_deletion = self.api_client.delete(
    #         url=url_format_delete,
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         timeout=self.api_client.timeout,
    #         verify=self.api_client.ssl,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_format_deletion)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     return req_format_deletion


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_format = ApiFormat()
