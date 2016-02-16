# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (print_function, unicode_literals)
# -----------------------------------------------------------------------------
# Name:         Isogeo
# Purpose:      Python minimalist SDK to use Isogeo API
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      22/12/2015
# Updated:      10/01/2016
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import base64
from collections import Counter
import socket
import locale
from math import ceil

# 3rd party library
import arrow
import requests

# #############################################################################
# ########## Classes ###############
# ##################################

class Isogeo(object):
    """
    docstring for Isogeo
    """
    # useful variables
    sub_resources_available = [
                                "conditions",
                                "contacts",
                                "coordinate-system",
                                "events",
                                "feature-attributes",
                                "keywords",
                                "limitations",
                                "links",
                                "specifications"
                              ]

    geo_relations_available = [
                                "contains",
                                "disjoint",
                                "equal",
                                "intersects",
                                "overlaps",
                                "within"
                              ]

    tr_types_label_en = {
                            "vector-dataset": "Vector",
                            "raster-dataset": "Raster",
                            "resource": "Resources",
                            "service": "Geographic service"
                        }

    tr_types_label_fr = {
                            "vector-dataset": "Vecteur",
                            "raster-dataset": "Raster",
                            "resource": "Ressources",
                            "service": "Service géographique"
                        }

    def __init__(self, client_id, client_secret, lang="en", proxy=None):
        """ Isogeo connection parameters

        Keyword arguments:
        client_id -- application identifier
        client_secret -- application
        secret lang -- language asked for localized tags (INSPIRE themes).
        Could be "en" [DEFAULT] or "fr".
        proxy -- to pass through the local
        proxy. Optional. Must be a dict { 'protocol':
        'http://username:password@proxy_url:port' }.\ e.g.: {'http':
        'http://martin:p4ssW0rde@10.1.68.1:5678',\ 'https':
        'http://martin:p4ssW0rde@10.1.68.1:5678'}")
        """
        super(Isogeo, self).__init__()
        self.id = client_id
        self.ct = client_secret

        # checking internet connection
        if self.check_internet_connection:
            print("Your're connected to the world!")
            pass
        else:
            print("It seems that your internet connection isn't available. Check it up and try again!")
            return

        # testing parameters
        if len(client_secret) != 64:
            print("Your application secret isn't good. Check it.")
            return
        else:
            pass

        # setting language
        if lang.lower() not in ("fr", "en"):
            print("Isogeo API is only available in English ('en', default) or \
                   French ('fr').\nYour language has been set on English.")
            self.lang = "en"
        else:
            self.lang = lang.lower()

        # setting locale according to the language passed
        if lang.lower() == "fr":
            locale.setlocale(locale.LC_ALL, str("fra_fra"))
            self.types_lbl = self.tr_types_label_fr
        else:
            locale.setlocale(locale.LC_ALL, str("uk_UK"))
            self.types_lbl = self.tr_types_label_en

        # handling proxy parameters
        # see: http://docs.python-requests.org/en/latest/user/advanced/#proxies
        if proxy and type(proxy) is dict and 'http' in proxy.keys():
            print("Proxy activated")
            self.proxies = proxy
        elif proxy and type(proxy) is not dict:
            print("Proxy syntax error. Must be a dict { 'protocol': 'http://username:password@proxy_url:port' }.\
                e.g.: {'http': 'http://martin:p4ssW0rde@10.1.68.1:5678',\
                       'https': 'http://martin:p4ssW0rde@10.1.68.1:5678'}")
            return
        else:
            self.proxies = {}
            print("No proxy set. Use default configuration.")
            pass

    def connect(self, client_id=None, client_secret=None):
        """
        Isogeo API uses oAuth  2.0 protocol (http://tools.ietf.org/html/rfc6749)
        see: https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing#heading=h.1rjxk9mvjoc0
        """
        # instanciated or direct call
        if not client_id and not client_secret:
            client_id = self.id
            client_secret = self.ct
        else:
            pass

        # requires a basic Authentication header encoded in Base64 (https://en.wikipedia.org/wiki/Base64)
        # see: http://tools.ietf.org/html/rfc2617#section-2
        credentials = base64.b64encode(client_id + ":" + client_secret)
        headers = {"Authorization": "Basic " + credentials}

        # using Client Credentials Grant method
        # see: http://tools.ietf.org/html/rfc6749#section-4.4
        payload = {"grant_type":"client_credentials"}

        # passing request to get a 24h bearer
        # see: http://tools.ietf.org/html/rfc6750#section-2
        conn = requests.post("https://id.api.isogeo.com/oauth/token",
                             headers=headers,
                             data=payload,
                             proxies=self.proxies)

        # just a fast check
        self.check_api_response(conn)

        # getting access
        axx = conn.json()
        bearer = axx.get("access_token")

        # get the limit date
        expiration_date = arrow.get(arrow.utcnow().timestamp + axx.get("expires_in"))

        # end of method
        return (bearer, expiration_date)

    def share(self, jeton):
        """
        TO DO
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # passing auth parameter
        head = {"Authorization": "Bearer " + jeton[0]}
        share_req = requests.get("https://v1.api.isogeo.com/shares/",
                                 headers=head,
                                 proxies=self.proxies)

        # checking response
        self.check_api_response(share_req)

        # end of method
        return share_req.json()

    def search(self,
               jeton,
               query="",
               bbox=None,
               poly=None,
               georel=None,
               order_by="_created",
               order_dir="desc",
               page_size=100,
               offset=0,
               sub_resources=[],
               whole_share=True,
               preprocess=0,
               prot="https"):
        """ Search request

        Keyword arguments:
        jeton -- API bearer
        query -- search terms. It could be a simple string like 'oil' or a tag
        like 'keyword:isogeo:formations' or 'keyword:inspire-theme:landcover'.
        \nThe AND operator is applied when various tags are passed.\nEmpty by default.
        bbox -- Bounding box to limit the search. Must be a 4 list of coordinates in WGS84 (EPSG 4326).\
        \nCould be completed with the georel parameter
        poly -- Geographic criteria for the search, in WKT format.\
        \nCould be completed by the georel parameter.
        georel -- spatial operator to apply to the bbox or poly parameters.\
        \n\tAvailable values: 'contains', 'disjoint', 'equals', 'intersects' [DEFAULT],\
        'overlaps', 'within'. To get available values: 'isogeo.geo_relations_available'.
        order_by -- to sort results. \n\tAvailable values:\n\t'_created': metadata
        creation date [DEFAULT]\n\t'_modified': metadata last update\n\t'title': metadata title\n\t'created': data
        creation date (possibly None)\n\t'modified': data last update date
        (possibly None).
        order_dir -- sorting direction. \n\tAvailable values:\n\t'desc':
        descending [DEFAULT]\n\t'asc': ascending
        page_size -- limits the number of results. Useful to paginate results display.
        offset -- offset
        sub_resources -- indicates subresources that should be returned. Must be a list of strings.\\n
        To get available values: 'isogeo.sub_resources_available'
        whole_share -- option to return all results or only the page size. True by DEFAULT.
        preprocess -- option to get preprocessed results. It could be much longer...

        see: https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing#heading=h.yusgqavk96n1
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # sub resources specific parsing
        if sub_resources == "all":
            sub_resources = self.sub_resources_available
        elif type(sub_resources) is list:
            sub_resources = ",".join(sub_resources)
        else:
            return "Error: sub_resources argument must be a list or 'all'"

        # handling request parameters
        payload = {
                   '_include': sub_resources,
                   '_lang': self.lang,
                   '_limit': page_size,
                   '_offset': offset,
                   'box': bbox,
                   'geo': poly,
                   'rel': georel,
                   'ob': order_by,
                   'od': order_dir,
                   'q': query,
                   }

        # search request
        head = {"Authorization": "Bearer " + jeton[0]}
        search_req = requests.get(prot + "://v1.api.isogeo.com/resources/search",
                                  headers=head,
                                  params=payload,
                                  proxies=self.proxies)
        # fast response check
        self.check_api_response(search_req)

        # serializing result into dict and storing resources in variables
        search_rez = search_req.json()
        resources_count = search_rez.get('total')  # total of metadatas shared

        # handling Isogeo API pagination
        # see: https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing#heading=h.bg6le8mcd07z
        if resources_count > page_size and whole_share:
            # if API returned more than one page of results, let's get the rest!
            metadatas = []  # a recipient list
            payload['_limit'] = 100  # now it'll get pages of 100 resources
            # let's parse pages
            for idx in range(0, int(ceil(resources_count / 100)) + 1):
                payload['_offset'] = idx * 100
                search_req = requests.get(prot + "://v1.api.isogeo.com/resources/search",
                                          headers=head,
                                          params=payload)
                # storing results by addition
                metadatas.extend(search_req.json().get('results'))
            search_rez['results'] = metadatas
        else:
            pass

        # storing
        # print(len(metadatas) == len(set(search_rez['li_ids_md'])))  # checking dobles

        if preprocess:
            self.search_preprocessed(jeton, search_rez)
        else:
            pass

        # end of method
        return search_rez

    def search_preprocessed(self, jeton, search):
        """
        X dernières données modifiées
        X dernières md modifiées
        list owners / occurrences
        list keywords / occurrences
        list catalogs
        list ids
        list contacts / occurrences
        count / percentage view
        count / percentage download
        count / percentage both
        count / percentage other
        """
        # recipient variables
        ids_md = []
        resources_types = {}
        owners = {}
        keywords = {}
        theminspire = {}
        formats = {}
        srs = {}
        actions = []

        # parsing tags
        tags = search.get('tags')
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

        # # parsing resources
        # for md in search.get('results'):
        #     ids_md.append(md.get('_id'))
        #     # owners stats
        #     # owners[md.get('tags')]

        # storing
        search['actions'] = actions
        search['datatypes'] = resources_types
        search['coordsys'] = srs
        search['formats'] = formats
        search['inspire'] = theminspire
        search['keywords'] = keywords
        # search['li_ids_md'] = ids_md
        search['owners'] = owners

        # end of method
        return search

    def resource(self, jeton, id_resource, sub_resources=list, prot="https"):
        """
        TO DO
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # handling request parameters
        payload = {
                   '_include': sub_resources
                   }

        # resource search
        head = {"Authorization": "Bearer " + jeton[0]}
        resource_req = requests.get(prot + "://v1.api.isogeo.com/resources/" + id_resource,
                                    headers=head,
                                    params=payload,
                                    proxies=self.proxies
                                    )
        self.check_api_response(resource_req)

        # end of method
        return resource_req.json()

    def check_bearer_validity(self, jeton):
        """
        Isogeo ID delivers authentication bearers which are valid during 24h, so
        this method checks the validity of the token (jeton in French) with a
        30 mn anticipation limit, and renews it if necessary.

        jeton = must be a tuple like (bearer, expiration_date)

        see: http://tools.ietf.org/html/rfc6750#section-2
        FI: 24h = 86400 seconds, 30 mn = 1800
        """
        if (jeton[1].timestamp - arrow.utcnow().timestamp) < 1800:
            jeton = self.connect(self.id, self.ct)
            # print("Your bearer had expired then has been renewed. Just go on!")
        else:
            # print("Your bearer is still valid. Just go on!")
            pass

        # end of method
        return jeton

    def check_api_response(self, response):
        """
        Check the API response and raise exceptions if needed
        """
        if response.status_code == 200:
            # print("Everything is OK dude, just go on!")
            pass
        elif response.status_code >= 400:
            print("Something's wrong Houston, check your parameters again!")
            print(dir(response))
            response.raise_for_status()
            return 0
        else:
            pass

        # end of method
        return 1

    def check_internet_connection(self, remote_server="www.isogeo.com"):
        """ Test if an internet connection is operational
        source: http://stackoverflow.com/a/20913928/2556577
        """
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(remote_server)
            # connect to the host -- tells us if the host is actually
            # reachable
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        # end of method
        return False

# ##############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == '__main__':
    """ standalone execution """
    # ------------ Specific imports ----------------
    import ConfigParser     # to manage options.ini 
    from os import path
    from random import randrange    # to get a random resource

    # ------------ Settings from ini file ----------------
    if not path.isfile(path.realpath(r"isogeo_params.ini")):
        print("ERROR: to execute this script as standalone, you need to store your Isogeo application settings in a isogeo_params.ini file. You can use the template to set your own.")
        import sys
        sys.exit()
    else:
        pass

    config = ConfigParser.SafeConfigParser()
    config.read(r"isogeo_params.ini")

    share_id = config.get('auth', 'app_id')
    share_token = config.get('auth', 'app_secret')

    # ------------ Real start ----------------
    # instanciating the class
    isogeo = Isogeo(client_id=share_id,
                    client_secret=share_token,
                    lang="fr")

    # check which sub resources are available
    # print(isogeo.sub_resources_available)
    # print(isogeo.tr_types_label_fr)

    # getting a token
    jeton = isogeo.connect()

    # option to get some precprocessed stats (needs more time)
    preproc = 1

    # # get share properties
    # share = isogeo.share(jeton)
    # print(share)
    # print(share.get("catalogs"))

    # let's search for metadatas!
    # print(dir(isogeo))
    search = isogeo.search(jeton,
                           # sub_resources='all',
                           # sub_resources=["conditions", "contacts"],
                           sub_resources=isogeo.sub_resources_available,
                           # query="keyword:isogeo:2015",
                           preprocess=preproc,
                           prot='http')

    print(search.keys())
    print(search.get('query'))
    print("Total count of metadatas shared: ", search.get("total"))
    print("Count of resources got by request: {}\n".format(len(search.get("results"))))
    # print(search.get("results")[0].get("contacts"))

    # get one random resource
    hatnumber = randrange(0, len(search.get("results")))
    my_resource = isogeo.resource(jeton,
                                  search.get("results")[hatnumber].get("_id"),
                                  sub_resources=isogeo.sub_resources_available,
                                  prot="http"
                                  )
    print(my_resource.keys())

    # count and parse related resources
    # actions number
    count_view = isogeo.search(jeton,
                               query="action:view",
                               page_size=0,
                               whole_share=0,
                               prot="http",
                               preprocess=0)
    print("count of resources with view action: {}".format(count_view.get('total')))

    kind_ogc = ('wfs', 'wms', 'wmts')
    kind_esri = ('esriFeatureService', 'esriMapService', 'esriTileService')

    li_ogc = []
    li_esri = []
    li_dl = []

    for md in search.get('results'):
        rel_resources = md.get('links')
        if not rel_resources:
            continue
        else:
            pass
        for link in rel_resources:
            # only OGC
            if link.get('kind') in kind_ogc\
            or (link.get('type') == 'link' and link.get('link').get('kind') in kind_ogc):
                li_ogc.append((link.get('title'), link.get('url')))
                continue
            else:
                pass

            # only Esri
            if link.get('kind') in kind_esri\
            or (link.get('type') == 'link' and link.get('link').get('kind') in kind_esri):
                li_esri.append((link.get('title'), link.get('url')))
                continue
            else:
                pass

            # downloadable
            if link.get('kind') == 'data' and link.get('actions') == 'download'\
            or (link.get('type') == 'link' and link.get('link').get('kind') == 'data'):
                li_dl.append((link.get('title'), link.get('url')))
                continue
            else:
                pass

            # secondary
            if link.get('type') == 'link':
                # li_dl.append((link.get('title'), link.get('url')))
                print(link.get('kind'))
                print(link.get('link'), "\n")
                continue
            else:
                pass

            # others
            # print(link)

    # print("\n\tOGC: ", li_ogc)
    # print("\n\tEsri: ", li_esri)
    # print("\n\tDownload: ", li_dl)

    # if preproc == 1:
    #     print(search.get('owners'))
    #     print(search.get('datatypes'))
    #     print(search.get('keywords'))
    #     print(search.get('inspire'))
    #     print(search.get('formats'))
    #     print(search.get('coordsys'))
    #     print(search.get('actions'))
    # else:
    #     pass
