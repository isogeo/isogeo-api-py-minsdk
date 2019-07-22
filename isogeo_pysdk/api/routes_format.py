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
    #     url_format_formats = utils.get_request_base_url(
    #         route="format/{}/formats/search".format(formats_id)
    #     )

    #     # request
    #     req_formats_formats = self.api_client.get(
    #         url=url_format_formats,
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

        :returns: list of dicts
        :rtype: list

        :Example:
        >>> formats = isogeo.format.listing()
        >>> # count all formats
        >>> print(len(formats))
        32
        >>> # list all unique codes
        >>> formats_codes = [i.get("code") for i in formats]
        >>> pprint.pprint(formats_codes)
        [
            'apic',
            'arcsde',
            'dgn',
            'dwg',
            'dxf',
            ...
        ]
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

        # cache
        if caching:
            self.api_client._formats = req_formats.json()

        # end of method
        return req_formats.json()

    @ApiDecorators._check_bearer_validity
    def get(self, format_code: str) -> Format:
        """Get details about a specific format.

        :param str format_code: format code

        :rtype: Format

        :Example:
        >>> pprint.pprint(isogeo.format.get("postgis"))
        {
            '_id': string (uuid),
            '_tag': 'format:postgis',
            'aliases': [],
            'code': 'postgis',
            'name': 'PostGIS',
            'type': 'dataset',
            'versions': [
                '2.2',
                '2.1',
                '2.0',
                '1.5',
                '1.4',
                '1.3',
                '1.2',
                '1.1',
                '1.0',
                '0.9',
                None
                ]
        }
        """

        # format route
        url_format = utils.get_request_base_url(route="formats/{}".format(format_code))

        # request
        req_format = self.api_client.get(
            url=url_format,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_format)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return Format(**req_format.json())

    @ApiDecorators._check_bearer_validity
    def create(self, frmt: Format, check_exists: bool = 1) -> Format:
        """Add a new format to the Isogeo formats database.

        If a format with the same code already exists, the Isogeo API returns a 500 HTTP code.
        To prevent this error, use the check_exists option or check by yourself before.

        :param Format frmt: Format model object to create
        :param bool check_exists: check if a format with the same code exists before

        :rtype: Format or tuple

        :Example:
        >>> format_to_add = Format(
            code="geojson",
            name="GeoJSON",
            type="vectorDataset"
        )
        >>> print(isogeo.format.create(format_to_add))
        {
            '_id': string (uuid),
            '_tag': 'format:geojson',
            'aliases': [],
            'code': 'geojson',
            'name': 'GeoJSON',
            'type': 'vectorDataset',
            'versions': []
        }
        """
        # check format code
        if not frmt.code:
            raise ValueError("Format code is required: {}".format(frmt.code))
        else:
            pass

        # check if format code doesn't exist
        if check_exists:
            # use cache if possible to retrive formats codes
            if self.api_client._formats:
                formats_codes = [i.get("code") for i in self.api_client._formats]
            else:
                formats_codes = [i.get("code") for i in self.listing()]
            # check if new code already exists
            if frmt.code in formats_codes:
                raise ValueError(
                    "Format code already exists: {}. Consider using 'format.update' instead.".format(
                        frmt.code
                    )
                )
        else:
            pass

        # URL
        url_format_create = utils.get_request_base_url(route="formats")

        # request
        req_new_format = self.api_client.post(
            url=url_format_create,
            json=frmt.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        print(req_new_format)
        req_check = checker.check_api_response(req_new_format)
        if isinstance(req_check, tuple):
            return req_check

        # update cache
        self.api_client._formats.append(req_new_format.json())

        # end of method
        return Format(**req_new_format.json())

    @ApiDecorators._check_bearer_validity
    def delete(self, frmt: Format):
        """Delete a format from Isogeo database.

        :param Format frmt: Format model object to delete
        """
        # URL
        url_format_delete = utils.get_request_base_url(
            route="formats/{}".format(frmt.code)
        )

        # request
        req_format_deletion = self.api_client.delete(
            url=url_format_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_format_deletion)
        if isinstance(req_check, tuple):
            return req_check

        # update cache
        self.listing()

        return req_format_deletion

    @ApiDecorators._check_bearer_validity
    def update(self, frmt: Format) -> Format:
        """Update a format in Isogeo database.

        :param Format frmt: Format model object to update

        :rtype: Format

        :Example:
        >>> # retrieve format to update
        >>> fmt_postgis = isogeo.format.get("postgis")
        >>> # add new versions locally
        >>> fmt_postgis.versions.extend(["3.0", "3.1])
        >>> # update online
        >>> fmt_postgis_updted = isogeo.format.update(fmt_pgis)
        """
        # check format UUID
        if not checker.check_is_uuid(frmt._id):
            raise ValueError("Format ID is not a correct UUID: {}".format(frmt._id))
        else:
            pass
        # check format required code
        if not frmt.code:
            raise ValueError("Format code is required")
        else:
            pass

        # URL
        url_format_update = utils.get_request_base_url(
            route="formats/{}".format(frmt.code)
        )

        # request
        req_format_update = self.api_client.put(
            url=url_format_update,
            json=frmt.to_dict(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_format_update)
        if isinstance(req_check, tuple):
            return req_check

        # update cache
        self.listing()

        # end of method
        return Format(**req_format_update.json())


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_format = ApiFormat()
