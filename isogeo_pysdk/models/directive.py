# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of Directive entity

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint


# #############################################################################
# ########## Classes ###############
# ##################################
class Directive(object):
    """Directives are entities included as subresource into metadata for data history description.


    Sample:

    ```json
    [
        {
            "_id": string (uuid),
            "name": string,
            "description": string
        }
    ]
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of directive attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
    """
    attr_types = {"_id": str, "description": str, "name": str}

    attr_crea = {"description": str, "name": str}

    attr_map = {}

    def __init__(self, _id: str = None, description: str = None, name: str = None):
        """Directive model"""

        # default values for the object attributes/properties
        self.__id = None
        self._description = None
        self._name = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _id is not None:
            self.__id = _id
        if description is not None:
            self._description = description
        if name is not None:
            self._name = name

    # -- PROPERTIES --------------------------------------------------------------------
    # directive UUID
    @property
    def _id(self) -> str:
        """Gets the id of this Directive.

        :return: The id of this Directive.
        :rtype: str
        """
        return self.__id

    # description
    @property
    def description(self) -> str:
        """Gets the description of this Directive.

        :return: The description of this Directive.
        :rtype: str
        """
        return self._description

    # name
    @property
    def name(self) -> str:
        """Gets the name of this Directive.

        :return: The name of this Directive.
        :rtype: str
        """
        return self._name

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
        if issubclass(Directive, dict):
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
        if issubclass(Directive, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pdirective(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, Directive):
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
    test = Directive()