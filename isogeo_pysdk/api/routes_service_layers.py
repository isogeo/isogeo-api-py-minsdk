# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for ServiceLayers entities

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from datetime import datetime

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import ServiceLayer, Metadata
from isogeo_pysdk.utils import IsogeoUtils

# #############################################################################
# ########## Global ################
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiServiceLayer:
    """Routes as methods of Isogeo API used to manipulate service_layers.
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
        super(ApiServiceLayer, self).__init__()

    @ApiDecorators._check_bearer_validity
    def listing(self, metadata: Metadata) -> list:
        """Get all service_layers of a metadata.

        :param Metadata metadata: metadata (resource) to edit
        """
        # check metadata type
        if metadata.type != "service":
            raise TypeError("Layers routes are only available for metadata of services, not: {}".format(metadata.type))
        else:
            pass

        # URL
        url_service_layers = utils.get_request_base_url(
            route="resources/{}/layers/".format(metadata._id)
        )

        # request
        req_service_layers = self.api_client.get(
            url=url_service_layers,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_service_layers)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_service_layers.json()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_service_layer = ApiServiceLayer()
