# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""
    Isogeo API v1 - API Route for bulk update on resources (= Metadata)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from functools import lru_cache

# 3rd party
from requests.models import Response

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.enums import BulkActions, BulkTargets
from isogeo_pysdk.models import Metadata
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
class ApiBulk:
    """Routes as methods of Isogeo API used to mass edition of metadatas (resources).

    :Example:

    .. code-block:: python

        # retrive objects
        catalog_1 = isogeo.catalog.get(
            workgroup_id={WORKGROUP_UUID},
            catalog_id={CATALOG_UUID_1},
        )

        catalog_2 = isogeo.catalog.get(
            workgroup_id={WORKGROUP_UUID},
            catalog_id={CATALOG_UUID_2},
        )

        keyword = isogeo.keyword.get(keyword_id={KEYWORD_UUID},)

        # along the script, prepare the bulk requests
        isogeo.metadata.bulk.prepare(
            metadatas=(
                {METADATA_UUID_1},
                {METADATA_UUID_2},
            ),
            action="add",
            target="catalogs",
            models=(catalog_1, catalog_2),
        )

        isogeo.metadata.bulk.prepare(
            metadatas=(
                {METADATA_UUID_1},

            ),
            action="add",
            target="keywords",
            models=(keyword,),
        )

        # send the one-shot request
        isogeo.metadata.bulk.send()

    """

    BULK_DATA = []

    def __init__(self, api_client=None):
        if api_client is not None:
            self.api_client = api_client

        # store API client (Request [Oauthlib] Session) and pass it to the decorators
        self.api_client = api_client
        ApiDecorators.api_client = api_client

        # ensure platform to request
        (
            self.platform,
            self.api_url,
            self.app_url,
            self.csw_url,
            self.mng_url,
            self.oc_url,
            self.ssl,
        ) = utils.set_base_url(self.api_client.platform)

        # initialize
        super(ApiBulk, self).__init__()

    def prepare(self, metadatas: tuple, action: str, target: str, models: tuple):
        """Prepare requests to be sent later in one shot.

        :param tuple metadatas: tuple of metadatas UUIDs to be updated
        :param str action: TO DOC
        :param str target: TO DOC
        :param tuple models: TO DOC
        """
        # ensure lowercase
        action = action.lower()
        target = target.lower()

        # check uuid
        if not all([checker.check_is_uuid(md) for md in metadatas]):
            raise TypeError("Not all metadatas passed are valid UUID")

        # check action
        if action not in BulkActions.__members__:
            raise ValueError(
                "Action '{}' is not a valid value. Must be one of: {}".format(
                    action, " | ".join([e.name for e in BulkActions])
                )
            )
        # check target
        if target not in BulkTargets.__members__:
            raise ValueError(
                "Target '{}' is not a valid value. Must be one of: {}".format(
                    target, " | ".join([e.name for e in BulkTargets])
                )
            )

        # check passed objects
        obj_type = models[0]
        if not all([isinstance(obj, type(obj_type)) for obj in models]):
            raise TypeError(
                "Models must contain an unique type of objects. First found: {}".format(
                    obj_type
                )
            )

        # prepare request data
        data_prepared = {
            "action": action,
            "target": target,
            "query": {"ids": metadatas},
            "model": [obj.to_dict() for obj in models],
        }

        # add it to be sent later
        self.BULK_DATA.append(data_prepared)

    @ApiDecorators._check_bearer_validity
    def send(self):
        """Send prepared BULK_DATA to the `POST BULK resources/`."""

        # build request url
        url_metadata_bulk = utils.get_request_base_url(route="resources")

        # request
        req_metadata_bulk = self.api_client.post(
            url=url_metadata_bulk,
            json=self.BULK_DATA,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_metadata_bulk)
        if isinstance(req_check, tuple):
            return req_check

        # empty bulk data
        self.BULK_DATA.clear()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """standalone execution."""
    sample_test = ApiBulk()
    print(sample_test)
