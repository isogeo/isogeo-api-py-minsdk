# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# -----------------------------------------------------------------------------
# Name:         DataGouvFR
# Purpose:      Abstraction class to manipulate data.gouv.fr API
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      22/04/2017
# Updated:      10/05/2017
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from sys import platform as opersys

# 3rd party library
import requests

# #############################################################################
# ########## Classes ###############
# ##################################


class DataGouvFr(object):
    """Use DataGouvFR REST API.

    Full doc at (French): https://www.data.gouv.fr/fr/apidoc/
    """
    base_url = "https://www.data.gouv.fr/api/1/"

    def __init__(self, api_key=environ.get("DATAGOUV_API_KEY", None)):
        """
        """
        super(DataGouvFr, self).__init__()
        if api_key:
            print("youhou")
            self.api_key = api_key
        else:
            raise ValueError

    def org_datasets(self, org_id="isogeo", page_size=25, x_fields=None):
        """"""
        # handling request parameters
        # payload = {'org': org_id,
        #            'size': page_size,
        #            'X-Fields': x_fields,
        #            }

        # search request
        # head = {"X-API-KEY": self.api_key}
        search_url = "{}organizations/{}/datasets/?size={}"\
                     .format(self.base_url,
                             org_id,
                             page_size
                             )

        search_req = requests.get(search_url,
                                  # headers=head,
                                  # params=payload
                                  )

        # serializing result into dict and storing resources in variables
        return search_req.json()

# ##############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == '__main__':
    """ standalone execution """
    api_key = environ.get("DATAGOUV_API_KEY")
    app = DataGouvFr()
    org_ds = app.org_datasets()
    print(len(org_ds), sorted(org_ds[0].keys()))
