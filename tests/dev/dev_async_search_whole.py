# -*- coding: UTF-8 -*-
#! python3

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import asyncio
from concurrent.futures import ThreadPoolExecutor
from os import environ
from timeit import default_timer
import urllib3

# 3rd party
from dotenv import load_dotenv

# Isogeo
from isogeo_pysdk import Isogeo, IsogeoUtils, Metadata

# #############################################################################
# ######## Globals #################
# ##################################

utils = IsogeoUtils()

# get user ID as environment variables
load_dotenv("dev.env")

# ignore warnings related to the QA self-signed cert
if environ.get("ISOGEO_PLATFORM").lower() == "qa":
    urllib3.disable_warnings()

# start Isogeo
isogeo = Isogeo(
    auth_mode="group",
    client_id=environ.get("ISOGEO_API_GROUP_CLIENT_ID"),
    client_secret=environ.get("ISOGEO_API_GROUP_CLIENT_SECRET"),
    auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
    platform=environ.get("ISOGEO_PLATFORM", "qa"),
)

# getting a token
isogeo.connect()


# #############################################################################
# ########## Functions ##############
# ##################################
def _meta_get_resource_sync(offset):
    """Just a meta func to get execution time"""
    search = isogeo.search(
        page_size=50, offset=offset, check=0, whole_results=0, include="all"
    )

    elapsed = default_timer() - START_TIME
    time_completed_at = "{:5.2f}s".format(elapsed)
    print("{0:<30} {1:>20}".format(offset, time_completed_at))

    return search


# ASYNC
async def search_metadata_asynchronous(max_workers):
    with ThreadPoolExecutor(
        max_workers=max_workers, thread_name_prefix="IsogeoSearch"
    ) as executor:
        # Set any session parameters here before calling `fetch`
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                _meta_get_resource_sync,
                # Allows us to pass in multiple arguments to `fetch`
                *(offset,),
            )
            for offset in li_paginated_search
        ]

        # store responses
        out_list = []
        for response in await asyncio.gather(*tasks):
            out_list.extend(response.results)

        return out_list


# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    page = 50
    search = isogeo.search(page_size=page, whole_results=0)
    total_shared = search.total
    total_pages = utils.pages_counter(total_shared, page_size=page)

    # create the pagination
    li_paginated_search = [offset * page for offset in range(0, total_pages)]

    # SYNCHRONOUS
    search_sync = search
    print(
        "\nSearching for {} metadata in {} pages of {} - SYNCHRONOUS".format(
            total_shared, total_pages, len(li_paginated_search)
        )
    )
    START_TIME = default_timer()
    print("{0:<30} {1:>20}".format("File", "Completed at"))
    total_start_time = default_timer()
    metadatas = []  # a recipient list
    for offset in range(0, total_pages):
        in_search = isogeo.search(
            page_size=page, offset=offset, check=0, whole_results=0, include="all"
        )
        # storing results by addition
        metadatas.extend(in_search.results)
        time_completed_at = "{:5.2f}s".format(default_timer() - START_TIME)
        print("{0:<30} {1:>20}".format(offset, time_completed_at))

    search_sync.results = metadatas
    for i in search_sync.results:
        i["coordinateSystem"] = i.pop("coordinate-system", list)
        i["featureAttributes"] = i.pop("feature-attributes", list)
        Metadata(**i)

    elapsed = default_timer() - total_start_time
    time_completed_at = "{:5.2f}s".format(elapsed)
    print("SYNCHRONOUS - TOTAL ELAPSED TIME: " + time_completed_at)

    # check results structure
    for i in search_sync.results:
        i["coordinateSystem"] = i.pop("coordinate-system", list)
        i["featureAttributes"] = i.pop("feature-attributes", list)
        Metadata(**i)

    # ASYNC
    search_async = search
    print(
        "\nSearching for {} metadata in {} pages of {} - ASYNCHRONOUS".format(
            total_shared, total_pages, page
        )
    )
    START_TIME = default_timer()
    print("{0:<30} {1:>20}".format("Offset", "Completed at"))
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(search_metadata_asynchronous(total_pages))
    loop.run_until_complete(future)

    elapsed = default_timer() - START_TIME
    time_completed_at = "{:5.2f}s".format(elapsed)
    print("{} metadatas retrieved.".format(len(future.result())))
    print("ASYNCHRONOUS - TOTAL ELAPSED TIME: " + time_completed_at)

    # check results structure
    search_async.results = future.result()
    for i in search_async.results:
        i["coordinateSystem"] = i.pop("coordinate-system", list)
        i["featureAttributes"] = i.pop("feature-attributes", list)
        Metadata(**i)
