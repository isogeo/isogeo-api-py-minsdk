# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of ServiceOperation entity

    See: http://help.isogeo.com/api/complete/index.html#definition-serviceOperation
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint

# submodels
# from isogeo_pysdk.models.resource import Resource as Metadata


# #############################################################################
# ########## Classes ###############
# ##################################
class ServiceOperation(object):
    """ServiceOperations are entities defining rules of data creation.


    Sample:

    ```json
    {
    "_id": "string (uuid)",
    "mimeTypesOutIn": [
        "string"
    ],
    "mimeTypesOutOut": [
        "string"
    ],
    "name": "string",
    "url": "string",
    "verb": "string"
    }
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of service layer attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
      attr_map (dict): mapping between read and write attributes. {"attribute name - GET": "attribute type - POST"}
    """
    attr_types = {
        "_id": str,
        "mimeTypesOutIn": list,
        "mimeTypesOutOut": list,
        "name": str,
        "url": str,
        "verb": str,
    }

    attr_crea = {"name": str, "verb": str}

    attr_map = {}

    def __init__(
        self,
        _id: str = None,
        mimeTypesOutIn: str = None,
        mimeTypesOutOut: str = None,
        name: str = None,
        verb: str = None,
        # additional parameters
        parent_resource: str = None,
    ):
        """ServiceOperation model"""

        # default values for the object attributes/properties
        self.__id = None
        self._mimeTypesOutIn = None
        self._mimeTypesOutOut = None
        self._name = None
        self._verb = None
        # additional parameters
        self.parent_resource = parent_resource

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _id is not None:
            self.__id = _id
        if mimeTypesOutIn is not None:
            self._mimeTypesOutIn = mimeTypesOutIn
        if mimeTypesOutOut is not None:
            self._mimeTypesOutOut = mimeTypesOutOut
        if name is not None:
            self._name = name
        if verb is not None:
            self._verb = verb
        # additional parameters
        if parent_resource is not None:
            self._parent_resource = parent_resource

    # -- PROPERTIES --------------------------------------------------------------------
    # service layer UUID
    @property
    def _id(self) -> str:
        """Gets the id of this ServiceOperation.

        :return: The id of this ServiceOperation.
        :rtype: str
        """
        return self.__id

    # service layer associated mimeTypesOutIn
    @property
    def mimeTypesOutIn(self) -> dict:
        """Gets the mimeTypesOutIn used for Isogeo filters of this ServiceOperation.

        :return: The mimeTypesOutIn of this ServiceOperation.
        :rtype: dict
        """
        return self._mimeTypesOutIn

    @mimeTypesOutIn.setter
    def mimeTypesOutIn(self, mimeTypesOutIn: dict):
        """Sets the mimeTypesOutIn used into Isogeo filters of this ServiceOperation.

        :param dict mimeTypesOutIn: the mimeTypesOutIn of this ServiceOperation.
        """

        self._mimeTypesOutIn = mimeTypesOutIn

    # mimeTypesOut
    @property
    def mimeTypesOut(self) -> str:
        """Gets the mimeTypesOut of this ServiceOperation.

        :return: The mimeTypesOut of this ServiceOperation.
        :rtype: str
        """
        return self._mimeTypesOut

    @mimeTypesOut.setter
    def mimeTypesOut(self, mimeTypesOut: str):
        """Sets the mimeTypesOut of this ServiceOperation.

        :param str mimeTypesOut: The mimeTypesOut of this ServiceOperation.
        """

        self._mimeTypesOut = mimeTypesOut

    # service layer name
    @property
    def name(self) -> str:
        """Gets the name used for Isogeo filters of this ServiceOperation.

        :return: The name of this ServiceOperation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name used into Isogeo filters of this ServiceOperation.

        :param str name: the name of this ServiceOperation.
        """

        self._name = name

    # verb
    @property
    def verb(self) -> list:
        """Gets the verb of this ServiceOperation.

        :return: The verb of this ServiceOperation.
        :rtype: list
        """
        return self._verb

    @verb.setter
    def verb(self, verb: list):
        """Sets the verb of this ServiceOperation.

        :param list verb: The verb of this ServiceOperation.
        """

        self._verb = verb

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
        if issubclass(ServiceOperation, dict):
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
        if issubclass(ServiceOperation, dict):
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
        if not isinstance(other, ServiceOperation):
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
    test_model = ServiceOperation()
    print(test_model.__dict__)
    print(test_model._id)
    print(test_model.__dict__.get("_id"))
    print(hasattr(test_model, "_id"))
    print(test_model.to_dict_creation())
    # print(test_model.to_str()
