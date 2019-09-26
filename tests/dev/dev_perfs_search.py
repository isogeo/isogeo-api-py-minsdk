# -*- coding: UTF-8 -*-
#! python3  # noqa E265

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import urllib3

from os import environ
from timeit import default_timer

# 3rd party
from dotenv import load_dotenv

# Isogeo
from isogeo_pysdk import Isogeo

# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":

    # logs
    logger = logging.getLogger(__name__)
    logging.captureWarnings(True)
    logger.setLevel(logging.DEBUG)

    # get user ID as environment variables
    load_dotenv("dev.env")

    # ignore warnings related to the QA self-signed cert
    if environ.get("ISOGEO_PLATFORM").lower() == "qa":
        urllib3.disable_warnings()

    # instanciate
    isogeo = Isogeo(
        client_id=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_ID"),
        client_secret=environ.get("ISOGEO_API_USER_LEGACY_CLIENT_SECRET"),
        auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
        platform=environ.get("ISOGEO_PLATFORM", "qa"),
    )

    # getting a token
    isogeo.connect(
        username=environ.get("ISOGEO_USER_NAME"),
        password=environ.get("ISOGEO_USER_PASSWORD"),
    )

    START_TIME = default_timer()

    # without stream
    START_TIME = default_timer()
    isogeo.get("https://v1.api.qa.isogeo.com/resources/search?_limit=0", verify=False)
    elapsed_nostream = default_timer() - START_TIME
    print("Without stream: {:5.2f}s".format(elapsed_nostream))

    # with stream
    START_TIME = default_timer()
    isogeo.get(
        "https://v1.api.qa.isogeo.com/resources/search?_limit=0",
        verify=False,
        stream=True,
    )
    elapsed_stream = default_timer() - START_TIME
    print("With stream: {:5.2f}s".format(elapsed_stream))

    # with content-length check
    START_TIME = default_timer()
    with isogeo.get(
        url="https://v1.api.qa.isogeo.com/resources/search?_limit=0",
        stream=True,
        verify=False,
    ) as r:
        if int(r.headers["content-length"]) > 10000:
            print("Too heavy")
            elapsed_stream_check = default_timer() - START_TIME
            print("With stream check: {:5.2f}s".format(elapsed_stream_check))
            exit()
        else:
            print("Acceptable weight")
            elapsed_stream_check = default_timer() - START_TIME
            print("With stream check: {:5.2f}s".format(elapsed_stream_check))

    # -- END -------
    isogeo.close()  # close session
