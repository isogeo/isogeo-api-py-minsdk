# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Attributes analisis
# Purpose:      Get feature attributes from Isogeo to perform some metrics.
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      14/04/2016
# Updated:      10/05/2017
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import configparser  # to manage options.ini
from collections import Counter
from os import path

# Isogeo
from isogeo_pysdk import Isogeo

# ############################################################################
# ######### Main program ###########
# ##################################

if __name__ == "__main__":
    """Standalone execution"""
    # storing application parameters into an ini file
    settings_file = r"../isogeo_params.ini"

    # testing ini file
    if not path.isfile(path.realpath(settings_file)):
        raise IOError(
            "ERROR: to execute this script as standalone,"
            " you need to store your Isogeo application "
            "settings in a isogeo_params.ini file."
            " You can use the template to set your own."
        )
    else:
        pass

    # reading ini file
    config = configparser.SafeConfigParser()
    config.read(settings_file)

    share_id = config.get("auth", "app_id")
    share_token = config.get("auth", "app_secret")

    # instanciating the class
    isogeo = Isogeo(client_id=share_id, client_secret=share_token, lang="fr")

    token = isogeo.connect()

    # ------------ REAL START ------------------------------------------------

    # search
    search = isogeo.search(
        token,
        query="type:vector-dataset",
        include=["feature-attributes"],
        page_size=100,
        whole_share=0,
    )

    if type(search) != dict:
        raise TypeError(search)
    else:
        pass

    # variables
    attributes = {}
    attributes_names = []
    attributes_types = []
    attributes_alias = []
    attributes_description = []
    vectors_without_attributes = []

    # parse
    for md in search.get("results"):
        md_attributes = md.get("feature-attributes")
        if not md_attributes:
            vectors_without_attributes.append(
                "{} ({})".format(md.get("title"), md.get("_id"))
            )
            continue
        for field in md_attributes:
            attributes_names.append(field.get("name"))
            attributes_alias.append(field.get("alias", "NR"))
            attributes_types.append(field.get("dataType"))
            attributes_description.append(field.get("description", "NR"))
            attributes[field.get("name")] = (
                field.get("dataType"),
                field.get("alias", "NR"),
                field.get("description", "NR"),
            )

    # global metrics
    print(
        "{} attributes among "
        "{} metadatas retrieved of which "
        "{} do not have feature attributes.".format(
            len(attributes_names),
            len(search.get("results")),
            len(vectors_without_attributes),
        )
    )

    # attributes names
    names_frequency = Counter(attributes_names)
    names_top10 = names_frequency.most_common(10)
    print("\nTop 10 attributes names: ", names_top10)

    # attributes types
    types_frequency = Counter(attributes_types)
    types_top10 = types_frequency.most_common(10)
    print("\nTop 10 attributes types: ", types_top10)

    # attributes aliases
    alias_frequency = Counter(attributes_alias)
    alias_top10 = alias_frequency.most_common(10)
    print("\nTop 10 attributes aliases: ", alias_top10)

    # attributes aliases
    description_frequency = Counter(attributes_description)
    description_top10 = description_frequency.most_common(10)
    print("\nTop 10 attributes descriptions: ", description_top10)
