# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# ------------------------------------------------------------------------------
# Name:         Isogeo metadata preprocessor
# Purpose:      Preprocess metadatas downloaded from Isogeo.
#               It's one of the submodules of isogeo2office
#               (https://bitbucket.org/isogeo/isogeo-2-office).
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      14/02/2016
# Updated:      31/03/2016
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from datetime import datetime

# 3rd party library
from dateutil.parser import parse as dtparse

# ##############################################################################
# ########## Classes ###############
# ##################################


class IsogeoPreProcessor(object):
    """
    docstring for IsogeoPreProcessor
    """
    def __init__(self, search_results):
        """ Isogeo connection parameters
        """
        super(Isogeo, self).__init__()
        self.search = search_results

    def tags_extractor(self):
        """ Adds lists of useful tags to the search_results attributes:
        * owners
        * keywords
        * INSPIRE themes
        * formats
        * coordinate systems
        * type of resources
        * available actions
        """
        # recipient variables
        resources_types = {}
        owners = {}
        keywords = {}
        theminspire = {}
        formats = {}
        srs = {}
        actions = []

        # parsing tags
        tags = self.search.get('tags')
        for tag in tags.keys():
            # resources type
            if tag.startswith('type'):
                resources_types[self.types_lbl.get(tag[5:])] = tag[5:]
                continue
            else:
                pass
            # owners
            if tag.startswith('owner'):
                owners[tags.get(tag)] = tag[6:]
                continue
            else:
                pass
            # custom keywords
            if tag.startswith('keyword:isogeo'):
                keywords[tags.get(tag)] = tag[15:]
                continue
            else:
                pass
            # INSPIRE themes
            if tag.startswith('keyword:inspire-theme'):
                theminspire[tags.get(tag)] = tag[22:]
                continue
            else:
                pass
            # formats
            if tag.startswith('format'):
                formats[tags.get(tag)] = tag[7:]
                continue
            else:
                pass
            # coordinate systems
            if tag.startswith('coordinate-system'):
                srs[tags.get(tag)] = tag[18:]
                continue
            else:
                pass
            # available actions
            if tag.startswith('action'):
                actions.append(tag[7:])
                continue
            else:
                pass

        # storing
        self.search['actions'] = actions
        self.search['datatypes'] = resources_types
        self.search['coordsys'] = srs
        self.search['formats'] = formats
        self.search['inspire'] = theminspire
        self.search['keywords'] = keywords
        self.search['owners'] = owners

        # end of method
        return self.search

    def safe_empty_values(self, rpl_value="NR"):
        """ Parses metadata attributes and replace missing
        attributes by a default value to avoid None errors
        """
        for md in self.search:
            for key in md.iterkeys():
                md.setdefault(key, rpl_value)

        # end of methode
        return

###############################################################################
###### Stand alone program ########
###################################

if __name__ == '__main__':
    """ Standalone execution and tests
    """
    # ------------ Specific imports ---------------------
    from ConfigParser import SafeConfigParser   # to manage options.ini
    from os import path

    # Custom modules
    from isogeo_sdk import Isogeo

    # ------------ Settings from ini file ----------------
    if not path.isfile(path.realpath(r"..\settings.ini")):
        print("ERROR: to execute this script as standalone, you need to store your Isogeo application settings in a isogeo_params.ini file. You can use the template to set your own.")
        import sys
        sys.exit()
    else:
        pass

    config = SafeConfigParser()
    config.read(r"..\settings.ini")

    settings = {s: dict(config.items(s)) for s in config.sections()}
    app_id = settings.get('auth').get('app_id')
    app_secret = settings.get('auth').get('app_secret')
    client_lang = settings.get('basics').get('def_codelang')

    # ------------ Connecting to Isogeo API ----------------
    # instanciating the class
    isogeo = Isogeo(client_id=app_id,
                    client_secret=app_secret,
                    lang="fr")

    token = isogeo.connect()

    # ------------ Isogeo search --------------------------
    search_results = isogeo.search(token,
                                   sub_resources=isogeo.sub_resources_available,
                                   preprocess=1)

    # ------------ REAL START ----------------------------
