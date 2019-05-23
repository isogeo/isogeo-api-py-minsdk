# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Resources (= Metadata) entity

    See: http://help.isogeo.com/api/complete/index.html#definition-resource
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.utils import IsogeoUtils
from isogeo_pysdk.models import Metadata

from .routes_event import ApiEvent

# #############################################################################
# ########## Libraries #############
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiResource:
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

        # sub routes
        self.events = ApiEvent(self.api_client)

        # initialize
        super(ApiResource, self).__init__()

    @ApiDecorators._check_bearer_validity
    def metadata(self, metadata_id: str, include: list = []) -> Metadata:
        """Get complete or partial metadata abou a specific metadata (= resource).

        :param str metadata_id: metadata UUID to get
        :param list include: subresources that should be included.
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # request parameters
        payload = {"_include": checker._check_filter_includes(include)}

        # URL
        url_resource = utils.get_request_base_url(
            route="resources/{}".format(metadata_id)
        )

        # request
        req_resource = self.api_client.get(
            url=url_resource,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_resource)
        if isinstance(req_check, tuple):
            return req_check

        # handle bad JSON attribute
        metadata = req_resource.json()
        metadata["coordinateSystem"] = metadata.pop("coordinate-system", list)
        metadata["featureAttributes"] = metadata.pop("feature-attributes", list)

        # end of method
        return Metadata(**metadata)

    # def workgroup_metadata(
    #     self,
    #     workgroup_id: str,
    #     order_by: str = "_created",
    #     order_dir: str = "desc",
    #     page_size: int = 100,
    #     offset: int = 0,
    # ) -> dict:
    #     """List workgroup metadata.

    #     :param str workgroup_id: identifier of the owner workgroup
    #     """
    #     # check workgroup UUID
    #     if not checker.check_is_uuid(workgroup_id):
    #         raise ValueError("Workgroup ID is not a correct UUID.")
    #     else:
    #         pass

    #     # request parameters
    #     payload = {
    #         # "_include": include,
    #         # "_lang": self.lang,
    #         "_limit": page_size,
    #         "_offset": offset,
    #         "ob": order_by,
    #         "od": order_dir,
    #         # "q": query,
    #         # "s": share,
    #     }

    #     # build request url
    #     url_metadata_list = utils.get_request_base_url(
    #         route="groups/{}/resources/search".format(workgroup_id)
    #     )

    #     wg_metadata = self.api_client.get(
    #         url_metadata_list,
    #         headers=self.api_client.header,
    #         params=payload,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     wg_metadata = wg_metadata.json()

    #     # # if caching use or store the workgroup metadata
    #     # if caching and not self._wg_apps_names:
    #     #     self._wg_apps_names = {i.get("name"): i.get("_id") for i in wg_metadata}

    #     return wg_metadata


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_resource = ApiResource()
    print(api_resource)
