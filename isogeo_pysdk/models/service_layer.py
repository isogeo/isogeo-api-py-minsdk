# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""
    Isogeo API v1 - Model of ServiceLayer entity

    See: http://help.isogeo.com/api/complete/index.html#definition-serviceLayer
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint

# package
from isogeo_pysdk.enums import ServiceLayerTypes


# #############################################################################
# ########## Classes ###############
# ##################################
class ServiceLayer(object):
    """ServiceLayers are entities defining rules of data creation.

    :Example:

    .. code-block:: json

        {
            "_id": "string (uuid)",
            "id": "string",
            "mimeTypes": [
                "string"
            ],
            "titles": [
                {
                    "lang": "string",
                    "value": "string"
                }
            ],
            "title": "string",
            "type": "string,
            "targetDataset": {
                "format": string,
                "name": string
            }
        }
    """

    ATTR_TYPES = {
        "_id": str,
        "dataset": dict,
        "datasets": list,
        "noGeoDatasets": list,
        "name": str,
        "mimeTypes": str,
        "parentUid": str,
        "targetDataset": dict,
        "titles": list,
        "title": str,
        "type": str,
    }

    ATTR_CREA = {
        "name": str,
        "parentUid": str,
        "targetDataset": dict,
        "titles": list,
        "title": str,
        "type": str
    }

    ATTR_MAP = {"name": "id"}

    def __init__(
        self,
        _id: str = None,
        dataset: dict = None,
        datasets: list = None,
        noGeoDatasets: list = None,
        id: str = None,
        name: str = None,  # = id in API model but it's a reserved keyword in Python
        parentUid: str = None,
        mimeTypes: str = None,
        targetDataset: dict = None,  # only used with POST to indentify dataset metadata to associated the layer with
        titles: list = None,
        title: str = None,
        type: str = None,
        # additional parameters
        parent_resource: str = None,
    ):
        """ServiceLayer model."""

        # default values for the object attributes/properties
        self.__id = None
        self._dataset = None
        self._datasets = None
        self._noGeoDatasets = None
        self._name = None
        self._mimeTypes = None
        self._parentUid = None
        self._targetDataset = None
        self._titles = None
        self._title = None
        self._type = None
        # additional parameters
        self.parent_resource = parent_resource

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _id is not None:
            self.__id = _id
        if id is not None:
            self._name = id
        if dataset is not None:
            self._dataset = dataset
        if datasets is not None:
            self._datasets = datasets
        if noGeoDatasets is not None:
            self._noGeoDatasets = noGeoDatasets
        if name is not None:
            self._name = name
        if mimeTypes is not None:
            self._mimeTypes = mimeTypes
        if parentUid is not None:
            self._parentUid = parentUid
        if targetDataset is not None:
            self._targetDataset = targetDataset
        if titles is not None:
            self._titles = titles
        if title is not None:
            self._title = title
        if type is not None:
            self._type = type
        # additional parameters
        if parent_resource is not None:
            self._parent_resource = parent_resource

    # -- PROPERTIES --------------------------------------------------------------------
    # service layer UUID
    @property
    def _id(self) -> str:
        """Gets the id of this ServiceLayer.

        :return: The id of this ServiceLayer.
        :rtype: str
        """
        return self.__id

    # service layer associated dataset
    @property
    def dataset(self) -> dict:
        """Gets the dataset used for Isogeo filters of this ServiceLayer.

        :return: The dataset of this ServiceLayer.
        :rtype: dict
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: dict):
        """Sets the dataset used into Isogeo filters of this ServiceLayer.

        :param dict dataset: the dataset of this ServiceLayer.
        """

        self._dataset = dataset

    # service layer associated datasets
    @property
    def datasets(self) -> list:
        """Gets the datasets used for Isogeo filters of this ServiceLayer.

        :return: The datasets of this ServiceLayer.
        :rtype: list
        """
        return self._datasets

    @datasets.setter
    def datasets(self, datasets: list):
        """Sets the datasets used into Isogeo filters of this ServiceLayer.

        :param list datasets: the datasets of this ServiceLayer.
        """

        self._datasets = datasets

    # service layer associated no geo datasets
    @property
    def noGeoDatasets(self) -> list:
        """Gets the noGeoDatasets used for Isogeo filters of this ServiceLayer.

        :return: The noGeoDatasets of this ServiceLayer.
        :rtype: list
        """
        return self._noGeoDatasets

    @noGeoDatasets.setter
    def noGeoDatasets(self, noGeoDatasets: list):
        """Sets the noGeoDatasets used into Isogeo filters of this ServiceLayer.

        :param list noGeoDatasets: the noGeoDatasets of this ServiceLayer.
        """

        self._noGeoDatasets = noGeoDatasets

    # service layer name
    @property
    def name(self) -> str:
        """Gets the name used for Isogeo filters of this ServiceLayer.

        :return: The name of this ServiceLayer.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name used into Isogeo filters of this ServiceLayer.

        :param str name: the name of this ServiceLayer.
        """

        self._name = name

    # mimeTypes
    @property
    def mimeTypes(self) -> str:
        """Gets the mimeTypes of this ServiceLayer.

        :return: The mimeTypes of this ServiceLayer.
        :rtype: str
        """
        return self._mimeTypes

    @mimeTypes.setter
    def mimeTypes(self, mimeTypes: str):
        """Sets the mimeTypes of this ServiceLayer.

        :param str mimeTypes: The mimeTypes of this ServiceLayer.
        """

        self._mimeTypes = mimeTypes

    # parentUid
    @property
    def parentUid(self) -> str:
        """Gets the parentUid of this ServiceLayer.

        :return: The parentUid of this ServiceLayer.
        :rtype: str
        """
        return self._parentUid

    @parentUid.setter
    def parentUid(self, parentUid: str):
        """Sets the parentUid of this ServiceLayer.

        :param str parentUid: The parentUid of this ServiceLayer.
        """

        self._parentUid = parentUid

    # targetDataset
    @property
    def targetDataset(self) -> dict:
        """Gets the targetDataset of this ServiceLayer.

        :return: The targetDataset of this ServiceLayer.
        :rtype: dict
        """
        return self._targetDataset

    @targetDataset.setter
    def targetDataset(self, targetDataset: dict):
        """Sets the targetDataset of this ServiceLayer.

        :param dict targetDataset: The targetDataset of this ServiceLayer.
        """
        if not isinstance(targetDataset, dict):
            raise TypeError("'targetDataset' argument value must be a dict, not: {}".format(type(targetDataset)))
        elif "name" not in targetDataset:
            raise ValueError("'targetDataset' must have a key named 'name'.")
        else:
            pass
        self._targetDataset = targetDataset

    # titles
    @property
    def titles(self) -> list:
        """Gets the titles of this ServiceLayer.

        :return: The titles of this ServiceLayer.
        :rtype: list
        """
        return self._titles

    @titles.setter
    def titles(self, titles: list):
        """Sets the titles of this ServiceLayer.

        :param list titles: The titles of this ServiceLayer.
        """

        self._titles = titles

    # title
    @property
    def title(self) -> str:
        """Gets the title of this ServiceLayer.

        :return: The title of this ServiceLayer.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this ServiceLayer.

        :param str title: The title of this ServiceLayer.
        """

        self._title = title

    # type
    @property
    def type(self) -> str:
        """Gets the type of this ServiceLayer.

        :return: The type of this ServiceLayer.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this ServiceLayer.

        :param str type: The type of this ServiceLayer. Must be one of "group", "layer" or "table".
        """

        # check type value
        if type not in ServiceLayerTypes.__members__:
            raise ValueError(
                "link type '{}' is not an accepted value. Must be one of: {}.".format(
                    type, " | ".join([e.name for e in ServiceLayerTypes])
                )
            )
        else:
            pass

        self._type = type

    # -- METHODS -----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Returns the model properties as a dict."""
        result = {}

        for attr, _ in self.ATTR_TYPES.items():
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
        if issubclass(ServiceLayer, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_dict_creation(self) -> dict:
        """Returns the model properties as a dict structured for creation purpose (POST)"""
        result = {}

        for attr, _ in self.ATTR_CREA.items():
            # get attribute value
            value = getattr(self, attr)
            # switch attribute name for creation purpose
            if attr in self.ATTR_MAP:
                attr = self.ATTR_MAP.get(attr)
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
        if issubclass(ServiceLayer, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model."""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal."""
        if not isinstance(other, ServiceLayer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal."""
        return not self == other


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """standalone execution."""
    test_model = ServiceLayer()
    print(test_model.__dict__)
    print(test_model._id)
    print(test_model.__dict__.get("_id"))
    print(hasattr(test_model, "_id"))
    print(test_model.to_dict_creation())
    # print(test_model.to_str()
