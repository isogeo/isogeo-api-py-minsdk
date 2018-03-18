# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from six import string_types as str
from os import environ
import logging
from sys import exit
import unittest

# module target
from isogeo_pysdk import Isogeo


# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get('ISOGEO_API_DEV_ID')
app_token = environ.get('ISOGEO_API_DEV_SECRET')

# #############################################################################
# ########## Classes ###############
# ##################################


class Search(unittest.TestCase):
    """Test search to Isogeo API."""
    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=app_id,
                             client_secret=app_token)
        self.bearer = self.isogeo.connect()

    def tearDown(self):
        """Executed after each test."""
        pass

    # metadata models
    def test_search_result_vector_min(self):
        """Search with sub-resources included."""
        # from a specific md. Can be viewed here: https://goo.gl/RDWDWJ
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    specific_md=["c4b7ad9732454beca1ab3ec1958ffa50",])
        md = search.get("results")[0]
        self.assertIsInstance(md, dict)

        # basic metadata keys/keys
        self.assertIn("_id", md)
        self.assertIn("_created", md)
        self.assertIn("_modified", md)
        self.assertIn("_creator", md)
        self.assertIn("_abilities", md)
        self.assertIn("title", md)
        self.assertIn("type", md)
        self.assertIn("tags", md)
        self.assertIn("editionProfile", md)
        self.assertIn("series", md)

        # _creator keys/values
        md_crea = md.get("_creator")
        self.assertIsInstance(md_crea, dict)
        self.assertIn("_id", md_crea)
        self.assertIn("_tag", md_crea)
        self.assertIn("_created", md_crea)
        self.assertIn("_modified", md_crea)
        self.assertIn("contact", md_crea)
        self.assertIn("canCreateMetadata", md_crea)
        self.assertIn("canCreateLegacyServiceLinks", md_crea)
        self.assertIn("areKeywordsRestricted", md_crea)
        self.assertIn("hasCswClient", md_crea)
        self.assertIn("hasScanFme", md_crea)
        self.assertIn("keywordsCasing", md_crea)
        self.assertIn("metadataLanguage", md_crea)

        # _creator subcontact keys/values
        md_crea_ct = md_crea.get("contact")
        self.assertIsInstance(md_crea_ct, dict)
        self.assertIn("_id", md_crea_ct)
        self.assertIn("_tag", md_crea_ct)
        self.assertIn("_deleted", md_crea_ct)
        self.assertIn("type", md_crea_ct)
        self.assertIn("name", md_crea_ct)
        self.assertIn("email", md_crea_ct)
        self.assertIn("addressLine1", md_crea_ct)
        self.assertIn("addressLine2", md_crea_ct)
        self.assertIn("city", md_crea_ct)
        self.assertIn("zipCode", md_crea_ct)
        self.assertIn("countryCode", md_crea_ct)
        self.assertIn("available", md_crea_ct)

        # _tags keys/values
        md_tags = md.get("tags")
        self.assertIsInstance(md_tags, dict)
        self.assertIn("type:vector-dataset", md_tags)
        self.assertIn("owner:32f7e95ec4e94ca3bc1afda960003882", md_tags)
        self.assertIn("provider:manual", md_tags)

    def test_search_result_raster_min(self):
        """Search with sub-resources included."""
        # from a specific md. Can be viewed here: https://goo.gl/RDWDWJ
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    specific_md=["3663e29d3c2a433384ee308b4d632a04",])
        md = search.get("results")[0]
        self.assertIsInstance(md, dict)

        # basic metadata keys/keys
        self.assertIn("_id", md)
        self.assertIn("_created", md)
        self.assertIn("_modified", md)
        self.assertIn("_creator", md)
        self.assertIn("_abilities", md)
        self.assertIn("title", md)
        self.assertIn("type", md)
        self.assertIn("tags", md)
        self.assertIn("editionProfile", md)
        self.assertIn("series", md)

        # _creator keys/values
        md_crea = md.get("_creator")
        self.assertIsInstance(md_crea, dict)
        self.assertIn("_id", md_crea)
        self.assertIn("_tag", md_crea)
        self.assertIn("_created", md_crea)
        self.assertIn("_modified", md_crea)
        self.assertIn("contact", md_crea)
        self.assertIn("canCreateMetadata", md_crea)
        self.assertIn("canCreateLegacyServiceLinks", md_crea)
        self.assertIn("areKeywordsRestricted", md_crea)
        self.assertIn("hasCswClient", md_crea)
        self.assertIn("hasScanFme", md_crea)
        self.assertIn("keywordsCasing", md_crea)
        self.assertIn("metadataLanguage", md_crea)

        # _creator subcontact keys/values
        md_crea_ct = md_crea.get("contact")
        self.assertIsInstance(md_crea_ct, dict)
        self.assertIn("_id", md_crea_ct)
        self.assertIn("_tag", md_crea_ct)
        self.assertIn("_deleted", md_crea_ct)
        self.assertIn("type", md_crea_ct)
        self.assertIn("name", md_crea_ct)
        self.assertIn("email", md_crea_ct)
        self.assertIn("addressLine1", md_crea_ct)
        self.assertIn("addressLine2", md_crea_ct)
        self.assertIn("city", md_crea_ct)
        self.assertIn("zipCode", md_crea_ct)
        self.assertIn("countryCode", md_crea_ct)
        self.assertIn("available", md_crea_ct)

        # _tags keys/values
        md_tags = md.get("tags")
        self.assertIsInstance(md_tags, dict)
        self.assertIn("type:raster-dataset", md_tags)
        self.assertIn("owner:32f7e95ec4e94ca3bc1afda960003882", md_tags)
        self.assertIn("provider:manual", md_tags)

    def test_search_result_resource_min(self):
        """Search with sub-resources included."""
        # from a specific md. Can be viewed here: https://goo.gl/RDWDWJ
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    specific_md=["d3df351cb9a64a35b6bde4a383c9bddc",])
        md = search.get("results")[0]
        self.assertIsInstance(md, dict)

        # basic metadata keys/keys
        self.assertIn("_id", md)
        self.assertIn("_created", md)
        self.assertIn("_modified", md)
        self.assertIn("_creator", md)
        self.assertIn("_abilities", md)
        self.assertIn("title", md)
        self.assertIn("type", md)
        self.assertIn("tags", md)
        self.assertIn("editionProfile", md)

        # _creator keys/values
        md_crea = md.get("_creator")
        self.assertIsInstance(md_crea, dict)
        self.assertIn("_id", md_crea)
        self.assertIn("_tag", md_crea)
        self.assertIn("_created", md_crea)
        self.assertIn("_modified", md_crea)
        self.assertIn("contact", md_crea)
        self.assertIn("canCreateMetadata", md_crea)
        self.assertIn("canCreateLegacyServiceLinks", md_crea)
        self.assertIn("areKeywordsRestricted", md_crea)
        self.assertIn("hasCswClient", md_crea)
        self.assertIn("hasScanFme", md_crea)
        self.assertIn("keywordsCasing", md_crea)
        self.assertIn("metadataLanguage", md_crea)

        # _creator subcontact keys/values
        md_crea_ct = md_crea.get("contact")
        self.assertIsInstance(md_crea_ct, dict)
        self.assertIn("_id", md_crea_ct)
        self.assertIn("_tag", md_crea_ct)
        self.assertIn("_deleted", md_crea_ct)
        self.assertIn("type", md_crea_ct)
        self.assertIn("name", md_crea_ct)
        self.assertIn("email", md_crea_ct)
        self.assertIn("addressLine1", md_crea_ct)
        self.assertIn("addressLine2", md_crea_ct)
        self.assertIn("city", md_crea_ct)
        self.assertIn("zipCode", md_crea_ct)
        self.assertIn("countryCode", md_crea_ct)
        self.assertIn("available", md_crea_ct)

        # _tags keys/values
        md_tags = md.get("tags")
        self.assertIsInstance(md_tags, dict)
        self.assertIn("type:resource", md_tags)
        self.assertIn("owner:32f7e95ec4e94ca3bc1afda960003882", md_tags)
        self.assertIn("provider:manual", md_tags)

    def test_search_result_series_min(self):
        """Search with sub-resources included."""
        # from a specific md. Can be viewed here: https://goo.gl/RDWDWJ
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    specific_md=["af522449ae5041cf9f058c9e8822f45f",])
        md = search.get("results")[0]
        self.assertIsInstance(md, dict)

        # basic metadata keys/keys
        self.assertIn("_id", md)
        self.assertIn("_created", md)
        self.assertIn("_modified", md)
        self.assertIn("_creator", md)
        self.assertIn("_abilities", md)
        self.assertIn("title", md)
        self.assertIn("type", md)
        self.assertIn("tags", md)
        self.assertIn("editionProfile", md)
        self.assertIn("series", md)
        self.assertEqual(md.get("series"), 1)

        # _creator keys/values
        md_crea = md.get("_creator")
        self.assertIsInstance(md_crea, dict)
        self.assertIn("_id", md_crea)
        self.assertIn("_tag", md_crea)
        self.assertIn("_created", md_crea)
        self.assertIn("_modified", md_crea)
        self.assertIn("contact", md_crea)
        self.assertIn("canCreateMetadata", md_crea)
        self.assertIn("canCreateLegacyServiceLinks", md_crea)
        self.assertIn("areKeywordsRestricted", md_crea)
        self.assertIn("hasCswClient", md_crea)
        self.assertIn("hasScanFme", md_crea)
        self.assertIn("keywordsCasing", md_crea)
        self.assertIn("metadataLanguage", md_crea)

        # _creator subcontact keys/values
        md_crea_ct = md_crea.get("contact")
        self.assertIsInstance(md_crea_ct, dict)
        self.assertIn("_id", md_crea_ct)
        self.assertIn("_tag", md_crea_ct)
        self.assertIn("_deleted", md_crea_ct)
        self.assertIn("type", md_crea_ct)
        self.assertIn("name", md_crea_ct)
        self.assertIn("email", md_crea_ct)
        self.assertIn("addressLine1", md_crea_ct)
        self.assertIn("addressLine2", md_crea_ct)
        self.assertIn("city", md_crea_ct)
        self.assertIn("zipCode", md_crea_ct)
        self.assertIn("countryCode", md_crea_ct)
        self.assertIn("available", md_crea_ct)

        # _tags keys/values
        md_tags = md.get("tags")
        self.assertIsInstance(md_tags, dict)
        self.assertIn("type:raster-dataset", md_tags)
        self.assertIn("owner:32f7e95ec4e94ca3bc1afda960003882", md_tags)
        self.assertIn("provider:manual", md_tags)

    def test_search_result_service_min(self):
        """Search with sub-resources included."""
        # from a specific md. Can be viewed here: https://goo.gl/RDWDWJ
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    specific_md=["a7653d11752c4a6c890a9f9d1603eceb",])
        md = search.get("results")[0]
        self.assertIsInstance(md, dict)

        # basic metadata keys/keys
        self.assertIn("_id", md)
        self.assertIn("_created", md)
        self.assertIn("_modified", md)
        self.assertIn("_creator", md)
        self.assertIn("_abilities", md)
        self.assertIn("title", md)
        self.assertIn("path", md)
        self.assertIn("type", md)
        self.assertIn("tags", md)
        self.assertIn("editionProfile", md)

        # _creator keys/values
        md_crea = md.get("_creator")
        self.assertIsInstance(md_crea, dict)
        self.assertIn("_id", md_crea)
        self.assertIn("_tag", md_crea)
        self.assertIn("_created", md_crea)
        self.assertIn("_modified", md_crea)
        self.assertIn("contact", md_crea)
        self.assertIn("canCreateMetadata", md_crea)
        self.assertIn("canCreateLegacyServiceLinks", md_crea)
        self.assertIn("areKeywordsRestricted", md_crea)
        self.assertIn("hasCswClient", md_crea)
        self.assertIn("hasScanFme", md_crea)
        self.assertIn("keywordsCasing", md_crea)
        self.assertIn("metadataLanguage", md_crea)

        # _creator subcontact keys/values
        md_crea_ct = md_crea.get("contact")
        self.assertIsInstance(md_crea_ct, dict)
        self.assertIn("_id", md_crea_ct)
        self.assertIn("_tag", md_crea_ct)
        self.assertIn("_deleted", md_crea_ct)
        self.assertIn("type", md_crea_ct)
        self.assertIn("name", md_crea_ct)
        self.assertIn("email", md_crea_ct)
        self.assertIn("addressLine1", md_crea_ct)
        self.assertIn("addressLine2", md_crea_ct)
        self.assertIn("city", md_crea_ct)
        self.assertIn("zipCode", md_crea_ct)
        self.assertIn("countryCode", md_crea_ct)
        self.assertIn("available", md_crea_ct)

        # _tags keys/values
        md_tags = md.get("tags")
        self.assertIsInstance(md_tags, dict)
        self.assertIn("type:service", md_tags)
        self.assertIn("owner:32f7e95ec4e94ca3bc1afda960003882", md_tags)
        self.assertIn("provider:manual", md_tags)

    # specific attributes
    def test_search_result_inspire_compliance(self):
        """Search with sub-resources included."""
        # from a specific md. Can be viewed here: https://goo.gl/RDWDWJ
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    specific_md=["3c649da21ed9405e8d508bfdbe831516",],
                                    sub_resources=["contacts", ])
        md = search.get("results")[0]
        self.assertIsInstance(md, dict)

        # basic metadata keys/keys
        self.assertIn("_id", md)
        self.assertIn("_created", md)
        self.assertIn("_modified", md)
        self.assertIn("_creator", md)
        self.assertIn("_abilities", md)
        self.assertIn("title", md)
        self.assertIn("type", md)
        self.assertIn("tags", md)
        self.assertIn("editionProfile", md)
        self.assertIn("series", md)

        # _tags keys/values
        md_tags = md.get("tags")
        self.assertIsInstance(md_tags, dict)
        self.assertIn("conformity:inspire", md_tags)
        self.assertIsNone(md_tags.get("conformity:inspire"))
        self.assertIn("owner:32f7e95ec4e94ca3bc1afda960003882", md_tags)
        self.assertIn("provider:manual", md_tags)

        # INSPIRE compliance expected keys/values
        self.assertIn("abstract", md)
        self.assertIn("collectionContext", md)
        self.assertIn("envelope", md)
        self.assertIn("format", md)
        self.assertIn("formatVersion", md)
        self.assertIn("scale", md)
        self.assertIn("encoding", md)
        self.assertIn("created", md)
        self.assertIn("contacts", md)

    # share models
    def test_shares(self):
        """Check shares route model response."""
        shares = self.isogeo.shares(self.bearer)
        share = shares[0]
        self.assertIsInstance(share, dict)

        # root keys
        self.assertIn("_created", share)
        self.assertIn("_creator", share)
        self.assertIn("_id", share)
        self.assertIn("_modified", share)
        self.assertIn("applications", share)
        self.assertIn("catalogs", share)
        self.assertIn("name", share)
        self.assertIn("rights", share)
        self.assertIn("type", share)
        self.assertIn("urlToken", share)

        # root values
        self.assertIsInstance(share.get("_created"), str)
        self.assertIsInstance(share.get("_id"), str)
        self.assertIsInstance(share.get("_modified"), str)
        self.assertIsInstance(share.get("applications"), list)
        self.assertIsInstance(share.get("catalogs"), list)
        self.assertIsInstance(share.get("name"), str)
        self.assertIsInstance(share.get("catalogs"), list)
        self.assertIsInstance(share.get("rights"), list)
        self.assertIsInstance(share.get("type"), str)
        self.assertIsInstance(share.get("urlToken"), str)

        # _creator keys/values
        share_crea = share.get("_creator")
        self.assertIsInstance(share_crea, dict)
        self.assertIn("_created", share_crea)
        self.assertIn("_id", share_crea)
        self.assertIn("_modified", share_crea)
        self.assertIn("_tag", share_crea)
        self.assertIn("areKeywordsRestricted", share_crea)
        self.assertIn("canCreateLegacyServiceLinks", share_crea)
        self.assertIn("canCreateMetadata", share_crea)
        self.assertIn("contact", share_crea)
        self.assertIn("hasCswClient", share_crea)
        self.assertIn("hasScanFme", share_crea)
        self.assertIn("keywordsCasing", share_crea)
        self.assertIn("metadataLanguage", share_crea)

        # _creator subcontact keys/values
        share_crea_ct = share_crea.get("contact")
        self.assertIsInstance(share_crea_ct, dict)
        self.assertIn("_deleted", share_crea_ct)
        self.assertIn("_id", share_crea_ct)
        self.assertIn("_tag", share_crea_ct)
        self.assertIn("addressLine1", share_crea_ct)
        self.assertIn("addressLine2", share_crea_ct)
        self.assertIn("available", share_crea_ct)
        self.assertIn("city", share_crea_ct)
        self.assertIn("countryCode", share_crea_ct)
        self.assertIn("email", share_crea_ct)
        self.assertIn("fax", share_crea_ct)
        self.assertIn("name", share_crea_ct)
        self.assertIn("phone", share_crea_ct)
        self.assertIn("type", share_crea_ct)
        self.assertIn("zipCode", share_crea_ct)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
