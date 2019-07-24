# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of Catalog entity

    See: http://help.isogeo.com/api/complete/index.html#definition-catalog
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint

# other model
from isogeo_pysdk.models.workgroup import Workgroup


# #############################################################################
# ########## Classes ###############
# ##################################
class Catalog(object):
    """Catalogs are entities used to organize and shares metadata of a workgroup.


    Sample:

    ```json
    {
        '$scan': False,
        '_abilities': ['catalog:share'],
        '_created': '2018-04-16T08:19:52.7008403+00:00',
        '_id': 'aba3020305f04babaefe8c0719a612b3',
        '_modified': '2018-10-08T12:53:30.4629329+00:00',
        '_tag': 'catalog:aba3020305f04babaefe8c0719a612b3',
        'code': 'new',
        'count': 44,
        'name': '_Démonstration',
        'owner': {
            '_created': '2014-04-18T16:23:38.617093+00:00',
            '_id': '08b3054757544463abd06f3ab51ee491',
            '_modified': '2018-11-29T07:37:22.0319922+00:00',
            '_tag': 'owner:08b3054757544463abd06f3ab51ee491',
            'areKeywordsRestricted': False,
            'canCreateLegacyServiceLinks': True,
            'canCreateMetadata': True,
            'contact': {
                '_deleted': False,
                '_id': '80aabc302fe946c8a51fffe22d60eb77',
                '_tag': 'contact:group:80aabc302fe946c8a51fffe22d60eb77',
                'addressLine1': '26 rue du faubourg Saint-Antoine',
                'addressLine2': '4ème étage',
                'available': False,
                'city': 'Paris',
                'countryCode': 'FR',
                'email': 'contact@isogeo.com',
                'fax': '+33 9 81 40 00 66',
                'name': 'Isogeo Demo',
                'phone': '+33 9 67 46 50 06',
                'type': 'group',
                'zipCode': '75012'
                },
            'hasCswClient': False,
            'hasScanFme': True,
            'keywordsCasing': 'lowercase',
            'metadataLanguage': 'fr'
            }
    }
    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of catalog attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
    """
    attr_types = {
        "_abilities": list,
        "_created": str,
        "_id": str,
        "_modified": str,
        "_tag": str,
        "code": str,
        "count": int,
        "name": str,
        "owner": Workgroup,
        "scan": bool,
    }

    attr_crea = {"code": str, "name": str, "scan": bool}

    attr_map = {"scan": "$scan"}

    def __init__(
        self,
        _abilities: list = None,
        _created: str = None,
        _id: str = None,
        _modified: str = None,
        _tag: str = None,
        code: str = None,
        count: int = None,
        name: str = None,
        owner: Workgroup = None,
        scan: bool = None,
    ):
        """Catalog model"""

        # default values for the object attributes/properties
        self.__abilities = None
        self.__created = None
        self.__id = None
        self.__modified = None
        self.__tag = None
        self._code = None
        self._count = None
        self._name = None
        self._owner = (None,)
        self._scan = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _abilities is not None:
            self.__abilities = _abilities
        if _created is not None:
            self.__created = _created
        if _id is not None:
            self.__id = _id
        if _modified is not None:
            self.__modified = _modified
        if _tag is not None:
            self.__tag = _tag
        if code is not None:
            self._code = code
        if count is not None:
            self._count = count
        if name is not None:
            self._name = name
        if scan is not None:
            self._scan = scan

        # required
        self._owner = owner

    # -- PROPERTIES --------------------------------------------------------------------
    # catalog abilities
    @property
    def _abilities(self) -> str:
        """Gets the abilities of this Catalog.

        :return: The abilities of this Catalog.
        :rtype: str
        """
        return self.__abilities

    # catalog creation date
    @property
    def _created(self) -> str:
        """Gets the created of this Catalog.

        :return: The created of this Catalog.
        :rtype: str
        """
        return self.__created

    # catalog UUID
    @property
    def _id(self) -> str:
        """Gets the id of this Catalog.

        :return: The id of this Catalog.
        :rtype: str
        """
        return self.__id

    @_id.setter
    def _id(self, _id: str):
        """Sets the id of this Catalog.

        :param str id: The id of this Catalog.
        """

        self.__id = _id

    # catalog last modification date
    @property
    def _modified(self) -> str:
        """Gets the modified of this Catalog.

        :return: The modified of this Catalog.
        :rtype: str
        """
        return self.__modified

    # catalog tag for search
    @property
    def _tag(self) -> str:
        """Gets the tag of this Catalog.

        :return: The tag of this Catalog.
        :rtype: str
        """
        return self.__tag

    # code
    @property
    def code(self) -> str:
        """Gets the code of this Catalog.

        :return: The code of this Catalog.
        :rtype: str
        """
        return self._code

    # name
    @property
    def name(self) -> str:
        """Gets the name of this Catalog.

        :return: The name of this Catalog.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Catalog.

        :param str name: The name of this Catalog.
        """

        self._name = name

    # count
    @property
    def count(self) -> str:
        """Gets the count of this Catalog.

        :return: The count of this Catalog.
        :rtype: str
        """
        return self._count

    @count.setter
    def count(self, count: str):
        """Sets the count of this Catalog.

        :param str count: The count of this Catalog.
        """

        self._count = count

    @property
    def owner(self):
        """Gets the owner of this Catalog.  # noqa: E501


        :return: The owner of this Catalog.  # noqa: E501
        :rtype: Workgroup
        """
        return self._owner

    # scan
    @property
    def scan(self) -> bool:
        """Gets the scan of this Catalog.

        :return: The scan of this Catalog.
        :rtype: bool
        """
        return self._scan

    @scan.setter
    def scan(self, scan: bool):
        """Sets the scan of this Catalog.

        :param bool scan: The scan of this Catalog. Must be one of GROUP_KIND_VALUES
        """

        self._scan = scan

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
        if issubclass(Catalog, dict):
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
            # process value depending on attr type
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
        if issubclass(Catalog, dict):
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
        if not isinstance(other, Catalog):
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
    cat = Catalog(name="youpi", scan=1)
    to_crea = cat.to_dict_creation()
    print(type(to_crea.get("IsScanSink")))
