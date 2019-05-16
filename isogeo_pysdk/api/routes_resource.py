# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Resources (= Metadata) entity

    See: http://help.isogeo.com/api/complete/index.html#definition-resource
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.utils import IsogeoUtils

# #############################################################################
# ########## Libraries #############
# ##################################

checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiResource:
    """Routes as methods of Isogeo API used to manipulate metadatas (resources).
    """

    def __init__(self, api_client):
        self.api_client = api_client
        # ensure platform to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            self.api_client.platform
        )
        super(ApiResource, self).__init__()

    def workgroup_metadatoto(
        self,
        workgroup_id: str,
        order_by: str = "_created",
        order_dir: str = "desc",
        page_size: int = 100,
        offset: int = 0,
    ) -> dict:
        """List workgroup metadata.

        :param str workgroup_id: identifier of the owner workgroup
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # request parameters
        payload = {
            # "_include": include,
            # "_lang": self.lang,
            "_limit": page_size,
            "_offset": offset,
            "ob": order_by,
            "od": order_dir,
            # "q": query,
            # "s": share,
        }

        # build request url
        url_metadata_list = utils.get_request_base_url(
            route="groups/{}/resources/search".format(workgroup_id)
        )

        wg_metadata = self.api_client.get(
            url_metadata_list,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        wg_metadata = wg_metadata.json()

        # # if caching use or store the workgroup metadata
        # if caching and not self._wg_apps_names:
        #     self._wg_apps_names = {i.get("name"): i.get("_id") for i in wg_metadata}

        return wg_metadata


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_resource = ApiResource()
    print(api_resource)