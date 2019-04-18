# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of Contact entity

    See: http://help.isogeo.com/api/tech/#definition-contact
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint


# #############################################################################
# ########## Classes ###############
# ##################################
class Contact(object):
    """Contacts are entities used into Isogeo adress book that
    can be associated to metadata.
    """

    """
    Attributes:
      attr_types (dict): The key is attribute name
                            and the value is attribute type.
      attr_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    attr_types = {
        "_created": "datetime",
        "_id": "str",
        "address_line1": "str",
        "address_line2": "str",
        "address_line3": "str",
        "available": "str",
        "city": "str",
        "country_code": "str",
        "email": "str",
        "fax": "str",
        "hash": "str",
        "modified": "datetime",
        "name": "str",
        "organization": "str",
        "phone": "str",
        "type": "str",
        "zip_code": "str",
    }

    attr_map = {
        "created": "_created",
        "id": "_id",
        "modified": "_modified",
        "address_line1": "addressLine1",
        "address_line2": "addressLine2",
        "address_line3": "addressLine3",
        "available": "available",
        "city": "city",
        "country_code": "countryCode",
        "email": "email",
        "fax": "fax",
        "hash": "hash",
        "name": "name",
        "organization": "organization",
        "phone": "phone",
        "type": "type",
        "zip_code": "zipCode",
    }

    def __init__(
        self,
        _abilities: list = None,
        _deleted: bool = None,
        _id: str = None,
        _tag: str = None,
        addressLine1: str = None,
        addressLine2: str = None,
        addressLine3: str = None,
        available: bool = None,
        city: str = None,
        count: int = None,
        countryCode: str = None,
        email: str = None,
        fax: str = None,
        name: str = None,
        organization: str = None,
        owner: dict = None,
        phone: str = None,
        type: str = None,
        zipCode: str = None,
        # swaggered
        created=None,
        modified=None,
        hash=None,
    ):
        """Contact model"""

        self._created = None
        self._modified = None
        self._address_line1 = None
        self._address_line2 = None
        self._address_line3 = None
        self._available = None
        self._city = None
        self._country_code = None
        self._email = None
        self._fax = None
        self._id = None
        self._hash = None
        self._name = None
        self._organization = None
        self._phone = None
        self._type = None
        self._zip_code = None
        self.discriminator = None

        if created is not None:
            self.created = created
        if _id is not None:
            self._id = _id
        if modified is not None:
            self.modified = modified
        if addressLine1 is not None:
            self.address_line1 = addressLine1
        if addressLine2 is not None:
            self.address_line2 = addressLine2
        if addressLine3 is not None:
            self.address_line3 = addressLine3
        if available is not None:
            self.available = available
        if city is not None:
            self.city = city
        if countryCode is not None:
            self.country_code = countryCode
        if email is not None:
            self.email = email
        if fax is not None:
            self.fax = fax
        if hash is not None:
            self.hash = hash
        if name is not None:
            self.name = name
        if organization is not None:
            self.organization = organization
        if phone is not None:
            self.phone = phone
        if type is not None:
            self.type = type
        if zipCode is not None:
            self.zip_code = zipCode

    @property
    def created(self):
        """Gets the created of this Contact.


        :return: The created of this Contact.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Contact.


        :param created: The created of this Contact.
        :type: datetime
        """

        self._created = created

    @property
    def _id(self):
        """Gets the _id of this Contact.


        :return: The _id of this Contact.
        :rtype: str
        """
        return self._id

    @_id.setter
    def _id(self, _id):
        """Sets the _id of this Contact.


        :param _id: The _id of this Contact.
        :type: str
        """

        self._id = _id

    @property
    def modified(self):
        """Gets the modified of this Contact.


        :return: The modified of this Contact.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this Contact.


        :param modified: The modified of this Contact.
        :type: datetime
        """

        self._modified = modified

    @property
    def address_line1(self):
        """Gets the address_line1 of this Contact.


        :return: The address_line1 of this Contact.
        :rtype: str
        """
        return self._address_line1

    @address_line1.setter
    def address_line1(self, address_line1):
        """Sets the address_line1 of this Contact.


        :param address_line1: The address_line1 of this Contact.
        :type: str
        """

        self._address_line1 = address_line1

    @property
    def address_line2(self):
        """Gets the address_line2 of this Contact.


        :return: The address_line2 of this Contact.
        :rtype: str
        """
        return self._address_line2

    @address_line2.setter
    def address_line2(self, address_line2):
        """Sets the address_line2 of this Contact.


        :param address_line2: The address_line2 of this Contact.
        :type: str
        """

        self._address_line2 = address_line2

    @property
    def address_line3(self):
        """Gets the address_line3 of this Contact.


        :return: The address_line3 of this Contact.
        :rtype: str
        """
        return self._address_line3

    @address_line3.setter
    def address_line3(self, address_line3):
        """Sets the address_line3 of this Contact.


        :param address_line3: The address_line3 of this Contact.
        :type: str
        """

        self._address_line3 = address_line3

    @property
    def available(self):
        """Gets the available of this Contact.


        :return: The available of this Contact.
        :rtype: str
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this Contact.


        :param available: The available of this Contact.
        :type: str
        """

        self._available = available

    @property
    def city(self):
        """Gets the city of this Contact.


        :return: The city of this Contact.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this Contact.


        :param city: The city of this Contact.
        :type: str
        """

        self._city = city

    @property
    def country_code(self):
        """Gets the country_code of this Contact.


        :return: The country_code of this Contact.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """Sets the country_code of this Contact.


        :param country_code: The country_code of this Contact.
        :type: str
        """

        self._country_code = country_code

    @property
    def email(self):
        """Gets the email of this Contact.


        :return: The email of this Contact.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this Contact.


        :param email: The email of this Contact.
        :type: str
        """

        self._email = email

    @property
    def fax(self):
        """Gets the fax of this Contact.


        :return: The fax of this Contact.
        :rtype: str
        """
        return self._fax

    @fax.setter
    def fax(self, fax):
        """Sets the fax of this Contact.


        :param fax: The fax of this Contact.
        :type: str
        """

        self._fax = fax

    @property
    def hash(self):
        """Gets the hash of this Contact.


        :return: The hash of this Contact.
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this Contact.


        :param hash: The hash of this Contact.
        :type: str
        """

        self._hash = hash

    @property
    def name(self):
        """Gets the name of this Contact.


        :return: The name of this Contact.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Contact.


        :param name: The name of this Contact.
        :type: str
        """

        self._name = name

    @property
    def organization(self):
        """Gets the organization of this Contact.


        :return: The organization of this Contact.
        :rtype: str
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this Contact.


        :param organization: The organization of this Contact.
        :type: str
        """

        self._organization = organization

    @property
    def phone(self):
        """Gets the phone of this Contact.


        :return: The phone of this Contact.
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this Contact.


        :param phone: The phone of this Contact.
        :type: str
        """

        self._phone = phone

    @property
    def type(self):
        """Gets the type of this Contact.


        :return: The type of this Contact.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Contact.


        :param type: The type of this Contact.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")
        allowed_values = ["custom", "group", "user"]
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}".format(
                    type, allowed_values
                )
            )

        self._type = type

    @property
    def zip_code(self):
        """Gets the zip_code of this Contact.


        :return: The zip_code of this Contact.
        :rtype: str
        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, zip_code):
        """Sets the zip_code of this Contact.


        :param zip_code: The zip_code of this Contact.
        :type: str
        """

        self._zip_code = zip_code

    def to_dict(self):
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
        if issubclass(Contact, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Contact):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    ct = Contact()
    print(dir(ct))
