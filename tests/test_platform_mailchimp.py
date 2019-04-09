# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    python -m unittest tests.test_platform_mailchimp
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from sys import exit
import unittest

# 3rd party
import requests

# Mailchimp
from mailchimp3 import MailChimp

# #############################################################################
# ######## Globals #################
# ##################################

# API access
isogeo_mailchimp_api_prod = environ.get("ISOGEO_MAILCHIMP_API_PROD_KEY")
isogeo_mailchimp_api_qa = environ.get("ISOGEO_MAILCHIMP_API_QA_KEY")


# #############################################################################
# ######## Classes #################
# ##################################


class TestMailchimp(unittest.TestCase):
    """Test authentication process."""

    if not isogeo_mailchimp_api_prod or not isogeo_mailchimp_api_qa:
        logging.critical("No API credentials set as env variables.")
        exit()

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.headers = requests.utils.default_headers()
        self.headers["User-Agent"] = "Isogeo Python SDK - Unittests (it@isogeo.com)"

    def tearDown(self):
        """Executed after each test."""
        pass

    # Mailchimp
    def test_mailchimp_status_prod(self):
        """Check the mailchimp authentication and PROD status."""
        client = MailChimp(
            mc_api=isogeo_mailchimp_api_prod,
            mc_user="Unittest - Python SDK",
            request_headers=self.headers,
            timeout=10.0,
        )
        p = client.ping
        self.assertDictEqual(p.get(), {"health_status": "Everything's Chimpy!"})

    def test_mailchimp_status_qa(self):
        """Check the mailchimp authentication and QA status."""
        client = MailChimp(
            mc_api=isogeo_mailchimp_api_qa,
            mc_user="Unittest - Python SDK",
            request_headers=self.headers,
            timeout=30.0,
        )
        p = client.ping
        self.assertDictEqual(p.get(), {"health_status": "Everything's Chimpy!"})

    def test_mailchimp_lists_qa(self):
        """Check present lists into the mailchimp organization."""
        client = MailChimp(
            mc_api=isogeo_mailchimp_api_prod,
            mc_user="Unittest - Python SDK",
            request_headers=self.headers,
            timeout=30.0,
        )
        lists_subscribers = client.lists.all(get_all=True, fields="lists.name,lists.id")
        self.assertEqual(lists_subscribers.get("total_items"), 5)

    def test_mailchimp_bad_api_key(self):
        """Must fail during connection step."""
        with self.assertRaises(ValueError):
            client = MailChimp(
                mc_api="ImNotAValidApiKey",
                mc_user="Unittest - Python SDK",
                request_headers=self.headers,
                timeout=10.0,
            )


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    unittest.main()
