# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Enums for Resource entity accepted kinds

    See: http://help.isogeo.com/api/complete/index.html#definition-application
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
from enum import Enum, auto


# #############################################################################
# ########## Classes ###############
# ##################################
class ApplicationKinds(Enum):
    """Closed list of accepted Application (metadata subresource) kinds in Isogeo API.

    :Example:

        >>> # parse members and values
        >>> print("{0:<30} {1:>20}".format("Enum", "Value"))
        >>> for md_kind in ApplicationKinds:
        >>>     print("{0:<30} {1:>20}".format(md_kind, md_kind.value))
        Enum                                          Value
        ApplicationKinds.group                            1
        ApplicationKinds.user                             2

        >>> # check if a var is an accepted value
        >>> print("group" in ApplicationKinds.__members__)
        True
        >>> print("User" in ApplicationKinds.__members__)  # case sensitive
        False
        >>> print("confidential" in ApplicationKinds.__members__)
        False

    See: https://docs.python.org/3/library/enum.html
    """

    group = auto()
    user = auto()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    print("{0:<30} {1:>20}".format("Enum", "Value"))
    for md_kind in ApplicationKinds:
        print("{0:<30} {1:>20}".format(md_kind, md_kind.value))

    print(len(ApplicationKinds))

    print("group" in ApplicationKinds.__members__)
    print("User" in ApplicationKinds.__members__)
    print("confidential" in ApplicationKinds.__members__)
