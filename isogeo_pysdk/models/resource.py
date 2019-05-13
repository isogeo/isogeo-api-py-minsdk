# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of Resource (= Metadata) entity

    See: http://help.isogeo.com/api/complete/index.html#definition-resource
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint


# #############################################################################
# ########## Classes ###############
# ##################################
class Resource(object):
    """Resource are the main entities in Isogeo, they represent metadata.

    Sample:

    ```json
    {
        '_abilities': [
            'metadata:content-upload',
            'metadata:delete',
            'metadata:update'
            ],
        '_created': '2018-06-14T13:22:17.2880035+00:00',
        '_creator': {
            '_created': '2015-05-21T12:08:16.4295098+00:00',
            '_id': '32f7e95ec4e94ca3bc1afda960003882',
            '_modified': '2019-05-03T10:31:01.4796052+00:00',
            '_tag': 'owner:32f7e95ec4e94ca3bc1afda960003882',
            'areKeywordsRestricted': True,
            'canCreateLegacyServiceLinks': True,
            'canCreateMetadata': True,
            'resource': {
                '_deleted': False,
                '_id': '2a3aefc4f80347f590afe58127f6cb0f',
                '_tag': 'resource:group:2a3aefc4f80347f590afe58127f6cb0f',
                'addressLine1': '26 rue du faubourg Saint-Antoine',
                'addressLine2': '4 éme étage',
                'available': True,
                'city': 'Paris',
                'countryCode': 'FR',
                'email': 'dev@isogeo.com',
                'fax': '33 (0)9 67 46 50 06',
                'name': 'Isogeo Test',
                'phone': '33 (0)9 67 46 50 06',
                'type': 'group',
                'zipCode': '75012'
                },
            'hasCswClient': False,
            'hasScanFme': True,
            'keywordsCasing': 'lowercase',
            'metadataLanguage': 'fr',
            'themeColor': '#4499A1'
            },
        '_id': '43380f6c60424095b67cbd1aa9526fe4',
        '_modified': '2018-11-19T14:45:27.5211691+00:00',
        'abstract': '**Gras**\n'
                    '*Italique*\t\n'
                    '<del>Supprimé</del>\n'
                    '<cite>Citation</cite>\n'
                    '\n'
                    '* Élément 1\n'
                    '* Élément 2\n'
                    '\n'
                    '1. Élément 1\n'
                    '2. Élément 2\n'
                    '\n'
                    '[Foo](http://foo.bar)',
        'collectionContext': 'Possibly long text',
        'collectionMethod': 'Possibly long text',
        'conditions': [
            {
                '_id': '0ad0664576ef4bf08a16abf853eb213b',
                'description': 'Possibly long text in markdown',
                'license': {
                    '_id': 'cdf0eecc36534cb2b49c79ad281dee65',
                    '_tag': 'license:isogeo:cdf0eecc36534cb2b49c79ad281dee65',
                    'link': 'http://vvlibri.org/fr/licence/odbl/10/fr',
                    'name': 'ODbL 1.0 - Open Database Licence'
                    }
            }
            ],
        'contacts': [
            {'resource': {
                '_deleted': False,
                '_id': '643f1035377b4ca59da6f31a39704c34',
                '_tag': 'resource:group:643f1035377b4ca59da6f31a39704c34',
                'addressLine1': '26 rue du faubourg Saint-Antoine',
                'available': True,
                'city': 'Paris',
                'countryCode': 'FR',
                'email': 'resource@isogeo.com',
                'fax': '+33 9 81 40 00 66',
                'name': 'Isogeo',
                'phone': '+33 9 82 39 20 53',
                'type': 'group',
                'zipCode': '75012'
                },
                'role': 'author'
                }
                ],
        'coordinate-system': {
            '_tag': 'coordinate-system:2154',
            'code': 2154,
            'name': 'RGF93 / Lambert-93'
            },
        'created': '2018-06-04T00:00:00+00:00',
        'distance': 5.0,
        'editionProfile': 'manual',
        'encoding': 'iso-8859-15',
        'envelope': {
            'bbox': [
                -13.359375,
                24.5271348225978,
                26.015625,
                59.5343180010956
            ],
            'coordinates': [
                [
                    [-13.359375, 24.5271348225978],
                    [26.015625, 24.5271348225978],
                    [26.015625, 59.5343180010956],
                    [-13.359375, 59.5343180010956],
                    [-13.359375, 24.5271348225978]
                ]
            ],
            'type': 'Polygon'
        },
        'events': [
            {
                '_id': 'fec8a8d92de9400d8d7742962bacfc59',
                'date': '2018-06-14T00:00:00+00:00',
                'description': '',
                'kind': 'publication'
                },
            {
                '_id': '46455174c27849fabf1e64f7d12ea0ee',
                'date': '2018-06-13T00:00:00+00:00',
                'description': '',
                'kind': 'update'
                },
            {
                '_id': 'eed830ffdfee46ca9d070c152e8a632c',
                'date': '2018-06-04T00:00:00+00:00',
                'kind': 'creation'
                }
        ],
        'feature-attributes': [{'_id': 'c959f434753647979c9d9dba73f609c3',
                                'alias': 'Identifiant',
                                'dataType': 'Nombre',
                                'description': '**Gras**\n'
                                                '*Italique*\t\n'
                                                '<del>Supprimé</del>\n'
                                                '<cite>Citation</cite>\n'
                                                '\n'
                                                '* Élément 1\n'
                                                '* Élément 2\n'
                                                '\n'
                                                '1. Élément 1\n'
                                                '2. Élément 2\n'
                                                '\n'
                                                '[Foo](http://foo.bar)',
                                'language': 'fr',
                                'name': 'ID'}],
        'features': 150,
        'format': 'shp',
        'formatVersion': '1.0',
        'geometry': 'Polygon',
        'keywords': [{'_id': 'b181316d4e254c23839128062f914140',
                    '_tag': 'keyword:inspire-theme:addresses',
                    'code': 'addresses',
                    'description': 'Localisation des propriétés fondée sur les '
                                    'identifiants des adresses, habituellement le '
                                    'nom de la rue, le numéro de la maison et le '
                                    'code postal.',
                    'text': 'Addresses'},
                    {'_id': '227c2351b47f426a84a53d9beb472cfc',
                    '_tag': 'keyword:isogeo:test',
                    'code': 'test',
                    'text': 'test'}],
        'language': 'fr',
        'limitations': [{'_id': '4fbb36e8cb444857be4f07a016198620',
                        'description': '**Gras**\n'
                                        '*Italique*\t\n'
                                        '<del>Supprimé</del>\n'
                                        '<cite>Citation</cite>\n'
                                        '\n'
                                        '* Élément 1\n'
                                        '* Élément 2\n'
                                        '\n'
                                        '1. Élément 1\n'
                                        '2. Élément 2\n'
                                        '\n'
                                        '[Foo](http://foo.bar)',
                        'type': 'security'},
                        {'_id': '97dade01cb26464fa2436e0600ce5170',
                        'description': '**Gras**\n'
                                        '*Italique*\t\n'
                                        '<del>Supprimé</del>\n'
                                        '<cite>Citation</cite>\n'
                                        '\n'
                                        '* Élément 1\n'
                                        '* Élément 2\n'
                                        '\n'
                                        '1. Élément 1\n'
                                        '2. Élément 2\n'
                                        '\n'
                                        '[Foo](http://foo.bar)',
                        'directive': {'_id': '6756c1875d06446982ed941555102c72',
                                        'description': 'Aucun des articles de la loi '
                                                    'ne peut être invoqué pour '
                                                    'justifier d’une restriction '
                                                    'd’accès public.',
                                        'name': 'Pas de restriction d’accès public '
                                                'selon INSPIRE'},
                        'restriction': 'license',
                        'type': 'legal'}],
        'links': [{'_id': '7b045939f5ae4ff3ad34d73143c6da40',
                    'actions': ['download'],
                    'kind': 'data',
                    'size': 204132,
                    'title': 'BDCARTO_3-2_TOUSTHEMES_SHP_LAMB93_XE123_2016-07-18.7z',
                    'type': 'hosted',
                    'url': '/resources/43380f6c60424095b67cbd1aa9526fe4/links/7b045939f5ae4ff3ad34d73143c6da40.bin'},
                {'_id': 'e87499b29f85406ca2b2502e51fb83fd',
                    'actions': ['other'],
                    'kind': 'url',
                    'title': 'Site web isogeo',
                    'type': 'url',
                    'url': 'https://www.isogeo.com/'}],
        'modified': '2018-06-13T00:00:00+00:00',
        'published': '2018-06-14T00:00:00+00:00',
        'scale': 10000,
        'series': False,
        'serviceLayers': [{'_id': '0ab65c8fb8994d54b375399a523c7160',
                            'id': '{isogeo}DEPARTEMENT_2014',
                            'mimeTypes': [],
                            'service': {'_created': '2017-01-08T11:44:39.5080021+00:00',
                                        '_creator': {'_created': '2015-05-21T12:08:16.4295098+00:00',
                                                    '_id': '32f7e95ec4e94ca3bc1afda960003882',
                                                    '_modified': '2019-05-03T10:31:01.4796052+00:00',
                                                    '_tag': 'owner:32f7e95ec4e94ca3bc1afda960003882',
                                                    'areKeywordsRestricted': True,
                                                    'canCreateLegacyServiceLinks': True,
                                                    'canCreateMetadata': True,
                                                    'resource': {'_deleted': False,
                                                                '_id': '2a3aefc4f80347f590afe58127f6cb0f',
                                                                '_tag': 'resource:group:2a3aefc4f80347f590afe58127f6cb0f',
                                                                'addressLine1': '26 '
                                                                                'rue '
                                                                                'du '
                                                                                'faubourg '
                                                                                'Saint-Antoine',
                                                                'addressLine2': '4 '
                                                                                'éme '
                                                                                'étage',
                                                                'available': True,
                                                                'city': 'Paris',
                                                                'countryCode': 'FR',
                                                                'email': 'dev@isogeo.com',
                                                                'fax': '33 (0)9 67 46 '
                                                                        '50 06',
                                                                'name': 'Isogeo Test',
                                                                'phone': '33 (0)9 67 '
                                                                        '46 50 06',
                                                                'type': 'group',
                                                                'zipCode': '75012'},
                                                    'hasCswClient': False,
                                                    'hasScanFme': True,
                                                    'keywordsCasing': 'lowercase',
                                                    'metadataLanguage': 'fr',
                                                    'themeColor': '#4499A1'},
                                        '_id': '546049f36b9b422ca78ded118261bd8b',
                                        '_modified': '2018-12-28T14:26:25.3593871+00:00',
                                        'abstract': '**FR**\r\n'
                                                    '\r\n'
                                                    'Serveur géographique interne à '
                                                    'Isogeo et dédié aux tests et aux '
                                                    'démonstrations de la plateforme '
                                                    'et des outils liés.\r\n'
                                                    '\r\n'
                                                    '\r\n'
                                                    '**EN**\r\n'
                                                    '\r\n'
                                                    'This is an internal geospatial '
                                                    'server owned by Isogeo to '
                                                    'demonstrate integration within '
                                                    'its platform and related tools.',
                                        'created': '2018-03-22T00:00:00+00:00',
                                        'editionProfile': 'manual',
                                        'envelope': {'bbox': [-167.34375,
                                                            -55.85558211472816,
                                                            191.25,
                                                            74.73887224676959],
                                                    'coordinates': [[[-167.34375,
                                                                    -55.85558211472816],
                                                                    [-167.34375,
                                                                    74.73887224676959],
                                                                    [191.25,
                                                                    74.73887224676959],
                                                                    [191.25,
                                                                    -55.85558211472816],
                                                                    [-167.34375,
                                                                    -55.85558211472816]]],
                                                    'type': 'Polygon'},
                                        'format': 'wfs',
                                        'formatVersion': '2.0.0',
                                        'language': 'fr',
                                        'path': 'http://noisy.hq.isogeo.fr:6090/geoserver/ows',
                                        'title': 'Isogeo - Web Feature Service de '
                                                'démonstration',
                                        'type': 'service'},
                            'titles': [{'value': 'Départements - France métropolitaine '
                                                '- 2014'}]},
                        {'_id': 'd70d8a7e91ac4abba90152387b5379ea',
                            'id': 'Isogeo:DEPARTEMENT_2014',
                            'mimeTypes': [],
                            'service': {'_created': '2017-03-01T17:43:24.2102075+00:00',
                                        '_creator': {'_created': '2015-05-21T12:08:16.4295098+00:00',
                                                    '_id': '32f7e95ec4e94ca3bc1afda960003882',
                                                    '_modified': '2019-05-03T10:31:01.4796052+00:00',
                                                    '_tag': 'owner:32f7e95ec4e94ca3bc1afda960003882',
                                                    'areKeywordsRestricted': True,
                                                    'canCreateLegacyServiceLinks': True,
                                                    'canCreateMetadata': True,
                                                    'resource': {'_deleted': False,
                                                                '_id': '2a3aefc4f80347f590afe58127f6cb0f',
                                                                '_tag': 'resource:group:2a3aefc4f80347f590afe58127f6cb0f',
                                                                'addressLine1': '26 '
                                                                                'rue '
                                                                                'du '
                                                                                'faubourg '
                                                                                'Saint-Antoine',
                                                                'addressLine2': '4 '
                                                                                'éme '
                                                                                'étage',
                                                                'available': True,
                                                                'city': 'Paris',
                                                                'countryCode': 'FR',
                                                                'email': 'dev@isogeo.com',
                                                                'fax': '33 (0)9 67 46 '
                                                                        '50 06',
                                                                'name': 'Isogeo Test',
                                                                'phone': '33 (0)9 67 '
                                                                        '46 50 06',
                                                                'type': 'group',
                                                                'zipCode': '75012'},
                                                    'hasCswClient': False,
                                                    'hasScanFme': True,
                                                    'keywordsCasing': 'lowercase',
                                                    'metadataLanguage': 'fr',
                                                    'themeColor': '#4499A1'},
                                        '_id': '48867893495e4c99bb3d7043466ac236',
                                        '_modified': '2018-12-28T14:26:25.3593871+00:00',
                                        'abstract': 'Serveur WMS interne à Isogeo pour '
                                                    'les besoins de tests ou de '
                                                    'démonstration.',
                                        'editionProfile': 'manual',
                                        'format': 'wms',
                                        'formatVersion': '1.3.0',
                                        'path': 'http://noisy.hq.isogeo.fr:6090/geoserver/Isogeo/wms',
                                        'title': 'TEST - WMS Isogeo (GeoServer)',
                                        'type': 'service'},
                            'titles': [{'value': 'Départements - France métropolitaine '
                                                '- 2014'}]}],
        'specifications': [{'conformant': True,
                            'specification': {'_id': 'ec09b20d4c6b4b3b8fd637a761ebdbbf',
                                            '_tag': 'specification:isogeo:ec09b20d4c6b4b3b8fd637a761ebdbbf',
                                            'link': 'http://cnig.gouv.fr/wp-content/uploads/2014/10/141002_Standard_CNIG_CC_diffusion.pdf',
                                            'name': 'CNIG CC v2014',
                                            'published': '2014-10-02T00:00:00'}}],
        'tags': {'action:download': 'Download',
                'action:other': 'Other',
                'action:view': 'View',
                'catalog:0221b7d26b034db68ddc4210587c1d15': 'Test CSW - ODS',
                'catalog:cd06d9e914a14b9e9b3f15da1226b331': 'Test - Dawizz',
                'catalog:ec81810c932348aca9581d4000cf5634': 'Test',
                'catalog:fc4b9eb738e54c4eb16156c152f3a7d2': 'DembaCatalog',
                'conformity:inspire': None,
                'resource:group:643f1035377b4ca59da6f31a39704c34': 'Isogeo',
                'coordinate-system:2154': 'RGF93 / Lambert-93',
                'format:shp': 'ESRI Shapefile',
                'keyword:inspire-theme:addresses': 'Addresses',
                'keyword:isogeo:test': 'test',
                'license:isogeo:cdf0eecc36534cb2b49c79ad281dee65': 'ODbL 1.0 - Open '
                                                                    'Database Licence',
                'owner:32f7e95ec4e94ca3bc1afda960003882': 'Isogeo Test',
                'provider:manual': None,
                'type:vector-dataset': 'Dataset (vector)'},
        'title': 'Fiche complète',
        'topologicalConsistency': '**Gras**\n'
                                '*Italique*\t\n'
                                '<del>Supprimé</del>\n'
                                '<cite>Citation</cite>\n'
                                '\n'
                                '* Élément 1\n'
                                '* Élément 2\n'
                                '\n'
                                '1. Élément 1\n'
                                '2. Élément 2\n'
                                '\n'
                                '[Foo](http://foo.bar)',
        'type': 'vectorDataset',
        'updateFrequency': 'P1Y',
        'validFrom': '2018-06-04T00:00:00+00:00',
        'validTo': '2018-06-30T00:00:00+00:00',
        'validityComment': '**Gras**\n'
                            '*Italique*\t\n'
                            '<del>Supprimé</del>\n'
                            '<cite>Citation</cite>\n'
                            '\n'
                            '* Élément 1\n'
                            '* Élément 2\n'
                            '\n'
                            '1. Élément 1\n'
                            '2. Élément 2\n'
                            '\n'
                            '[Foo](http://foo.bar)'
    }
    ```

    """

    """
    Attributes:
      attr_types (dict): basic structure of resource attributes. {"attribute name": "attribute type"}.
      attr_crea (dict): only attributes used to POST requests. {"attribute name": "attribute type"}
      attr_map (dict): mapping between read and write attributes. {"attribute name - GET": "attribute type - POST"}
    """
    attr_types = {
        "_abilities": list,
        "_created": str,
        "_creator": dict,
        "_id": str,
        "_modified": str,
        "abstract": str,
        "collectionContext": str,
        "collectionMethod": str,
        "conditions": list,
        "contacts": list,
        "coordinateSystem": dict,
        "created": str,
        "distance": float,
        "editionProfile": str,
        "encoding": str,
        "envelope": dict,
        "events": dict,
        "featureAttributes": dict,
        "features": int,
        "format": str,
        "formatVersion": str,
        "geometry": str,
        "keywords": list,
        "language": str,
        "limitations": list,
        "links": list,
        "modified": str,
        "name": str,
        "path": str,
        "published": str,
        "scale": int,
        "series": bool,
        "serviceLayers": list,
        "specifications": list,
        "tags": list,
        "title": str,
        "topologicalConsistency": str,
        "type": str,
        "updateFrequency": str,
        "validFrom": str,
        "validTo": str,
        "validityComment": str,
    }

    attr_crea = {
        # "_abilities": list,
        # "_creator": dict,
        # "_id": str,
        "abstract": str,
        "collectionContext": str,
        # "collectionMethod": str,
        # "created": str,
        # "distance": float,
        # "editionProfile": str,
        "encoding": str,
        # "features": int,
        "format": str,
        "formatVersion": str,
        # "geometry": str,
        # "keywords": list,
        "language": str,
        # "modified": str,
        # "name": str,
        "path": str,
        "precision": str,
        # "published": str,
        "scale": int,
        "series": bool,
        "title": str,
        "topologicalConsistency": str,
        "type": str,
        # "updateFrequency": str,
        # "validFrom": str,
        # "validTo": str,
        # "validityComment": str,
    }

    attr_map = {
        "coordinateSystem": "coordinate-system",
        "featureAttributes": "feature-attributes",
    }

    def __init__(
        self,
        _abilities: list = None,
        _created: str = None,
        _creator: dict = None,
        _id: str = None,
        _modified: str = None,
        abstract: str = None,
        collectionContext: str = None,
        collectionMethod: str = None,
        conditions: list = None,
        contacts: list = None,
        coordinateSystem: dict = None,
        created: str = None,
        distance: float = None,
        editionProfile: str = None,
        encoding: str = None,
        envelope: dict = None,
        events: dict = None,
        featureAttributes: dict = None,
        features: int = None,
        format: str = None,
        formatVersion: str = None,
        geometry: str = None,
        keywords: list = None,
        language: str = None,
        limitations: list = None,
        links: list = None,
        modified: str = None,
        name: str = None,
        path: str = None,
        precision: str = None,
        published: str = None,
        scale: int = None,
        series: bool = None,
        serviceLayers: list = None,
        specifications: list = None,
        tags: list = None,
        title: str = None,
        topologicalConsistency: str = None,
        type: str = None,
        updateFrequency: str = None,
        validFrom: str = None,
        validTo: str = None,
        validityComment: str = None,
    ):
        """Resource model"""

        # default values for the object attributes/properties
        self.__abilities = None
        self.__created = None
        self.__creator = None
        self.__id = None
        self.__modified = None
        self._abstract = None
        self._collectionContext = None
        self._collectionMethod = None
        self._conditions = None
        self._contacts = None
        self._coordinateSystem = None
        self._created = None
        self._distance = None
        self._editionProfile = None
        self._encoding = None
        self._envelope = None
        self._events = None
        self._featureAttributes = None
        self._features = None
        self._format = None
        self._formatVersion = None
        self._geometry = None
        self._keywords = None
        self._language = None
        self._limitations = None
        self._links = None
        self._modified = None
        self._name = None
        self._path = None
        self._precision = None
        self._published = None
        self._scale = None
        self._series = None
        self._serviceLayers = None
        self._specifications = None
        self._tags = None
        self._title = None
        self._topologicalConsistency = None
        self._type = None
        self._updateFrequency = None
        self._validFrom = None
        self._validTo = None
        self._validityComment = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _abilities is not None:
            self.__abilities = _abilities
        if _created is not None:
            self.__created = _created
        if _creator is not None:
            self.__creator = _creator
        if _id is not None:
            self.__id = _id
        if _modified is not None:
            self.__modified = _modified
        if abstract is not None:
            self._abstract = abstract
        if collectionContext is not None:
            self._collectionContext = collectionContext
        if collectionMethod is not None:
            self._collectionMethod = collectionMethod
        if conditions is not None:
            self._conditions = conditions
        if contacts is not None:
            self._contacts = contacts
        if coordinateSystem is not None:
            self._coordinateSystem = coordinateSystem
        if created is not None:
            self._created = created
        if distance is not None:
            self._distance = distance
        if editionProfile is not None:
            self._editionProfile = editionProfile
        if encoding is not None:
            self._encoding = encoding
        if envelope is not None:
            self._envelope = envelope
        if events is not None:
            self._events = events
        if featureAttributes is not None:
            self._featureAttributes = featureAttributes
        if features is not None:
            self._features = features
        if format is not None:
            self._format = format
        if geometry is not None:
            self._geometry = geometry
        if keywords is not None:
            self._keywords = keywords
        if language is not None:
            self._language = language
        if limitations is not None:
            self._limitations = limitations
        if links is not None:
            self._links = links
        if modified is not None:
            self._modified = modified
        if path is not None:
            self._path = path
        if precision is not None:
            self._precision = precision
        if published is not None:
            self._published = published
        if scale is not None:
            self._scale = scale
        if serviceLayers is not None:
            self._serviceLayers = serviceLayers
        if specifications is not None:
            self._specifications = specifications
        if tags is not None:
            self._tags = tags
        if title is not None:
            self._title = title
        if topologicalConsistency is not None:
            self._topologicalConsistency = topologicalConsistency
        if type is not None:
            self._type = type
        if updateFrequency is not None:
            self._updateFrequency = updateFrequency
        if validFrom is not None:
            self._validFrom = validFrom
        if validTo is not None:
            self._validTo = validTo
        if validityComment is not None:
            self._validityComment = validityComment

    # -- PROPERTIES --------------------------------------------------------------------
    # abilities of the user related to the metadata
    @property
    def _abilities(self) -> str:
        """Gets the abilities of this Catalog.

        :return: The abilities of this Catalog.
        :rtype: str
        """
        return self.__abilities

    # resource owner
    @property
    def _creator(self) -> str:
        """Gets the creator of this Catalog.

        :return: The creator of this Metadata.
        :rtype: str
        """
        return self.__creator

    # resource UUID
    @property
    def _id(self) -> str:
        """Gets the id of this Resource.

        :return: The id of this Resource.
        :rtype: str
        """
        return self.__id

    @_id.setter
    def _id(self, _id: str):
        """Sets the id of this Resource.

        :param str id: The id of this Resource.
        """

        self.__id = _id

    # metadata description
    @property
    def abstract(self) -> str:
        """Gets the abstract.

        :return: The abstract of this Resource.
        :rtype: str
        """
        return self._abstract

    @abstract.setter
    def abstract(self, abstract: str):
        """Sets the abstract used into Isogeo filters of this Resource.

        :param str abstract: the abstract of this Resource.
        """

        self._abstract = abstract

    # collection context
    @property
    def collectionContext(self) -> str:
        """Gets the collectionContext of this Resource.

        :return: The collectionContext of this Resource.
        :rtype: str
        """
        return self._collectionContext

    @collectionContext.setter
    def collectionContext(self, collectionContext: str):
        """Sets the first line of the address of this Resource.

        :param str collectionContext: The first address line of this Resource.
        """

        self._collectionContext = collectionContext

    # collection method
    @property
    def collectionMethod(self) -> str:
        """Gets the collectionMethod of this Resource.

        :return: The collectionMethod of this Resource.
        :rtype: str
        """
        return self._collectionMethod

    @collectionMethod.setter
    def collectionMethod(self, collectionMethod: str):
        """Sets the first line of the address of this Resource.

        :param str collectionMethod: The first address line of this Resource.
        """

        self._collectionMethod = collectionMethod

    # CGUs
    @property
    def conditions(self) -> str:
        """Gets the conditions of this Resource.

        :return: The conditions of this Resource.
        :rtype: str
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions: str):
        """Sets the first line of the address of this Resource.

        :param str conditions: The first address line of this Resource.
        """

        self._conditions = conditions

    # contacts
    @property
    def contacts(self) -> str:
        """Gets the contacts of this Resource.

        :return: The contacts of this Resource.
        :rtype: str
        """
        return self._contacts

    @contacts.setter
    def contacts(self, contacts: str):
        """Sets the first line of the address of this Resource.

        :param str contacts: The first address line of this Resource.
        """

        self._contacts = contacts

    # coordinateSystem
    @property
    def coordinateSystem(self) -> str:
        """Gets the coordinateSystem of this Resource.

        :return: The coordinateSystem of this Resource.
        :rtype: str
        """
        return self._coordinateSystem

    @coordinateSystem.setter
    def coordinateSystem(self, coordinateSystem: str):
        """Sets the first line of the address of this Resource.

        :param str coordinateSystem: The first address line of this Resource.
        """

        self._coordinateSystem = coordinateSystem

    # created
    @property
    def created(self) -> str:
        """Gets the created of this Resource.

        :return: The created of this Resource.
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created: str):
        """Sets the first line of the address of this Resource.

        :param str created: The first address line of this Resource.
        """

        self._created = created

    # distance
    @property
    def distance(self) -> str:
        """Gets the distance of this Resource.

        :return: The distance of this Resource.
        :rtype: str
        """
        return self._distance

    @distance.setter
    def distance(self, distance: str):
        """Sets the first line of the address of this Resource.

        :param str distance: The first address line of this Resource.
        """

        self._distance = distance

    # editionProfile
    @property
    def editionProfile(self) -> str:
        """Gets the editionProfile of this Resource.

        :return: The editionProfile of this Resource.
        :rtype: str
        """
        return self._editionProfile

    @editionProfile.setter
    def editionProfile(self, editionProfile: str):
        """Sets the first line of the address of this Resource.

        :param str editionProfile: The first address line of this Resource.
        """

        self._editionProfile = editionProfile

    # encoding
    @property
    def encoding(self) -> str:
        """Gets the encoding of this Resource.

        :return: The encoding of this Resource.
        :rtype: str
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: str):
        """Sets the first line of the address of this Resource.

        :param str encoding: The first address line of this Resource.
        """

        self._encoding = encoding

    # envelope
    @property
    def envelope(self) -> str:
        """Gets the envelope of this Resource.

        :return: The envelope of this Resource.
        :rtype: str
        """
        return self._envelope

    @envelope.setter
    def envelope(self, envelope: str):
        """Sets the first line of the address of this Resource.

        :param str envelope: The first address line of this Resource.
        """

        self._envelope = envelope

    # events
    @property
    def events(self) -> str:
        """Gets the events of this Resource.

        :return: The events of this Resource.
        :rtype: str
        """
        return self._events

    @events.setter
    def events(self, events: str):
        """Sets the first line of the address of this Resource.

        :param str events: The first address line of this Resource.
        """

        self._events = events

    # featureAttributes
    @property
    def featureAttributes(self) -> str:
        """Gets the featureAttributes of this Resource.

        :return: The featureAttributes of this Resource.
        :rtype: str
        """
        return self._featureAttributes

    @featureAttributes.setter
    def featureAttributes(self, featureAttributes: str):
        """Sets the first line of the address of this Resource.

        :param str featureAttributes: The first address line of this Resource.
        """

        self._featureAttributes = featureAttributes

    # features
    @property
    def features(self) -> str:
        """Gets the features of this Resource.

        :return: The features of this Resource.
        :rtype: str
        """
        return self._features

    @features.setter
    def features(self, features: str):
        """Sets the first line of the address of this Resource.

        :param str features: The first address line of this Resource.
        """

        self._features = features

    # format
    @property
    def format(self) -> str:
        """Gets the format of this Resource.

        :return: The format of this Resource.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format: str):
        """Sets the first line of the address of this Resource.

        :param str format: The first address line of this Resource.
        """

        self._format = format

    # formatVersion
    @property
    def formatVersion(self) -> str:
        """Gets the formatVersion of this Resource.

        :return: The formatVersion of this Resource.
        :rtype: str
        """
        return self._formatVersion

    @formatVersion.setter
    def formatVersion(self, formatVersion: str):
        """Sets the first line of the address of this Resource.

        :param str formatVersion: The first address line of this Resource.
        """

        self._formatVersion = formatVersion

    # geometry
    @property
    def geometry(self) -> str:
        """Gets the geometry of this Resource.

        :return: The geometry of this Resource.
        :rtype: str
        """
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: str):
        """Sets the first line of the address of this Resource.

        :param str geometry: The first address line of this Resource.
        """

        self._geometry = geometry

    # keywords
    @property
    def keywords(self) -> str:
        """Gets the keywords of this Resource.

        :return: The keywords of this Resource.
        :rtype: str
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords: str):
        """Sets the first line of the address of this Resource.

        :param str keywords: The first address line of this Resource.
        """

        self._keywords = keywords

    # language
    @property
    def language(self) -> str:
        """Gets the language of this Resource.

        :return: The language of this Resource.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language: str):
        """Sets the first line of the address of this Resource.

        :param str language: The first address line of this Resource.
        """

        self._language = language

    # limitations
    @property
    def limitations(self) -> str:
        """Gets the limitations of this Resource.

        :return: The limitations of this Resource.
        :rtype: str
        """
        return self._limitations

    @limitations.setter
    def limitations(self, limitations: str):
        """Sets the first line of the address of this Resource.

        :param str limitations: The first address line of this Resource.
        """

        self._limitations = limitations

    # links
    @property
    def links(self) -> str:
        """Gets the links of this Resource.

        :return: The links of this Resource.
        :rtype: str
        """
        return self._links

    @links.setter
    def links(self, links: str):
        """Sets the first line of the address of this Resource.

        :param str links: The first address line of this Resource.
        """

        self._links = links

    # modified
    @property
    def modified(self) -> str:
        """Gets the modified of this Resource.

        :return: The modified of this Resource.
        :rtype: str
        """
        return self._modified

    @modified.setter
    def modified(self, modified: str):
        """Sets the first line of the address of this Resource.

        :param str modified: The first address line of this Resource.
        """

        self._modified = modified

    # name
    @property
    def name(self) -> str:
        """Gets the name of this Resource.

        :return: The name of this Resource.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets technical name of the Resource.

        :param str name: technical name this Resource.
        """

        self._name = name

    # path
    @property
    def path(self) -> str:
        """Gets the path of this Resource.

        :return: The path of this Resource.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path: str):
        """Sets the first line of the address of this Resource.

        :param str path: The first address line of this Resource.
        """

        self._path = path

    # precision
    @property
    def precision(self) -> str:
        """Gets the precision of this Resource.

        :return: The precision of this Resource.
        :rtype: str
        """
        return self._precision

    @precision.setter
    def precision(self, precision: str):
        """Sets the first line of the address of this Resource.

        :param str precision: The first address line of this Resource.
        """

        self._precision = precision

    # published
    @property
    def published(self) -> str:
        """Gets the published of this Resource.

        :return: The published of this Resource.
        :rtype: str
        """
        return self._published

    @published.setter
    def published(self, published: str):
        """Sets the first line of the address of this Resource.

        :param str published: The first address line of this Resource.
        """

        self._published = published

    # scale
    @property
    def scale(self) -> str:
        """Gets the scale of this Resource.

        :return: The scale of this Resource.
        :rtype: str
        """
        return self._scale

    @scale.setter
    def scale(self, scale: str):
        """Sets the first line of the address of this Resource.

        :param str scale: The first address line of this Resource.
        """

        self._scale = scale

    # series
    @property
    def series(self) -> str:
        """Gets the series of this Resource.

        :return: The series of this Resource.
        :rtype: str
        """
        return self._series

    @series.setter
    def series(self, series: str):
        """Sets the first line of the address of this Resource.

        :param str series: The first address line of this Resource.
        """

        self._series = series

    # serviceLayers
    @property
    def serviceLayers(self) -> str:
        """Gets the serviceLayers of this Resource.

        :return: The serviceLayers of this Resource.
        :rtype: str
        """
        return self._serviceLayers

    @serviceLayers.setter
    def serviceLayers(self, serviceLayers: str):
        """Sets the first line of the address of this Resource.

        :param str serviceLayers: The first address line of this Resource.
        """

        self._serviceLayers = serviceLayers

    # specifications
    @property
    def specifications(self) -> str:
        """Gets the specifications of this Resource.

        :return: The specifications of this Resource.
        :rtype: str
        """
        return self._specifications

    @specifications.setter
    def specifications(self, specifications: str):
        """Sets the first line of the address of this Resource.

        :param str specifications: The first address line of this Resource.
        """

        self._specifications = specifications

    # tags
    @property
    def tags(self) -> str:
        """Gets the tags of this Resource.

        :return: The tags of this Resource.
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags: str):
        """Sets the first line of the address of this Resource.

        :param str tags: The first address line of this Resource.
        """

        self._tags = tags

    # title
    @property
    def title(self) -> str:
        """Gets the title of this Resource.

        :return: The title of this Resource.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the first line of the address of this Resource.

        :param str title: The first address line of this Resource.
        """

        self._title = title

    # topologicalConsistency
    @property
    def topologicalConsistency(self) -> str:
        """Gets the topologicalConsistency of this Resource.

        :return: The topologicalConsistency of this Resource.
        :rtype: str
        """
        return self._topologicalConsistency

    @topologicalConsistency.setter
    def topologicalConsistency(self, topologicalConsistency: str):
        """Sets the first line of the address of this Resource.

        :param str topologicalConsistency: The first address line of this Resource.
        """

        self._topologicalConsistency = topologicalConsistency

    # type
    @property
    def type(self) -> str:
        """Gets the type of this Resource.

        :return: The type of this Resource.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Resource.

        :param str type: The type of this Resource.
        """

        self._type = type

    # updateFrequency
    @property
    def updateFrequency(self) -> str:
        """Gets the updateFrequency of this Resource.

        :return: The updateFrequency of this Resource.
        :rtype: str
        """
        return self._updateFrequency

    @updateFrequency.setter
    def updateFrequency(self, updateFrequency: str):
        """Sets the first line of the address of this Resource.

        :param str updateFrequency: The first address line of this Resource.
        """

        self._updateFrequency = updateFrequency

    # validFrom
    @property
    def validFrom(self) -> str:
        """Gets the validFrom of this Resource.

        :return: The validFrom of this Resource.
        :rtype: str
        """
        return self._validFrom

    @validFrom.setter
    def validFrom(self, validFrom: str):
        """Sets the first line of the address of this Resource.

        :param str validFrom: The first address line of this Resource.
        """

        self._validFrom = validFrom

    # validTo
    @property
    def validTo(self) -> str:
        """Gets the validTo of this Resource.

        :return: The validTo of this Resource.
        :rtype: str
        """
        return self._validTo

    @validTo.setter
    def validTo(self, validTo: str):
        """Sets the first line of the address of this Resource.

        :param str validTo: The first address line of this Resource.
        """

        self._validTo = validTo

    # validityComment
    @property
    def validityComment(self) -> str:
        """Gets the validityComment of this Resource.

        :return: The validityComment of this Resource.
        :rtype: str
        """
        return self._validityComment

    @validityComment.setter
    def validityComment(self, validityComment: str):
        """Sets the first line of the address of this Resource.

        :param str validityComment: The first address line of this Resource.
        """

        self._validityComment = validityComment

    # -- METHODS -----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.attr_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(Resource, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_dict_creation(self) -> dict:
        """Returns the model properties as a dict structured for creation purpose (POST)"""
        result = {}

        for attr, _ in self.attr_crea.items():
            # get attribute value
            value = getattr(self, attr)
            # switch attribute name for creation purpose
            if attr in self.attr_map:
                attr = self.attr_map.get(attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(Resource, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, Resource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal"""
        return not self == other


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    md = Resource()
    print(md)
