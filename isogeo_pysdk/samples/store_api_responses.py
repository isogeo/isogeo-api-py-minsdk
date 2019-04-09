# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Batch export to XML ISO19139
# Purpose:      Exports each of 10 last updated metadata into an XML ISO19139
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      14/11/2016
# Updated:      21/04/2017
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
from os import environ

# Isogeo
from isogeo_pysdk import Isogeo

# ############################################################################
# ######### Main program ###########
# ##################################

if __name__ == "__main__":
    """Standalone execution"""
    share_id = environ.get("ISOGEO_API_DEV_ID")
    share_token = environ.get("ISOGEO_API_DEV_SECRET")

    # instanciating the class
    isogeo = Isogeo(client_id=share_id, client_secret=share_token)

    token = isogeo.connect()

    # ------------ REAL START ------------------------------------------------

    # # empty search
    # request = isogeo.search(token, page_size=0, whole_share=0, augment=1)
    # with open("out_api_search_empty.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )

    # share_id = list(isogeo.shares_id.keys())[0].split(":")[1]
    # share_augmented = isogeo.share(token, share_id, augment=1)

    request = isogeo.resource(
        token=token, resource_id="43380f6c60424095b67cbd1aa9526fe4", include="all"
    )
    with open("out_api_resource_complete.json", "w") as json_basic:
        json.dump(request, json_basic, sort_keys=True, indent=4)

    # #print(share_augmented)

    # shares = isogeo.shares(token)

    # # get first share id
    # share_id = shares[0].get("_id")
    # share_augmented = isogeo.share(token, share_id, augment=1)
    # if "oc_url" in share_augmented:
    #     print("OpenCatalog is set: {}"
    #           .format(share_augmented.get("oc_url"))
    #           )
    # else:
    #     print("OpenCatalog is not set in this share")

    # print("1465dd29fb074cb0b53ba8b7898396b3" in share_augmented.get("mds_ids"))

    # # basic search
    # request = isogeo.search(token, page_size=10, whole_share=0)
    # with open("out_api_search_basic.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )

    # # complete search
    # request = isogeo.search(token, whole_share=1, include="all")
    # with open("out_api_search_complete.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )

    # # shares informations
    # request = isogeo.shares(token)
    # with open("out_api_shares.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )

    # share_id = request[0].get("_id")
    # request = isogeo.share(token, share_id, augment=1)
    # with open("out_api_share.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )

    # # Thesauri
    # request = isogeo.thesauri(token)
    # with open("out_api_thesauri.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )

    # thez_id = request[0].get("_id")
    # request = isogeo.thesaurus(token, thez_id)
    # with open("out_api_thesaurus.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )

    # Link kinds
    # request = isogeo.get_link_kinds(token)
    # with open("out_api_link_kinds.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #              """  )

    # # Environment directives
    # request = isogeo.get_directives(token)
    # with open("out_api_environment_directives.json", "w") as json_basic:
    #     json.dump(request,
    #               json_basic,
    #               sort_keys=True,
    #               indent=4,
    #               )
