# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of Link entity

    See: http://help.isogeo.com/api/complete/index.html#definition-link
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint


# #############################################################################
# ########## Classes ###############
# ##################################
class Link(object):
    """Links are entities included as subresource into metadata for data history title.


    Sample:

    ```json
    {
        '_id': 'c693334b947445bd891d11ad227fbfab',
        'actions': ['view', 'download'],
        'kind': 'wfs',
        'parent_resource': '1d3b9f4ea78443489d47dfb505a0605f',
        'title': 'WFS - PUBLIC SSL - Externe (sans JSONP) - Visualisation et téléchargement lycées aquitains',
        'type': 'url',
        'url': 'https://www.pigma.org/geoserver/ows?typeName=craquitaine:craquitaine_lycees'
    }
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of link attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
      attr_
      LINK_KINDS_VALUES (tuple): possible values for an link kind
    """
    attr_types = {
        "_id": str,
        "actions": list,
        "kind": str,
        "title": str,
        "type": str,
        "parent_resource": str,
        "url": str
    }

    attr_crea = {
        "actions": list,
        "kind": str,
        "title": str,
        "type": str,
        "parent_resource": str,
        "url": str,
        "waitForSync": bool
    }

    attr_map = {
    }

    # possible values for link 'action' attribute
    LINK_ACTIONS_VALUES = (
        "download",
        "other",
        "view",
    )
    # possible values for link 'kind' attribute
    LINK_KINDS_VALUES = (
        "data",
        "esriFeatureService",
        "esriMapService",
        "esriTileService",
        "url",
        "wfs",
        "wms",
        "wmts"
    )

    # possible values for link 'type' attribute
    LINK_TYPESS_VALUES = (
        "hosted",
        "link",
        "url",
    )

    def __init__(
        self,
        _id: str = None,
        actions: list = None,
        kind: str = None,
        title: str = None,
        type: str = None,
        url: str = None,
        # implementation additional parameters
        parent_resource: str = None,
        waitForSync: bool = 1
    ):
        """Link model"""

        # default values for the object attributes/properties
        self.__id = None
        self._actions = None
        self._kind = None
        self._title = None
        self._type = None
        self._url = None
        # additional parameters
        self.parent_resource = parent_resource
        self.waitForSync = waitForSync

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _id is not None:
            self.__id = _id
        if actions is not None:
            self._actions = actions
        if kind is not None:
            self._kind = kind
        if title is not None:
            self._title = title
        if type is not None:
            self._type = type
        if url is not None:
            self._url = url

    # -- PROPERTIES --------------------------------------------------------------------
    # link UUID
    @property
    def _id(self) -> str:
        """Gets the id of this Link.

        :return: The id of this Link.
        :rtype: str
        """
        return self.__id

    @_id.setter
    def _id(self, _id: str):
        """Sets the id of this Link.

        :param str id: The id of this Link.
        """

        self.__id = _id

    # actions
    @property
    def actions(self) -> str:
        """Gets the actions of this Link.

        :return: The actions of this Link.
        :rtype: str
        """
        return self._actions

    @actions.setter
    def actions(self, actions: str):
        """Sets the actions of this Link.

        :param str actions: The actions of this Link.
        """

        self._actions = actions

    # title
    @property
    def title(self) -> str:
        """Gets the title of this Link.

        :return: The title of this Link.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Link.

        :param str title: The title of this Link.
        """

        self._title = title

    # kind
    @property
    def kind(self) -> str:
        """Gets the kind of this Link.

        :return: The kind of this Link.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind: str):
        """Sets the kind of this Link.

        :param str kind: The kind of this Link. Must be one of LINK_KIND_VALUES
        """

        self._kind = kind

    # type
    @property
    def type(self) -> str:
        """Gets the type of this Link.

        :return: The type of this Link.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Link.

        :param str type: The type of this Link. Must be one of LINK_KIND_VALUES
        """

        self._type = type

    # url
    @property
    def url(self) -> str:
        """Gets the url of this Link.

        :return: The url of this Link.
        :rurl: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this Link.

        :param str url: The url of this Link. Must be one of LINK_KIND_VALUES
        """

        self._url = url

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
        if issubclass(Link, dict):
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
        if issubclass(Link, dict):
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
        if not isinstance(other, Link):
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
    obj = Link()