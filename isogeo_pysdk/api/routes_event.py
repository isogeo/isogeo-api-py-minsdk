# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Events entities

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
from isogeo_pysdk.models import Event, Metadata
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
class ApiEvent:
    """Routes as methods of Isogeo API used to manipulate events.
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
        super(ApiEvent, self).__init__()

    @ApiDecorators._check_bearer_validity
    def listing(self, metadata: Metadata) -> list:
        """Get all events of a metadata.

        :param Metadata metadata: metadata (resource) to edit
        """
        # URL
        url_events = utils.get_request_base_url(
            route="resources/{}/events/".format(metadata._id)
        )

        # request
        req_events = self.api_client.get(
            url=url_events,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_events)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_events.json()

    @ApiDecorators._check_bearer_validity
    def event(self, metadata_id: str, event_id: str) -> Event:
        """Get details about a specific event.

        :param str event_id: event UUID to get
        :param str event_id: event UUID
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # check event UUID
        if not checker.check_is_uuid(event_id):
            raise ValueError("Event ID is not a correct UUID.")
        else:
            pass

        # URL
        url_event = utils.get_request_base_url(
            route="resources/{}/events/{}".format(metadata_id, event_id)
        )

        # request
        req_event = self.api_client.get(
            url=url_event,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_event)
        if isinstance(req_check, tuple):
            return req_check

        # add parent resource id to keep tracking
        event_augmented = req_event.json()
        event_augmented["parent_resource"] = metadata_id

        # end of method
        return Event(**event_augmented)

    @ApiDecorators._check_bearer_validity
    def create(
        self,
        metadata: Metadata,
        event_date: str or datetime,
        event_comment: str = None,
        event_kind: str = "update",
    ) -> Event:
        """Add a new event to a metadata (= resource).

        :param Metadata metadata: metadata (resource) to edit
        :param str event_date: date of the event. Must be in the format `YYYY-MM-DD`
        :param str event_kind: kind of event. Must be one of: creation, update, publication
        :param str event_comment: text to associate to the event. Not possible for event_kind=='creation'
        """
        # check params
        if event_kind not in ("creation", "update", "publication"):
            raise ValueError(
                "'event_kind' must be one of: creation, update, publication"
            )

        if isinstance(event_date, str):
            datetime.strptime(event_date, "%Y-%m-%d")
        elif isinstance(event_date, datetime):
            event_date = event_date.strftime("%Y-%m-%d")
        else:
            raise TypeError("'event_date' must be a str or a datetime")

        # ensure that a creation date doesn't already exist
        if event_kind == "creation":
            # retrieve metadata events
            metadata_events = self.api_client.resource(metadata._id, include=["events"])
            # filter on creation events
            events_creation = list(
                filter(
                    lambda d: d["kind"] in ["creation"], metadata_events.get("events")
                )
            )
            if events_creation:
                logger.warning(
                    "A creation event already exist. A metadata can only have one creation event. Use event_update instead."
                )
                return self.event(metadata._id, events_creation[0].get("_id"))

        # ensure removing event_comment for creation dates
        if event_kind == "creation" and event_comment:
            event_comment = None
            logger.warning("Event comments are not allowed for creation dates")

        # URL
        url_event_create = utils.get_request_base_url(
            route="resources/{}/events/".format(metadata._id)
        )

        # request
        req_new_event = self.api_client.post(
            url=url_event_create,
            json={"date": event_date, "description": event_comment, "kind": event_kind},
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_new_event)
        if isinstance(req_check, tuple):
            return req_check

        # add parent resource id to keep tracking
        event_augmented = req_new_event.json()
        event_augmented["parent_resource"] = metadata._id

        # end of method
        return Event(**event_augmented)

    @ApiDecorators._check_bearer_validity
    def delete(self, metadata: Metadata, event_id: str):
        """Delete a event from Isogeo database.

        :param Metadata metadata: metadata (resource) to edit
        :param str event_id: UUID of the event to delete
        """
        # check event UUID
        if not checker.check_is_uuid(event_id):
            raise ValueError("Event ID is not a correct UUID: {}".format(event_id))
        else:
            pass

        # URL
        url_event_delete = utils.get_request_base_url(
            route="resources/{}/events/{}".format(metadata._id, event_id)
        )

        # request
        req_event_deletion = self.api_client.delete(
            url=url_event_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_event_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_event_deletion

    # @ApiDecorators._check_bearer_validity
    # def event_update(self, event: Event, caching: bool = 1) -> Event:
    #     """Update a event owned by a workgroup.

    #     :param class event: Event model object to update
    #     :param bool caching: option to cache the response
    #     """
    #     # check event UUID
    #     if not checker.check_is_uuid(event._id):
    #         raise ValueError("Event ID is not a correct UUID: {}".format(event._id))
    #     else:
    #         pass

    #     # URL
    #     url_event_update = utils.get_request_base_url(
    #         route="events/{}".format(event._id)
    #     )

    #     # request
    #     req_event_update = self.api_client.put(
    #         url=url_event_update,
    #         json=event.to_dict_creation(),
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_event_update)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     # update event in cache
    #     new_event = Event(**req_event_update.json())
    #     if caching:
    #         self.api_client._events_names[new_event.name] = new_event._id

    #     # end of method
    #     return new_event


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_event = ApiEvent()
