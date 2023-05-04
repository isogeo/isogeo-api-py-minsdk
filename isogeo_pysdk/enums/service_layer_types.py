# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""
    Isogeo API v1 - Enums for Links types

    See: http://help.isogeo.com/api/complete/index.html#definition-resourceLink
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
from enum import Enum, auto


# #############################################################################
# ########## Classes ###############
# ##################################
class ServiceLayerTypes(Enum):
    """Closed list of accepted Link types in Isogeo API.

    :Example:

        >>> # parse members and values
        >>> print("{0:<30} {1:>20}".format("Enum", "Value"))
        >>> for i in ServiceLayerTypes:
        >>>     print("{0:<30} {1:>20}".format(i, i.value))
        Enum                                          Value
        ServiceLayerTypes.group                                   1
        ServiceLayerTypes.layer                                   2
        ServiceLayerTypes.table                                   3

        >>> # check if a var is an accepted value
        >>> print("hosted" in ServiceLayerTypes.__members__)
        False
        >>> print("Group" in ServiceLayerTypes.__members__)  # case sensitive
        False
        >>> print("group" in ServiceLayerTypes.__members__)
        True

    See: https://docs.python.org/3/library/enum.html
    """

    group = auto()
    layer = auto()
    table = auto()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """standalone execution."""
    print("{0:<30} {1:>20}".format("Enum", "Value"))
    for i in ServiceLayerTypes:
        print("{0:<30} {1:>20}".format(i, i.value))

    print(len(ServiceLayerTypes))

    print("hosted" in ServiceLayerTypes.__members__)
    print("Group" in ServiceLayerTypes.__members__)
    print("group" in ServiceLayerTypes.__members__)
