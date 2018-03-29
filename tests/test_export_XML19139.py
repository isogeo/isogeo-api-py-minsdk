# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from sys import exit
from tempfile import mkstemp
import unittest
import xml.etree.ElementTree as ET

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


class ExportXML19139(unittest.TestCase):
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
    def test_export_XML19139(self):
        """Download a metadata in XML 19139."""
        search = self.isogeo.search(self.bearer, whole_share=0,
                                    query="type:dataset",
                                    page_size=1)
        # get the metadata
        md_id = search.get("results")[0].get("_id")

        # download the XML version
        xml_stream = self.isogeo.xml19139(self.bearer,
                                          md_id)

        # create tempfile and fill with downloaded XML
        tmp_output = mkstemp(prefix="IsogeoPySDK_" + md_id[:5])
        with open(tmp_output[1] + ".xml", "wb") as fd:
            for block in xml_stream.iter_content(1024):
                fd.write(block)

        # read XML
        tree = ET.parse(tmp_output[1] + ".xml")
        root = tree.getroot()

        # check XML structure
        self.assertEqual(root.tag, "{http://www.isotc211.org/2005/gmd}MD_Metadata")
        self.assertEqual(root[0].tag, "{http://www.isotc211.org/2005/gmd}fileIdentifier")
        self.assertEqual(root[1].tag, "{http://www.isotc211.org/2005/gmd}language")
        self.assertEqual(root[2].tag, "{http://www.isotc211.org/2005/gmd}characterSet")
        self.assertEqual(root[3].tag, "{http://www.isotc211.org/2005/gmd}hierarchyLevel")
        self.assertEqual(root[4].tag, "{http://www.isotc211.org/2005/gmd}contact")
        self.assertEqual(root[5].tag, "{http://www.isotc211.org/2005/gmd}dateStamp")
        self.assertEqual(root[6].tag, "{http://www.isotc211.org/2005/gmd}metadataStandardName")
        self.assertEqual(root[7].tag, "{http://www.isotc211.org/2005/gmd}metadataStandardVersion")
        self.assertEqual(root[8].tag, "{http://www.isotc211.org/2005/gmd}spatialRepresentationInfo")
        self.assertEqual(root[9].tag, "{http://www.isotc211.org/2005/gmd}referenceSystemInfo")
        self.assertEqual(root[10].tag, "{http://www.isotc211.org/2005/gmd}identificationInfo")
        self.assertEqual(root[11].tag, "{http://www.isotc211.org/2005/gmd}distributionInfo")
        self.assertEqual(root[12].tag, "{http://www.isotc211.org/2005/gmd}dataQualityInfo")

    def test_export_bad(self):
        """Test errors raised by export function"""
        with self.assertRaises(ValueError):
            self.isogeo.xml19139(self.bearer,
                                 "trust_me_its_an_uuid")


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == '__main__':
    unittest.main()
