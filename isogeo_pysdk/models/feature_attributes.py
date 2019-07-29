# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of FeatureAttributes entity

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint
from uuid import UUID

# #############################################################################
# ########## Classes ###############
# ##################################
class FeatureAttribute(object):
    """
    FeatureAttributes are entities included as subresource into metadata.


    :Example:

    ```json
    {
        "_id": string (uuid),
        "alias": string,
        "dataType": string,
        "description": string,
        "language": string
        "name": string,
    }
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of event attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
    """
    attr_types = {
        "_id": str,
        "alias": str,
        "dataType": str,
        "description": str,
        "language": str,
        "name": str,
        "parent_resource": str,
    }

    attr_crea = {
        "alias": str,
        "dataType": str,
        "description": str,
        "language": str,
        "name": str,
    }

    attr_map = {}

    def __init__(
        self,
        _id: str = None,
        alias: str = None,
        dataType: str = None,
        description: str = None,
        language: str = None,
        name: str = None,
        # specific to implementation
        parent_resource: str = None,
    ):
        """Metadata Feature Attribute model.
        
        :param str _id: UUID, defaults to None
        :param str alias: [description], defaults to None
        :param str dataType: [description], defaults to None
        :param str description: [description], defaults to None
        :param str language: [description], defaults to None
        :param str name: [description], defaults to None
        """

        # default values for the object attributes/properties
        self.__id = None
        self._alias = None
        self._dataType = None
        self._description = None
        # additional parameters
        self.parent_resource = parent_resource

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _id is not None:
            self.__id = _id
        if alias is not None:
            self._alias = alias
        if dataType is not None:
            self._dataType = dataType
        if description is not None:
            self._description = description
        if language is not None:
            self._language = language
        if name is not None:
            self._name = name
        if parent_resource is not None:
            self._parent_resource = parent_resource

    # -- PROPERTIES --------------------------------------------------------------------
    # event UUID
    @property
    def _id(self) -> str:
        """Gets the id of this FeatureAttribute.

        :return: The id of this FeatureAttribute.
        :rtype: str
        """
        return self.__id

    # alias
    @property
    def alias(self) -> str:
        """Gets the alias of this FeatureAttribute.

        :return: The alias of this FeatureAttribute.
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias: str):
        """Sets the alias of this FeatureAttribute.

        :param str alias: The alias of this FeatureAttribute.
        """

        self._alias = alias

    # dataType
    @property
    def dataType(self) -> str:
        """Gets the dataType of this FeatureAttribute.

        :return: The dataType of this FeatureAttribute.
        :rtype: str
        """
        return self._dataType

    @dataType.setter
    def dataType(self, dataType: str):
        """Sets the dataType of this FeatureAttribute.

        :param str dataType: The dataType of this FeatureAttribute.
        """

        self._dataType = dataType

    # description
    @property
    def description(self) -> str:
        """Gets the description of this FeatureAttribute.

        :return: The description of this FeatureAttribute.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this FeatureAttribute.

        :param str description: The description of this FeatureAttribute. Accept markdown syntax.
        """

        self._description = description

    # language
    @property
    def language(self) -> str:
        """Gets the language of this FeatureAttribute.

        :return: The language of this FeatureAttribute.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language: str):
        """Sets the language of this FeatureAttribute.

        :param str language: The language of this FeatureAttribute.
        """

        self._language = language

    # name
    @property
    def name(self) -> str:
        """Gets the name of this FeatureAttribute.

        :return: The name of this FeatureAttribute.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this FeatureAttribute.

        :param str name: The name of this FeatureAttribute.
        """

        self._name = name

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
        if issubclass(FeatureAttribute, dict):
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
        if issubclass(FeatureAttribute, dict):
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
        if not isinstance(other, FeatureAttribute):
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
    ct = FeatureAttribute()
