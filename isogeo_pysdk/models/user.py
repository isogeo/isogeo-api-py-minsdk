# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of User entity

    See: http://help.isogeo.com/api/complete/index.html#definition-user
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint

# submodels
from isogeo_pysdk.models.contact import Contact


# #############################################################################
# ########## Classes ###############
# ##################################
class User(object):
    """Users in Isogeo platform.

    Sample:

    ```json
    {
        '_created': '2014-03-14T14:11:40.6815298+00:00',
        '_id': '89ee0eb3a15046a28886033b27f1d882',
        '_modified': '2018-06-07T08:13:32.0826782+00:00',
        'contact': {
            '_deleted': False,
            '_id': '647ce48061a64faf9f75577a41a63229',
            '_tag': 'contact:user:647ce48061a64faf9f75577a41a63229',
            'addressLine1': '26 rue du faubourg Saint-Antoine',
            'available': False,
            'city': 'Paris',
            'countryCode': 'FR',
            'email': 'julien.moura@isogeo.com',
            'hash': '23bc09e00e945c3c2cc0d13f7448c261',
            'name': 'Julien MOURA',
            'phone': '+33 6 58 00 30 64',
            'type': 'user',
            'zipCode': '75012'
            },
    'language': '',
    'mailchimp': {
        'subscriptions': [
            {
                'isInterested': False,
                'name': 'NewReleases'
            },
            {
                'isInterested': False,
                'name': 'TipsAndTricks'
            }
            ]
            },
    'staff': True,
    'timezone': 'Romance Standard Time'
    }
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of user attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
      attr_map (dict): mapping between read and write attributes. {"attribute name - GET": "attribute type - POST"}
    """
    attr_types = {
        "_created": "str",
        "_id": "str",
        "_modified": "str",
        "contact": Contact,
        "language": "str",
        "mailchimp": "str",
        "staff": "bool",
        "timezone": "str",
    }

    attr_crea = {
        "contact": Contact,
        "language": "str",
        "mailchimp": "str",
        "staff": "bool",
        "timezone": "str",
    }

    attr_map = {}

    def __init__(
        self,
        _abilities: list = None,
        _created: bool = None,
        _id: str = None,
        _modified: str = None,
        contact: Contact = None,
        language: str = None,
        mailchimp: dict = None,
        staff: bool = None,
        available: bool = None,
        timezone: str = None,
    ):
        """User model"""

        # default values for the object attributes/properties
        self.__abilities = None
        self.__created = None
        self.__id = None
        self.__modified = None
        self._contact = Contact
        self._language = None
        self._mailchimp = None
        self._staff = None
        self._timezone = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _abilities is not None:
            self._abilities = _abilities
        if _created is not None:
            self._created = _created
        if _id is not None:
            self.__id = _id
        if _modified is not None:
            self.__modified = _modified
        if language is not None:
            self._language = language
        if mailchimp is not None:
            self._mailchimp = mailchimp
        if staff is not None:
            self._staff = staff
        if timezone is not None:
            self._timezone = timezone

        # required
        self._contact = contact

    # -- PROPERTIES --------------------------------------------------------------------
    # abilities
    @property
    def _abilities(self):
        """Gets the abilities of this User.  # noqa: E501


        :return: The abilities of this User.  # noqa: E501
        :rtype: Abilities
        """
        return self.__abilities

    @_abilities.setter
    def _abilities(self, _abilities):
        """Sets the abilities of this User.


        :param abilities: The abilities of this User.  # noqa: E501
        :type: Abilities
        """

        self.__abilities = _abilities

    # creation date
    @property
    def _created(self) -> str:
        """Gets the created used for Isogeo filters of this User.

        :return: The created of this User.
        :rtype: str
        """
        return self.__created

    @_created.setter
    def _created(self, _created: str):
        """Sets the created used into Isogeo filters of this User.

        :param str _created: the created of this User.
        """

        self.__created = _created

    # user UUID
    @property
    def _id(self) -> str:
        """Gets the id of this User.

        :return: The id of this User.
        :rtype: str
        """
        return self.__id

    @_id.setter
    def _id(self, _id: str):
        """Sets the id of this User.

        :param str id: The id of this User.
        """

        self.__id = _id

    # last update
    @property
    def _modified(self) -> str:
        """Gets the modified used for Isogeo filters of this User.

        :return: The modified of this User.
        :rtype: str
        """
        return self.__modified

    @_modified.setter
    def _modified(self, _modified: str):
        """Sets the modified used into Isogeo filters of this User.

        :param str _modified: the modified of this User.
        """

        self.__modified = _modified

    # contact
    @property
    def contact(self) -> Contact:
        """Gets the contact of this user.

        :return: The contact of this user.
        :rtype: dict
        """
        return self._contact

    @contact.setter
    def contact(self, contact: Contact):
        """Sets the contact of this user.

        :param dict contact: The contact of this user.
        """

        if contact is None:
            raise ValueError("Invalid value for `contact`, must not be `None`")

        self._contact = contact

    # language
    @property
    def language(self) -> str:
        """Gets the id of this User.

        :return: The id of this User.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language: str):
        """Sets the first line of the address of this User.

        :param str language: The first address line of this User.
        """

        self._language = language

    # mailchimp subscriptions
    @property
    def mailchimp(self) -> str:
        """Gets the id of this User.

        :return: The second address line of this User.
        :rtype: str
        """
        return self._mailchimp

    @mailchimp.setter
    def mailchimp(self, mailchimp: str):
        """Sets the id of this User.

        :param str mailchimp: The second address line of this User.
        """

        self._mailchimp = mailchimp

    # staff status
    @property
    def staff(self) -> str:
        """Gets the third address line of this User.

        :return: The The third address line of this User.
        :rtype: str
        """
        return self._staff

    @staff.setter
    def staff(self, staff: str):
        """Sets the third address line of this User.

        :param str staff: The The third address line of this User.
        """

        self._staff = staff

    # timezone
    @property
    def timezone(self) -> str:
        """Gets the timezone of this User.

        :return: The timezone of this User.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone: str):
        """Sets the timezone of this User.

        :param str timezone: The timezone of this User.
        """

        self._timezone = timezone

    # -- METHODS -----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.attr_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(User, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_dict_creation(self) -> dict:
        """Returns the model properties as a dict structured for creation purpose (POST)"""
        result = {}

        for attr, _ in self.attr_crea.items():
            # get attribute value
            value = getattr(self, attr)
            # switch attribute name for creation purpose
            if attr in self.attr_map:
                attr = self.attr_map.get(attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(User, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, User):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal"""
        return not self == other


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    obj = User()
    print(obj)
