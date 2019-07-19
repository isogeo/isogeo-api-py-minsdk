# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes to retrieve CoordinateSystems

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
from isogeo_pysdk.models import CoordinateSystem
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
class ApiCoordinateSystem:
    """Routes as methods of Isogeo API used to manipulate coordinate-systems
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
        super(ApiCoordinateSystem, self).__init__()

    @ApiDecorators._check_bearer_validity
    def listing(self, workgroup_id: str = None, caching: bool = 1) -> list:
        """Get coordinate-systems in the whole Isogeo database or into a specific workgroup.

        :param str workgroup_id: identifier of the owner workgroup. OPTIONNAL: if present, list SRS slected into the workgroup.
        :param bool caching: option to cache the response

        :rtype: list

        :Example:

        >>> # list all coordinate-systems in the whole Isogeo database
        >>> srs = isogeo.srs.listing()
        >>> print(len(srs))
        4301
        >>> # list coordinate-systems which have been selected in a specific workgroup
        >>> srs = isogeo.srs.listing(workgroup_id=WORKGROUP_UUID)
        >>> print(len(srs))
        5
        """
        # check if workgroup or global
        if workgroup_id is None:
            # request URL
            url_coordinate_systems = utils.get_request_base_url(
                route="coordinate-systems"
            )
        else:
            # check workgroup UUID
            if not checker.check_is_uuid(workgroup_id):
                raise ValueError(
                    "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
                )
            # request URL
            url_coordinate_systems = utils.get_request_base_url(
                route="groups/{}/coordinate-systems".format(workgroup_id)
            )

        # request
        req_coordinate_systems = self.api_client.get(
            url=url_coordinate_systems,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_coordinate_systems)
        if isinstance(req_check, tuple):
            return req_check

        coordinate_systems = req_coordinate_systems.json()

        # if caching use or store the workgroup coordinate_systems
        if caching and workgroup_id is None:
            self.api_client._coordinate_systems = coordinate_systems
        elif caching:
            self.api_client._wg_coordinate_systems = coordinate_systems
        else:
            pass

        # end of method
        return coordinate_systems

    @ApiDecorators._check_bearer_validity
    def coordinate_system(
        self, coordinate_system_code: str, workgroup_id: str = None
    ) -> CoordinateSystem:
        """Get details about a specific coordinate_system, from the whole Isogeo database or
        into a specific workgroup (to get the SRS alias for example).

        :param str workgroup_id: identifier of the owner workgroup. OPTIONNAL: if present, list SRS slected into the workgroup.
        :param str coordinate_system_id: EPSG code of the coordinate system

        :rtype: CoordinateSystem

        :Example:

        >>> # list all coordinate-systems in the whole Isogeo database
        >>> srs = isogeo.srs.listing()
        >>> # print details about the first SRS found
        >>> pprint.pprint(isogeo.srs.coordinate_system(srs[0].get("code")))
        {
            '_tag': 'coordinate-system:4143',
            'code': 4143,
            'name': 'Abidjan 1987'
        }
        """
        # check if workgroup or global
        if workgroup_id is None:
            # request URL
            url_coordinate_system = utils.get_request_base_url(
                route="coordinate-systems/{}".format(coordinate_system_code)
            )
        else:
            # check workgroup UUID
            if not checker.check_is_uuid(workgroup_id):
                raise ValueError(
                    "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
                )
            # request URL
            url_coordinate_systems = utils.get_request_base_url(
                route="groups/{}/coordinate-systems/{}".format(
                    workgroup_id, coordinate_system_code
                )
            )

        # request
        req_coordinate_system = self.api_client.get(
            url=url_coordinate_system,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_coordinate_system)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return CoordinateSystem(**req_coordinate_system.json())


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_coordinate_system = ApiCoordinateSystem()
