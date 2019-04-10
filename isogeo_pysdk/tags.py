# -*- coding: UTF-8 -*-
#! python3
# ----------------------------------------------------------------------------

"""
    Complementary set of utils to use with Isogeo API.
"""

# ---------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
import logging

# modules
try:
    from . import checker
except (ImportError, ValueError, SystemError):
    import checker

# ##############################################################################
# ########## Globals ###############
# ##################################

checker = checker.IsogeoChecker()

# ##############################################################################
# ########## Classes ###############
# ##################################


class TagsHelpers(object):
    """Helpers to manipulate tags."""

    def __init__(self):
        """Instanciate TagsHelpers module.

        """
        super(TagsHelpers, self).__init__()

    # properties
    def _workgroups_as_dict(self, tags: dict) -> dict:
        """Transform"""
        return {
            k.split(":")[1]: v
            for k, v in tags.items()
            if k.startswith("owner")
            }


    # inner methods
    def _duplicate_tag_handler(
        self, target_dict: dict, duplicate: tuple, mode: str, workgroups: dict
    ):
        """Handle duplicates cases.
        
        tag name = k = duplicate[1]
        tag value = v = duplicate[0]
        """
        if mode == "merge":
            target_dict[duplicate[0]] += "||" + duplicate[1]
        elif mode == "rename":
            # get workgroup uuid
            if checker.check_is_uuid(duplicate[1].split(":")[1]):
                k_uuid = duplicate[1].split(":")[1]
            else:
                k_uuid = duplicate[1].split(":")[2]
            # match with workgroups owners
            if k_uuid in workgroups:
                repl = workgroups.get(k_uuid[:5])
            else:
                repl = k_uuid[:5]
            target_dict["{} ({})".format(duplicate[0], repl)] = duplicate[1]
        else:
            pass
        return

    # -- TAGS --------------------------------------------------------------------
    def tags_to_dict(self, tags=dict, prev_query=dict, duplicated: str = "rename"):
        """Reverse search tags dictionary to values as keys.
        Useful to populate filters comboboxes for example.

        :param dict tags: tags dictionary from a search request
        :param dict prev_query: query parameters returned after a search request. Typically `search.get("query")`.
        :param str duplicated: what to do about duplicated tags label. Values:

          * ignore - last tag parsed survives
          * merge - add duplicated in value as separated list (sep = '||')
          * rename [default] - if duplicated tag labels are part of different workgroup,
            so the tag label is renamed with workgroup.
        """
        # for rename option, get workgroups
        if duplicated == "rename":
            wgs = self._workgroups_as_dict(tags=tags)
            # wgs = None
            # wgs = {k.split(":")[1]: v for k, v in tags.items() if k.startswith("owner")}
            # wgs = list(filter(lambda x[1]: x[0].startswith("owner"), tags.items()))
        elif duplicated == "ignore" or duplicated == "merge":
            wgs = None
        else:
            raise ValueError(
                "Duplicated value '{}' is not an accepted value."
                " Please refer to __doc__ method.".format(duplicated)
            )

        # -- SEARCH TAGS -------------
        # output dicts structure
        tags_as_dicts = {
            "actions": {},
            "catalogs": {},      # name can be duplicated
            "contacts": {},      # name can be duplicated
            "data-sources": {},  # name can be duplicated
            "formats": {},
            "inspires": {},
            "keywords": {},
            "licenses": {},      # name can be duplicated
            "owners": {},
            "providers": {},
            "shares": {},
            "srs": {},
            "types": {},
        }

        # parsing tags and storing each one in a dict
        for k, v in sorted(tags.items()):
            # k = tag name
            # v = tag value
            if k.startswith("action"):
                tags_as_dicts.get("actions")[v] = k
                continue
            elif k.startswith("catalog"):
                if v in tags_as_dicts.get("catalogs") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        target_dict=tags_as_dicts.get("catalogs"),
                        duplicate=(v, k),
                        mode=duplicated,
                        workgroups=wgs
                    )
                else:
                    logging.debug(
                        "Duplicated catalog name: {}. Last catalog will retained.".format(
                            v
                        )
                    )
                    tags_as_dicts.get("catalogs")[v] = k
                continue
            elif k.startswith("contact"):
                if v in tags_as_dicts.get("contacts") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        tags_as_dicts.get("contacts"),
                        duplicate=(v, k),
                        mode=duplicated,
                        workgroups=wgs
                    )
                else:
                    logging.debug(
                        "Duplicated contact name: {}. Last contact is retained.".format(
                            v
                        )
                    )
                    tags_as_dicts.get("contacts")[v] = k
                continue
            elif k.startswith("coordinate-system"):
                tags_as_dicts.get("srs")[v] = k
                continue
            elif k.startswith("data-source"):
                if v in tags_as_dicts.get("data-sources") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        tags_as_dicts.get("data-sources"),
                        duplicate=(v, k),
                        mode=duplicated,
                        workgroups=wgs
                    )
                else:
                    logging.debug(
                        "Duplicated data-source name: {}. Last data-source is retained.".format(
                            v
                        )
                    )
                    tags_as_dicts.get("data-sources")[v] = k
                continue
            elif k.startswith("format"):
                tags_as_dicts.get("formats")[v] = k
                continue
            elif k.startswith("keyword:in"):
                tags_as_dicts.get("inspires")[v] = k
                continue
            elif k.startswith("keyword:is"):
                tags_as_dicts.get("keywords")[v] = k
                continue
            elif k.startswith("license"):
                if v in tags_as_dicts.get("licenses") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        tags_as_dicts.get("licenses"), (v, k), duplicated, wgs
                    )
                else:
                    logging.debug(
                        "Duplicated license name: {}. Last license is retained.".format(
                            v
                        )
                    )
                    tags_as_dicts.get("licenses")[v] = k
                continue
            elif k.startswith("owner"):
                tags_as_dicts.get("owners")[v] = k
                continue
            elif k.startswith("provider"):
                # providers are particular because its value is always null
                tags_as_dicts.get("providers")[k.split(":")[1]] = k
                continue
            elif k.startswith("share"):
                tags_as_dicts.get("shares")[v] = k
                continue
            elif k.startswith("type"):
                tags_as_dicts.get("types")[v] = k
                continue
            # ignored tags
            else:
                logging.debug("Unrecognized tag has been ignored during parsing: {}".format(k))

        # -- QUERY TAGS -------------
        # handle share case
        if prev_query.get("_shares"):
            prev_query.get("_tags").append(
                "share:{}".format(prev_query.get("_shares")[0])
            )
        else:
            pass
        # output dict struture
        logging.debug(prev_query)
        query_as_dicts = {
            "_tags": {
                "actions": {},
                "catalogs": {},
                "contacts": {},
                "data-sources": {},
                "formats": {},
                "inspires": {},
                "keywords": {},
                "licenses": {},
                "owners": {},
                "providers": {},
                "shares": {},
                "srs": {},
                "types": {},
            },
            "_shares": prev_query.get("_shares"),
            "_terms": prev_query.get("_terms"),
        }

        # parsing and matching tags
        query_tags = query_as_dicts.get("_tags")
        for t in prev_query.get("_tags"):
            if t.startswith("action"):
                query_tags.get("actions")[tags.get(t)] = t
                continue
            elif t.startswith("catalog"):
                if v in query_tags.get("catalogs") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        query_tags.get("catalogs"), (v, k), duplicated, wgs
                    )
                else:
                    logging.debug(
                        "Duplicated catalog name: {}. Last catalog is retained.".format(
                            v
                        )
                    )
                    query_tags.get("catalogs")[tags.get(t)] = t
                continue
            elif t.startswith("contact"):
                if v in query_tags.get("contacts") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        query_tags.get("contacts"), (v, k), duplicated, wgs
                    )
                else:
                    logging.debug(
                        "Duplicated contact name: {}. Last contact is retained.".format(
                            v
                        )
                    )
                    query_tags.get("contacts")[tags.get(t)] = t
                continue
            elif t.startswith("coordinate-system"):
                query_tags.get("srs")[tags.get(t)] = t
                continue
            elif t.startswith("data-source"):
                if v in query_tags.get("data-sources") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        query_tags.get("data-sources"), (v, k), duplicated, wgs
                    )
                else:
                    logging.debug(
                        "Duplicated data-source name: {}. Last data-source is retained.".format(
                            v
                        )
                    )
                    query_tags.get("data-sources")[tags.get(t)] = t
                continue
            elif t.startswith("format"):
                query_tags.get("formats")[tags.get(t)] = t
                continue
            elif t.startswith("keyword:in"):
                query_tags.get("inspires")[tags.get(t)] = t
                continue
            elif t.startswith("keyword:is"):
                query_tags.get("keywords")[tags.get(t)] = t
                continue
            elif t.startswith("license"):
                if v in query_tags.get("licenses") and duplicated != "ignore":
                    self._duplicate_tag_handler(
                        query_tags.get("licenses"), (v, k), duplicated, wgs
                    )
                else:
                    logging.debug(
                        "Duplicated license name: {}. Last license is retained.".format(
                            v
                        )
                    )
                    query_tags.get("licenses")[tags.get(t)] = t
                continue
            elif t.startswith("owner"):
                query_tags.get("owners")[tags.get(t)] = t
                continue
            elif t.startswith("provider"):
                # providers are particular bcause its value is always null.
                query_tags.get("providers")[k.split(":")[1]] = k
                continue
            elif t.startswith("share"):
                query_tags.get("shares")[tags.get(t)] = t
                continue
            elif t.startswith("type"):
                query_tags.get("types")[tags.get(t)] = t
                continue
            # ignored tags
            else:
                logging.debug(
                    "A query tag has been ignored during parsing: {}".format(t)
                )

        # return the output
        return tags_as_dicts, query_as_dicts


# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """Standalone execution."""
    tagshlpr = TagsHelpers()
