# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of CoordinateSystem entity

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
class CoordinateSystem(object):
    """CoordinateSystems.

    Sample:

    ```json
    {
        '_tag': 'coordinate-system:31154',
        'code': 31154,
        'name': 'Zanderij / TM 54 NW'
    },
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of datasource attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
    """

    attr_types = {"_tag": str, "code": str, "name": str}

    attr_crea = {}

    attr_map = {}

    def __init__(self, _tag: str = None, code: str = None, name: str = None):
        """CoordinateSystem model"""

        # default values for the object attributes/properties
        self.__tag = None
        self._code = None
        self._name = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _tag is not None:
            self.__tag = _tag
        if code is not None:
            self._code = code
        if name is not None:
            self._name = name

    # -- PROPERTIES --------------------------------------------------------------------
    # tag
    @property
    def _tag(self) -> str:
        """Gets the tag used for Isogeo filters of this CoordinateSystem.

        :return: The tag of this CoordinateSystem.
        :rtype: str
        """
        return self.__tag

    # EPSG code
    @property
    def code(self) -> str:
        """Gets the EPSG code of this CoordinateSystem.

        :return: The EPSG code of this CoordinateSystem.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code: str):
        """Sets the code of this CoordinateSystem.

        :param str code: The code of this CoordinateSystem.
        """

        self._code = code

    # name
    @property
    def name(self) -> str:
        """Gets the name of this CoordinateSystem.

        :return: The name of this CoordinateSystem.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this CoordinateSystem.

        :param str name: The name of this CoordinateSystem.
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
        if issubclass(CoordinateSystem, dict):
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
        if issubclass(CoordinateSystem, dict):
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
        if not isinstance(other, CoordinateSystem):
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
    atasource = CoordinateSystem(
        name="CoordinateSystem Test", _modified="Test datasource _modified"
    )
    print(atasource)
