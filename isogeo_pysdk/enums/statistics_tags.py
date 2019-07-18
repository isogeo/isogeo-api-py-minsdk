# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Enums for Workgroup statistics entity accepted tags

    See: http://help.isogeo.com/api/complete/index.html#operation--groups--gid--statistics-tag--tag--get
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
from enum import Enum


# #############################################################################
# ########## Classes ###############
# ##################################
class StatisticsTags(Enum):
    """Closed list of accepted tags for workgroup statistics in Isogeo API (used by the dashboard).

    :Example:

        >>> # parse members and values
        >>> print("{0:<30} {1:>20}".format("Enum", "Value"))
        >>> for tag in StatisticsTags:
        >>>     print("{0:<30} {1:>20}".format(tag, tag.value))
        Enum                                                    Value
        StatisticsTags.catalog                                catalog
        StatisticsTags.coordinateSystem             coordinate-system
        StatisticsTags.format                                  format
        StatisticsTags.inspireTheme             keyword:inspire-theme
        StatisticsTags.owner                                    owner

        >>> # check if a var is an accepted value
        >>> print("catalog" in StatisticsTags.__members__)
        True
        >>> print("Catalog" in StatisticsTags.__members__)  # case sensitive
        False
        >>> print("coordinate-system" in StatisticsTags.__members__)
        False
        >>> print("coordinateSystem" in StatisticsTags.__members__)
        True

    See: https://docs.python.org/3/library/enum.html
    """

    catalog = "catalog"
    coordinateSystem = "coordinate-system"
    format = "format"
    inspireTheme = "keyword:inspire-theme"
    keyword = "keyword"
    owner = "owner"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    print("{0:<30} {1:>30}".format("Enum", "Value"))
    for tag in StatisticsTags:
        print("{0:<30} {1:>30}".format(tag, tag.value))

    print(len(StatisticsTags))

    print("catalog" in StatisticsTags.__members__)
    print("Catalog" in StatisticsTags.__members__)
    print("coordinate-system" in StatisticsTags.__members__)
    print("coordinateSystem" in StatisticsTags.__members__)
