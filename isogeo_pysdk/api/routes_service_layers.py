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
        """Get all service layers of a metadata.

        :param Metadata metadata: metadata (resource) to edit
        """
        # check metadata type
        if metadata.type != "service":
            raise TypeError(
                "Layers routes are only available for metadata of services, not: {}".format(
                    metadata.type
                )
            )
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

    @ApiDecorators._check_bearer_validity
    def layer(self, metadata_id: str, layer_id: str) -> ServiceLayer:
        """Get details about a specific service_layer.

        :param str metadata_id: metadata with layers
        :param str layer_id: service layer UUID
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # check service_layer UUID
        if not checker.check_is_uuid(layer_id):
            raise ValueError(
                "ServiceLayer ID is not a correct UUID: {}".format(layer_id)
            )
        else:
            pass

        # URL
        url_service_layer = utils.get_request_base_url(
            route="resources/{}/layers/{}".format(metadata_id, layer_id)
        )

        # request
        req_service_layer = self.api_client.get(
            url=url_service_layer,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_service_layer)
        if isinstance(req_check, tuple):
            return req_check

        # add parent resource id to keep tracking
        service_layer_augmented = req_service_layer.json()
        service_layer_augmented["parent_resource"] = metadata_id

        # end of method
        return ServiceLayer(**service_layer_augmented)

    @ApiDecorators._check_bearer_validity
    def create(self, metadata: Metadata, layer: ServiceLayer) -> ServiceLayer:
        """Add a new layer to a metadata (= resource).

        :param Metadata metadata: metadata (resource) to edit. Must be a service.
        :param ServiceLayer ServiceLayer: service_layer object to create
        """
        # check metadata type
        if metadata.type != "service":
            raise TypeError(
                "Layers routes are only available for metadata of services, not: {}".format(
                    metadata.type
                )
            )
        else:
            pass

        # URL
        url_service_layer_create = utils.get_request_base_url(
            route="resources/{}/layers/".format(metadata._id)
        )

        # request
        req_new_service_layer = self.api_client.post(
            url=url_service_layer_create,
            json=layer.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_new_service_layer)
        if isinstance(req_check, tuple):
            return req_check

        # add parent resource id to keep tracking
        service_layer_augmented = req_new_service_layer.json()
        service_layer_augmented["parent_resource"] = metadata._id

        # end of method
        return ServiceLayer(**service_layer_augmented)

    @ApiDecorators._check_bearer_validity
    def delete(self, layer: ServiceLayer, metadata: Metadata = None):
        """Delete a service layer from Isogeo database.

        :param Metadata metadata: parent metadata (resource) containing the service_layer
        :param ServiceLayer layer: ServiceLayer model object to delete
        """
        # check service_layer UUID
        if not checker.check_is_uuid(layer._id):
            raise ValueError(
                "ServiceLayer ID is not a correct UUID: {}".format(layer._id)
            )
        else:
            pass

        # retrieve parent metadata
        if not checker.check_is_uuid(layer.parent_resource) and not metadata:
            raise ValueError(
                "ServiceLayer parent metadata is required. Requesting it..."
            )
        elif not checker.check_is_uuid(layer.parent_resource) and metadata:
            layer.parent_resource = metadata._id
        else:
            pass

        # URL
        url_service_layer_delete = utils.get_request_base_url(
            route="resources/{}/layers/{}".format(layer.parent_resource, layer._id)
        )

        # request
        req_service_layer_deletion = self.api_client.delete(
            url=url_service_layer_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_service_layer_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_service_layer_deletion


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_service_layer = ApiServiceLayer()
