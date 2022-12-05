#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_about

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
import urllib3
from socket import gethostname
from sys import _getframe
from time import gmtime, sleep, strftime
from os import environ
from pathlib import Path

# 3rd party
from dotenv import load_dotenv

# module target
from isogeo_pysdk import ApiAbout


# #############################################################################
# ######## Globals #################
# ##################################

if Path("dev.env").exists():
    load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name."""
    return "TEST_PySDK - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestAccount(unittest.TestCase):
    """Test Account model of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    def setUp(self):
        """Executed before each test."""
        if environ.get("ISOGEO_PLATFORM").lower() in ["qa", "custom"]:
            urllib3.disable_warnings()
        # tests stuff
        self.discriminator = "{}_{}".format(
            hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
        )

    def tearDown(self):
        """Executed after each test."""
        sleep(0.5)

    # -- TESTS ---------------------------------------------------------

    # -- GET --
    def test_about(self):
        """Get platform components versions"""
        # PROD
        isogeo_about = ApiAbout()
        print(isogeo_about.api())
        print(isogeo_about.database())
        print(isogeo_about.authentication())
        # print(isogeo_about.scan())
        # print(isogeo_about.services())

        # QA
        isogeo_about = ApiAbout("qa")
        print(isogeo_about.api())
        print(isogeo_about.database())
        print(isogeo_about.authentication())
        # print(isogeo_about.scan())
        # print(isogeo_about.services())

        # custom
        isogeo_about = ApiAbout(
            platform="custom",
            isogeo_urls={"api_url": environ.get("ISOGEO_API_URL")}
        )
        print(isogeo_about.api())
        print(isogeo_about.database())
        # print(isogeo_about.authentication())
        # print(isogeo_about.scan())
        # print(isogeo_about.services())

# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
