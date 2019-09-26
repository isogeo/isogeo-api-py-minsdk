# -*- coding: UTF-8 -*-
#! python3  # noqa E265

# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Remove custom specifications from metadatas of a workgroup
# Purpose:      useful to automatically clean workgroups
#
# Python:       3.7+
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from concurrent.futures import ThreadPoolExecutor
from os import environ
from timeit import default_timer

# 3rd party
from dotenv import load_dotenv

# Isogeo
from isogeo_pysdk import Isogeo, Metadata, Specification

# #############################################################################
# ######## Globals #################
# ##################################

# environment vars
load_dotenv("dev.env", override=True)
WG_TEST_UUID = ""


# ############################################################################
# ######## Export functions ###########
# ###########################################################################
def _meta_dissociate_specification(metadata: Metadata):
    """Meta function."""
    # parse metadata specifications
    for s in metadata.specifications:
        spec = Specification(**s.get("specification"))
        if ":isogeo:" in spec._tag:
            print(
                "Specification ignored because it's a locked one: {}".format(spec.name)
            )
        else:
            isogeo.specification.dissociate_metadata(
                metadata=metadata, specification_id=spec._id
            )
            print(
                "Specification {} removed from the metadata {}".format(
                    spec.name, metadata.title_or_name()
                )
            )


# ASYNC
def threaded_executor(li_metadatas_with_specifications: list):
    with ThreadPoolExecutor(
        max_workers=5, thread_name_prefix="IsogeoCleaningSpecifications"
    ) as executor:
        for metadata in li_metadatas_with_specifications:
            executor.submit(_meta_dissociate_specification(metadata))


# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    import urllib3

    # chronometer
    START_TIME = default_timer()

    # handle warnings
    if environ.get("ISOGEO_PLATFORM").lower() == "qa":
        urllib3.disable_warnings()

    # -- Authentication and connection ---------------------------------
    # for oAuth2 Legacy Flow
    isogeo = Isogeo(
        auth_mode="user_legacy",
        client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
        client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
        auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
        platform=environ.get("ISOGEO_PLATFORM", "qa"),
        timeout=(30, 200),
    )

    # getting a token
    isogeo.connect(
        username=environ.get("ISOGEO_USER_NAME"),
        password=environ.get("ISOGEO_USER_PASSWORD"),
    )

    # display elapsed time
    print("Authentication succeeded at {:5.2f}s".format(default_timer() - START_TIME))

    # search with specifications included
    search = isogeo.search(
        group=WG_TEST_UUID,
        query="owner:{}".format(WG_TEST_UUID),
        include=("specifications",),
        whole_results=1,
    )

    print(
        "{} metadatas owned by the workgroup {}. Retrieved at {:5.2f}s".format(
            search.total, WG_TEST_UUID, default_timer() - START_TIME
        )
    )

    # filter results
    li_metadatas_with_specs = [
        Metadata.clean_attributes(md)
        for md in search.results
        if len(md.get("specifications"))
    ]
    print(
        "{} metadatas have at leat one specification. Synchronously filtered at {:5.2f}s".format(
            len(li_metadatas_with_specs), default_timer() - START_TIME
        )
    )

    # -- Async loop --------------------------------------------------
    threaded_executor(li_metadatas_with_specs)
