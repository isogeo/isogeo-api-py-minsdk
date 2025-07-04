# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""Complementary set of tools to make some checks on requests to Isogeo API."""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import socket
import warnings
from collections import Counter
from json import JSONDecodeError
from uuid import UUID
from typing import Union

# modules
from isogeo_pysdk.enums import LinkActions, MetadataSubresources

# ##############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)

FILTER_KEYS = {
    "action": [],
    "catalog": [],
    "contact:group": [],
    "contact:isogeo": [],
    "coordinate-system": [],
    "data-source": [],
    "format": [],
    "has-no": [],
    "keyword:isogeo": [],
    "keyword:inspire-theme": [],
    "license:group": [],
    "license:isogeo": [],
    "owner": [],
    "provider": [],
    "text": [],
    "type": [],
}

FILTER_PROVIDERS = ("manual", "auto")

FILTER_TYPES = {
    "dataset": "dataset",
    "raster-dataset": "rasterDataset",
    "vector-dataset": "vectorDataset",
    "no-geo-dataset": "noGeoDataset",
    "resource": "resource",
    "service": "service",
}

GEORELATIONS = ("contains", "disjoint", "equal", "intersects", "overlaps", "within")

EDIT_TABS = {
    "identification": ",".join(FILTER_TYPES),
    "history": ",".join(FILTER_TYPES),
    "geography": "dataset, raster-dataset, vector-dataset, no-geo-dataset, service",
    "quality": "dataset, raster-dataset, vector-dataset, no-geo-dataset, service",
    "attributes": "vector-dataset, no-geo-dataset, series",
    "constraints": ",".join(FILTER_TYPES),
    "resources": ",".join(FILTER_TYPES),
    "contacts": ",".join(FILTER_TYPES),
    "advanced": ",".join(FILTER_TYPES),
    "metadata": ",".join(FILTER_TYPES),
}

_SUBRESOURCES_KW = ("_abilities", "count", "thesaurus")

_SUBRESOURCES_CT = ("count",)

# ##############################################################################
# ########## Classes ###############
# ##################################


class IsogeoChecker(object):
    """Complementary set of tools to make some checks on requests to Isogeo API."""

    def __init__(self):
        super(IsogeoChecker, self).__init__()

    def check_internet_connection(
        self, remote_server: str = "api.isogeo.com", proxies: dict = None
    ) -> bool:
        """Test if an internet connection is operational.
        Src: https://stackoverflow.com/a/20913928/2556577.

        :param str remote_server: remote server used to check
        """
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(remote_server)
            # connect to the host -- tells us if it's reachable
            sock = socket.create_connection((host, 80), 2)
            sock.close()
            return True
        except Exception as e:
            logger.error(e)
            if proxies is not None:
                logger.debug("Proxy detected. Ignoring error...")
                return True
            return False

    def check_api_response(self, response) -> Union[bool, tuple]:
        """Check API response and raise exceptions if needed.

        :param requests.models.Response response: request response to check

        :rtype: bool or tuple

        :Example:
        >>> checker.check_api_response(<Response [500]>)
        (False, 500)
        """
        # check response
        if response.status_code == 200:
            return True
        elif response.status_code >= 400:
            # ensure response got a JSON.
            # See: https://github.com/isogeo/isogeo-api-py-minsdk/issues/136
            try:
                resp_error_msg = response.json().get("error")
            except JSONDecodeError:
                resp_error_msg = ""

            # log it
            logger.error(
                "{}: {} - {} - URL: {}".format(
                    response.status_code,
                    response.reason,
                    resp_error_msg,
                    response.request.url,
                )
            )
            return False, response.status_code

    def check_request_parameters(self, parameters: dict = {}):
        """Check parameters passed to avoid errors and help debug.

        :param dict response: search request parameters
        """
        # -- SEMANTIC QUERY ---------------------------------------------------
        li_args = parameters.get("q").split()
        logger.debug(li_args)

        # Unicity
        li_filters = [i.split(":")[0] for i in li_args]
        filters_count = Counter(li_filters)
        li_filters_must_be_unique = ("coordinate-system", "format", "owner", "type")
        for i in filters_count:
            if i in li_filters_must_be_unique and filters_count.get(i) > 1:
                raise ValueError(
                    "This query filter must be unique: {}"
                    " and it occurred {} times.".format(i, filters_count.get(i))
                )

        # dict
        dico_query = FILTER_KEYS.copy()
        for i in li_args:
            if i.startswith("action"):
                dico_query["action"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("catalog"):
                dico_query["catalog"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("contact") and i.split(":")[1] == "group":
                dico_query["contact:group"].append(i.split(":")[1:][1])
                continue
            elif i.startswith("contact"):
                dico_query["contact:isogeo"].append(i.split(":", 1)[1])
                continue
            elif i.startswith("coordinate-system"):
                dico_query["coordinate-system"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("data-source"):
                dico_query["data-source"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("format"):
                dico_query["format"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("has-no"):
                dico_query["has-no"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("keyword:isogeo"):
                dico_query["keyword:isogeo"].append(i.split(":")[1:][1])
                continue
            elif i.startswith("keyword:inspire-theme"):
                dico_query["keyword:inspire-theme"].append(i.split(":")[1:][1])
                continue
            elif i.startswith("license:isogeo"):
                dico_query["license:isogeo"].append(i.split(":")[1:][1:])
                continue
            elif i.startswith("license"):
                dico_query["license:group"].append(i.split(":", 1)[1:][0:])
                continue
            elif i.startswith("owner"):
                dico_query["owner"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("provider"):
                dico_query["provider"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("share"):
                dico_query["share"].append(i.split(":")[1:][0])
                continue
            elif i.startswith("type"):
                dico_query["type"].append(i.split(":")[1:][0])
                continue
            else:
                # logger.debug(i.split(":")[1], i.split(":")[1].isdigit())
                dico_query["text"].append(i)
                continue

        # Values
        dico_filters = {i.split(":")[0]: i.split(":")[1:] for i in li_args}
        if dico_filters.get("type", ("dataset",))[0].lower() not in FILTER_TYPES:
            raise ValueError(
                "type value must be one of: {}".format(" | ".join(FILTER_TYPES))
            )
        elif (
            dico_filters.get("action", ("download",))[0].lower()
            not in LinkActions.__members__
        ):
            raise ValueError(
                "action value must be one of: {}".format(
                    " | ".join(LinkActions.__members__)
                )
            )
        elif (
            dico_filters.get("provider", ("manual",))[0].lower() not in FILTER_PROVIDERS
        ):
            raise ValueError(
                "provider value must be one of: {}".format(" | ".join(FILTER_PROVIDERS))
            )
        else:
            logger.debug(dico_filters)

        # -- GEOGRAPHIC -------------------------------------------------------
        in_box = parameters.get("box")
        in_geo = parameters.get("geo")
        # geometric relation
        in_rel = parameters.get("rel")
        if in_rel and in_box is None and in_geo is None:
            raise ValueError("'rel' should'nt be used without box or geo.")
        elif in_rel not in GEORELATIONS and in_rel is not None:
            raise ValueError(
                "{} is not a correct value for 'georel'."
                " Must be one of: {}.".format(in_rel, " | ".join(GEORELATIONS))
            )

    @classmethod
    def check_is_uuid(self, uuid_str: str):
        """Check if it's an Isogeo UUID handling specific form.

        :param str uuid_str: UUID string to check
        """
        # check uuid type
        if not isinstance(uuid_str, str):
            logger.debug(
                TypeError(
                    "'uuid_str' parameter expects a str value. Got: {}".format(
                        type(uuid_str)
                    )
                )
            )
            return False
        else:
            pass
        # handle Isogeo specific UUID in XML exports
        if "isogeo:metadata" in uuid_str:
            uuid_str = "urn:uuid:{}".format(uuid_str.split(":")[-1])
        else:
            pass
        # test it
        try:
            uid = UUID(uuid_str)
            return uid.hex == uuid_str.replace("-", "").replace("urn:uuid:", "")
        except ValueError as e:
            logger.warning(
                "uuid ValueError. {} ({}) -- {}".format(type(uuid_str), uuid_str, e)
            )
            return False

    def check_edit_tab(self, tab: str, md_type: str):
        """Check if asked tab is part of Isogeo web form and reliable with metadata type.

        :param str tab: tab to check. Must be one one of EDIT_TABS attribute
        :param str md_type: metadata type. Must be one one of FILTER_TYPES
        """
        # check parameters types
        if not isinstance(tab, str):
            raise TypeError("'tab' expected a str value, not {}".format(type(tab)))
        else:
            pass
        if not isinstance(md_type, str):
            raise TypeError(
                "'md_type' expected a str value, not {}".format(type(md_type))
            )
        else:
            pass
        # check parameters values
        if tab not in EDIT_TABS:
            raise ValueError(
                "'{}' isn't a valid edition tab. "
                "Available values: {}".format(tab, " | ".join(EDIT_TABS))
            )
        else:
            pass
        if md_type not in FILTER_TYPES:
            if md_type in FILTER_TYPES.values():
                md_type = self._convert_md_type(md_type)
            else:
                raise ValueError(
                    "'{}' isn't a valid metadata type. "
                    "Available values: {}".format(md_type, " | ".join(FILTER_TYPES))
                )
        else:
            pass
        # check adequation tab/md_type
        if md_type not in EDIT_TABS.get(tab):
            raise ValueError(
                "'{}'  isn't a valid tab for a '{}'' metadata."
                " Only for these types: {}.".format(tab, md_type, EDIT_TABS.get(tab))
            )
        else:
            return True

    # -- FILTERS -------------------------------------------------------------
    def _check_filter_specific_md(self, specific_md: tuple):
        """Check if specific_md parameter is valid.

        :param tuple specific_md: tuple of specific metadata UUID to check
        """
        if isinstance(specific_md, (list, tuple)):
            if len(specific_md) > 0:
                # checking UUIDs and popping bad ones
                specific_md = list(specific_md)
                for md in specific_md:
                    if not self.check_is_uuid(md):
                        specific_md.remove(md)
                        logger.warning(
                            "Incorrect metadata UUID has been removed: {}".format(md)
                        )
                # joining survivors
                specific_md = ",".join(specific_md)
            else:
                specific_md = ""
        else:
            raise TypeError(
                "'specific_md' expects a tuple, not {}".format(type(specific_md))
            )
        return specific_md

    def _check_filter_specific_tag(self, specific_tag: list):
        """Check if specific_tag parameter is valid.

        :param list specific_tag: list of specific tag to check
        """
        if isinstance(specific_tag, list):
            if len(specific_tag) > 0:
                specific_tag = ",".join(specific_tag)
            else:
                specific_tag = ""
        else:
            raise TypeError("'specific_tag' expects a list")
        return specific_tag

    def _check_filter_includes(self, includes: tuple, entity: str = "metadata") -> list:
        """Check if specific_resources parameter is valid.

        :param tuple includes: sub resources to check
        :param str entity: entity type to check sub resources. Must be one of:

          - contact
          - metadata
          - keyword

        :rtype: list

        :raises: ValueError if entity is not an accepted value
        :raises: TypeError if includes is not a tuple or a str
        """
        # check entity parameter
        if entity == "metadata":
            ref_subresources = [item.value for item in MetadataSubresources]
        elif entity == "keyword":
            ref_subresources = _SUBRESOURCES_KW
        elif entity == "contact":
            ref_subresources = _SUBRESOURCES_CT
        else:
            raise ValueError("Must be one of: contact | metadata | keyword.")

        # sub resources manager
        if isinstance(includes, str) and includes.lower() == "all":
            includes = ",".join(ref_subresources)
        elif isinstance(includes, (list, tuple)):
            if len(includes):
                for subresource in includes:
                    if subresource not in ref_subresources:
                        logger.warning(
                            "'{}' is not a valid subresource to include. "
                            "Must be one of: {}. It will be removed or ignored.".format(
                                subresource, " | ".join(ref_subresources)
                            )
                        )
                        list(includes).remove(subresource)  # removing bad subresource
                    else:
                        pass

                includes = ",".join(includes)
            else:
                includes = ""
        else:
            raise TypeError(
                "'includes' expect a tuple or a str='all', not {}".format(
                    type(includes)
                )
            )
        return includes

    def _check_subresource(self, subresource: str):
        """Check if specific_resources parameter is valid.

        :param str resource: subresource to check.
        """
        # warnings.warn(
        #     "subresource in URL is deprecated." " Use _include mechanism instead.",
        #     DeprecationWarning,
        # )
        l_subresources = (
            "conditions",
            "contacts",
            "coordinate-system",
            "events",
            "feature-attributes",
            "keywords",
            "layers",
            "limitations",
            "links",
            "operations",
            "specifications",
        )
        if isinstance(subresource, str):
            if subresource in l_subresources:
                subresource = subresource
            elif subresource == "tags":
                subresource = "keywords"
                logger.debug(
                    "'tags' is an include not a subresource."
                    " Don't worry, it has be automatically renamed "
                    "into 'keywords' which is the correct subresource."
                )
            elif subresource == "serviceLayers":
                subresource = "layers"
                logger.debug(
                    "'serviceLayers' is an include not a subresource."
                    " Don't worry, it has be automatically renamed "
                    "into 'layers' which is the correct subresource."
                )
            else:
                raise ValueError(
                    "Invalid subresource. Must be one of: {}".format(
                        "|".join(l_subresources)
                    )
                )
        else:
            raise TypeError("'subresource' expects a str")
        return subresource

    def _convert_md_type(self, type_to_convert: str):
        """Metadata types are not consistent in Isogeo API. A vector dataset is defined as vector-
        dataset in query filter but as vectorDataset in resource (metadata) details.

        see: https://github.com/isogeo/isogeo-api-py-minsdk/issues/29
        """
        if type_to_convert in FILTER_TYPES:
            return FILTER_TYPES.get(type_to_convert)
        elif type_to_convert in FILTER_TYPES.values():
            return [k for k, v in FILTER_TYPES.items() if v == type_to_convert][0]
        else:
            raise ValueError(
                "Incorrect metadata type to convert: {}".format(type_to_convert)
            )


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """Standalone execution."""
    checker = IsogeoChecker()
