# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Conditions entities

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from functools import lru_cache

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import Condition
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
class ApiCondition:
    """Routes as methods of Isogeo API used to manipulate conditions.
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
        super(ApiCondition, self).__init__()

    @lru_cache()
    @ApiDecorators._check_bearer_validity
    def list(self, metadata_id: str) -> list:
        """List metadata's conditions with complete information.

        :param str metadata_id: metadata UUID

        :returns: the list of conditions associated with the metadata
        :rtype: list
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # URL
        url_metadata_conditions = utils.get_request_base_url(
            route="resources/{}/conditions/".format(metadata_id)
        )

        # request
        req_metadata_conditions = self.api_client.get(
            url=url_metadata_conditions,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_conditions)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_metadata_conditions.json()

    @lru_cache()
    @ApiDecorators._check_bearer_validity
    def get(
        self,
        workgroup_id: str,
        condition_id: str,
        include: list = ["_abilities", "count"],
    ) -> Condition:
        """Get details about a specific condition.

        :param str workgroup_id: identifier of the owner workgroup
        :param str condition_id: condition UUID
        :param list include: additionnal subresource to include in the response
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass
        # check condition UUID
        if not checker.check_is_uuid(condition_id):
            raise ValueError(
                "Condition ID is not a correct UUID: {}".format(condition_id)
            )
        else:
            pass

        # request parameter
        payload = {"_include": include}

        # condition route
        url_condition = utils.get_request_base_url(
            route="groups/{}/conditions/{}".format(workgroup_id, condition_id)
        )

        # request
        req_condition = self.api_client.get(
            url=url_condition,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_condition)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return Condition.clean_attributes(req_condition.json())


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_condition = ApiCondition()
