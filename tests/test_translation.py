# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from sys import exit
import unittest

# module target
from isogeo_pysdk import Isogeo, IsogeoTranslator, __version__ as pysdk_version


# #############################################################################
# ######## Globals #################
# ##################################

# API access
app_id = environ.get('ISOGEO_API_DEV_ID')
app_token = environ.get('ISOGEO_API_DEV_SECRET')

li_contacts_fr = ("Auteur",
                  "Point de contact",
                  "Administrateur",
                  "Distributeur",
                  "Créateur",
                  "Propriétaire",
                  "Analyste principal",
                  "Responsable du traitement",
                  "Éditeur (publication)",
                  "Fournisseur",
                  "Utilisateur")

li_contacts_en = ("Author",
                  "Point of contact",
                  "Custodian",
                  "Distributor",
                  "Originator",
                  "Owner",
                  "Principal investigator",
                  "Processor",
                  "Publisher",
                  "Resource provider",
                  "User")

# #############################################################################
# ########## Classes ###############
# ##################################


class Translation(unittest.TestCase):
    """Test translation of specific words wihtin Isogeo API."""
    if not app_id or not app_token:
        logging.critical("No API credentials set as env variables.")
        exit()
    else:
        pass
    logging.debug('Isogeo PySDK version: {0}'.format(pysdk_version))

    # standard methods
    def setUp(self):
        """Executed before each test."""
        self.isogeo = Isogeo(client_id=app_id,
                             client_secret=app_token,
                             lang="FR")
        self.bearer = self.isogeo.connect()
        self.md_contacts = self.isogeo.resource(self.bearer,
                                                "e5e5ab788aff4418a1cd4a38f842ccbe",
                                                sub_resources=["contacts"],
                                                )
        self.li_contacts_roles = [i.get("role")
                                  for i in self.md_contacts.get("contacts")]
        # print(li_contacts_roles)

    def tearDown(self):
        """Executed after each test."""
        pass

    # tests
    def test_translation_fr(self):
        """Some French translations get from the subclass."""
        tr = IsogeoTranslator("FR")
        # contacts roles
        for role in self.li_contacts_roles:
            self.assertIn(tr.tr("roles", role), li_contacts_fr)

    def test_translation_en(self):
        """Some English translations get from the subclass."""
        tr = IsogeoTranslator("EN")
        # contacts roles
        for role in self.li_contacts_roles:
            self.assertIn(tr.tr("roles", role), li_contacts_en)


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == '__main__':
    unittest.main()
