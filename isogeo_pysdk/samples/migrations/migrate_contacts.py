# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    python -m migrate_contacts
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import (
    IsogeoSession,
    __version__ as pysdk_version,
    Catalog,
    Contact,
    License,
    Specification,
    Workgroup,
)


# #############################################################################
# ######## Globals #################
# ##################################

# environment vars
load_dotenv("dev.env", override=True)

# -- SOURCE PARAMS
src_group = ""
src_platform = "qa"

# -- DESTINATION PARAMS
dst_group = ""
dst_platform = "qa"

# #############################################################################
# ########## Main program ###############
# #######################################

# -- GET GROUP FROM SOURCE --------

# Isogeo client
src_isogeo = IsogeoSession(
    client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
    client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
    auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
    platform=environ.get("ISOGEO_PLATFORM", "qa"),
)

# getting a token
src_isogeo.connect(
    username=environ.get("ISOGEO_USER_NAME"),
    password=environ.get("ISOGEO_USER_PASSWORD"),
)

# duplicate group
# src_group = Workgroup(**src_isogeo.workgroup(workgroup_id=src_group))

# store catalogs
# src_catalogs = src_isogeo.workgroup_catalogs(workgroup_id=src_group)

# store contacts
# src_contacts = src_isogeo.workgroup_listing(workgroup_id=src_group)

# store licenses
src_licenses = src_isogeo.workgroup_listing(workgroup_id=src_group)

# store specifications
# src_specifications = src_isogeo.workgroup_listing(workgroup_id=src_group)

# close source connection
src_isogeo.close()

# -- INSERT DATA INTO DESTINATION GROUP --------

# Isogeo client
dst_isogeo = IsogeoSession(
    client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
    client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
    auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
    platform=environ.get("ISOGEO_PLATFORM", "qa"),
)

# getting a token
dst_isogeo.connect(
    username=environ.get("ISOGEO_USER_NAME"),
    password=environ.get("ISOGEO_USER_PASSWORD"),
)

# insert catalog
# for cat in src_catalogs:
#     cat_to_create = Catalog(**cat)
#     dst_isogeo.catalog_create(workgroup_id=dst_group, catalog=cat_to_create)

# # insert contacts
# for ct in src_contacts:
#     ct_to_create = Contact(**ct)
#     dst_isogeo.create(workgroup_id=dst_group, contact=ct_to_create)

# # insert specifications
# for spec in src_specifications:
#     spec_to_create = Specification(**spec)
#     dst_isogeo.specification_create(workgroup_id=dst_group, specification=spec_to_create)

# insert licenses
# for lic in src_licenses:
#     lic_to_create = License(**lic)
#     dst_isogeo.license_create(workgroup_id=dst_group, license=lic_to_create)

# close connections
dst_isogeo.close()

# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    pass
