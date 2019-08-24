# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Users entities

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
from isogeo_pysdk.models import Contact, User
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
class ApiUser:
    """Routes as methods of Isogeo API used to manipulate users.
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
        super(ApiUser, self).__init__()

    # -- Routes to manage the  User objects ---------------------------------------
    @ApiDecorators._check_bearer_validity
    def listing(self) -> list:
        """Get registered users.

        :Example:

        >>> # get all registered users
        >>> users = isogeo.user.listing()
        >>> print(len(users))
        925
        >>> # filter on staff users (as list)
        >>> staff = [user for user in users if user.get("staff")]
        >>> print(len(staff))
        10
        >>> # filter on users with an email from isogeo(as list)
        >>> users_isogeo = [user for user in users if "@isogeo" in user.get("contact").get("email")]
        >>> print(len(users_isogeo))
        37
        """
        # handling request parameters
        payload = {"_include": ["memberships"]}

        # request URL
        url_users = utils.get_request_base_url(route="users")

        # request
        req_users = self.api_client.get(
            url=url_users,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_users)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_users.json()

    @ApiDecorators._check_bearer_validity
    def user(self, user_id: str, include: list = ["_abilities"]) -> User:
        """Get details about a specific user.

        :param str user_id: user UUID
        :param list include: additionnal subresource to include in the response
        """
        # check user UUID
        if not checker.check_is_uuid(user_id):
            raise ValueError("User ID is not a correct UUID.")
        else:
            pass

        # handling request parameters
        payload = {"_include": ",".join(include)}

        # URL
        url_user = utils.get_request_base_url(route="users/{}".format(user_id))

        # request
        req_user = self.api_client.get(
            url=url_user,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_user)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return User(**req_user.json())

    # @ApiDecorators._check_bearer_validity
    # def create(self, user: object = User(), check_exists: int = 1) -> User:
    #     """Add a new user to Isogeo.

    #     :param class user: User model object to create
    #     :param int check_exists: check if a user already exists:

    #     - 0 = no check
    #     - 1 = compare name [DEFAULT]

    #     """
    #     # check if object has a correct contact
    #     if not hasattr(user, "contact") or not isinstance(user.contact, Contact):
    #         raise ValueError("`user.contact.name`is required to create a user.")

    #     # check if user already exists in user
    #     if check_exists == 1:
    #         # retrieve user users
    #         if not self.api_client._users_names:
    #             self.listing(include=[])
    #         # check
    #         if user.contact.name in self.api_client._users_names:
    #             logger.debug(
    #                 "User with the same name already exists: {}. Use 'user_update' instead.".format(
    #                     user.contact.name
    #                 )
    #             )
    #             return False
    #     else:
    #         pass

    #     # URL
    #     url_user_create = utils.get_request_base_url(route="users")

    #     # request
    #     req_new_user = self.api_client.post(
    #         url=url_user_create,
    #         data=user.to_dict_creation(),
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_new_user)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     # load new user and save it to the cache
    #     new_user = User(**req_new_user.json())
    #     self.api_client._users_names[new_user.contact.get("name")] = new_user._id

    #     # end of method
    #     return new_user

    # @ApiDecorators._check_bearer_validity
    # def update(self, user: User) -> User:
    #     """Update a user.

    #     :param class user: User model object to update
    #     """
    #     # check user UUID
    #     if not checker.check_is_uuid(user._id):
    #         raise ValueError("User ID is not a correct UUID: {}".format(user._id))
    #     else:
    #         pass

    #     # URL
    #     url_user_update = utils.get_request_base_url(route="users/{}".format(user._id))

    #     # request
    #     req_user_update = self.api_client.put(
    #         url=url_user_update,
    #         json=user.to_dict_creation(),
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_user_update)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     # end of method
    #     return User(**req_user_update.json())

    # # -- Routes to manage the related objects ------------------------------------------
    # @ApiDecorators._check_bearer_validity
    # def memberships(self, user_id: str) -> dict:
    #     """Returns memberships for the specified user.

    #     :param str user_id: user UUID
    #     """
    #     # URL builder
    #     url_user_memberships = utils.get_request_base_url(
    #         route="users/{}/memberships".format(user_id)
    #     )

    #     # request
    #     req_user_memberships = self.api_client.get(
    #         url=url_user_memberships,
    #         headers=self.api_client.header,
    #         proxies=self.api_client.proxies,
    #         verify=self.api_client.ssl,
    #         timeout=self.api_client.timeout,
    #     )

    #     # checking response
    #     req_check = checker.check_api_response(req_user_memberships)
    #     if isinstance(req_check, tuple):
    #         return req_check

    #     return req_user_memberships.json()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_user = ApiUser()
