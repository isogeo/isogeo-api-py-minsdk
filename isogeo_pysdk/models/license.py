# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of License entity

    See: http://help.isogeo.com/api/complete/index.html#definition-license
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint


# #############################################################################
# ########## Classes ###############
# ##################################
class License(object):
    """Licenses are entities included as subresource into metadata.


    Sample:

    ```json
    {
        '_abilities': [],
        '_id': '34f800d2370a43d2a1681eb2397b0dd3',
        '_tag': 'license:isogeo:34f800d2370a43d2a1681eb2397b0dd3',
        'link': 'http://professionnels.ign.fr/sites/default/files/cgu-mission-service-public.pdf',
        'name': 'Licence IGN - Mission de service public'
    }
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of license attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
    """

    attr_types = {
        "_id": str,
        "_tag": str,
        "content": str,
        "link": str,
        "name": str,
        "owner": dict,
    }

    attr_crea = {"content": "str", "link": "str", "name": "str"}

    attr_map = {}

    def __init__(
        self,
        _abilities: list = None,
        _id: str = None,
        _tag: str = None,
        count: str = None,
        content: str = None,
        link: str = None,
        name: str = None,
        owner: dict = None,
    ):
        """License model"""

        # default values for the object attributes/properties
        self.__id = None
        self.__tag = None
        self._content = None
        self._count = None
        self._link = None
        self._name = None
        self._owner = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _abilities is not None:
            self.__abilities = _abilities
        if _id is not None:
            self.__id = _id
        if _tag is not None:
            self.__tag = _tag
        if count is not None:
            self._count = count
        if content is not None:
            self._content = content
        if link is not None:
            self._link = link
        if name is not None:
            self._name = name
        if owner is not None:
            self.owner = owner

    # -- PROPERTIES --------------------------------------------------------------------
    # license UUID
    @property
    def _id(self) -> str:
        """Gets the id of this License.

        :return: The id of this License.
        :rtype: str
        """
        return self.__id

    @_id.setter
    def _id(self, _id: str):
        """Sets the id of this License.

        :param str id: The id of this License.
        """

        self.__id = _id

    # tag
    @property
    def _tag(self) -> str:
        """Gets the tag used for Isogeo filters of this Specification.

        :return: The tag of this Specification.
        :rtype: str
        """
        return self.__tag

    @_tag.setter
    def _tag(self, _tag: str):
        """Sets the tag used into Isogeo filters of this Specification.

        :param str _tag: the tag of this Specification.
        """

        self.__tag = _tag

    # content
    @property
    def content(self) -> str:
        """Gets the content of this License.

        :return: The content of this License.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content: str):
        """Sets the content of this License.

        :param str content: The content of this License. Accept markdown syntax.
        """

        self._content = content

    # count of resource linked to the license
    @property
    def count(self) -> int:
        """Gets the id of this License.

        :return: The id of this License.
        :rtype: str
        """
        return self._count

    @count.setter
    def count(self, count: int):
        """Sets the count of this License.

        :param int count: count of associated resources to the License
        """

        self._count = count

    # link
    @property
    def link(self) -> str:
        """Gets the link (URL) of this License.

        :return: The link (URL) of this License.
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link: str):
        """Sets the id of this License.

        :param str XX: The id of this License.
        """

        self._link = link

    # name
    @property
    def name(self) -> str:
        """Gets the name of this License.

        :return: The name of this License.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this License.

        :param str name: The name of this License. Accept markdown syntax.
        """

        self._name = name

    # workgroup owner
    @property
    def owner(self):
        """Gets the owner of this License.

        :return: The owner of this License.
        :rtype: Workgroup
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this License.


        :param owner: The owner of this License.
        :type: Workgroup
        """

        self._owner = owner

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
        if issubclass(License, dict):
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
        if issubclass(License, dict):
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
        if not isinstance(other, License):
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
    lic = License(name="License Test", content="Test license content")
    print(lic)
