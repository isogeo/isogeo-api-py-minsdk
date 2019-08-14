========
Usage
========

.. RST cheatsheet: https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst

Get application properties as attributes
----------------------------------------

.. code-block:: python

    from isogeo_pysdk import Isogeo

    # authenticate your client application
    isogeo = Isogeo(client_id=app_id,
                    client_secret=app_secret)

    # get the token
    token = isogeo.connect()

    # add properties as attribute
    isogeo.get_app_properties(token)

	# accessing properties
    print(isogeo.app_properties)


    # structure of returned dict
    app = {"admin_url": str,
           "creation_date": str,
           "last_update": str,
           "name": str,
           "type": str,
           "kind": str,
           "url": str
           }


Add shares tags to search response and as attributes
----------------------------------------------------

.. code-block:: python

    from isogeo_pysdk import Isogeo

    # authenticate your client application
    isogeo = Isogeo(client_id=app_id,
                    client_secret=app_secret)

    # get the token
    token = isogeo.connect()

    # set augment option on True
    search = isogeo.search(token, page_size=0, whole_results=0, augment=1)

    # through search tags
    print(search.get("tags"))

    # through attributes
    print(isogeo.shares_id)


Get OpenCatalog URL for a share
-------------------------------

OpenCatalog is an online metadata browser generated on Isogeo platform.
As a third-party application, it can be set or not in a share.

Here is how to check if it's set or not in a share.
The share UUID is required: 2 methods are proposed to retrieve it.


.. code-block:: python

    from isogeo_pysdk import Isogeo

    # authenticate your client application
    isogeo = Isogeo(client_id=app_id,
                    client_secret=app_secret)

    # get the token
    token = isogeo.connect()

    ## -- METHOD 1 - by shares route ------------------------------------------
    # get shares
    shares = isogeo.shares(token)

    # get first share id
    share_id = shares[0].get("_id")

    ## -- METHOD 2 - by augmented search --------------------------------------
    # empty search
    search = isogeo.search(token,
                           page_size=0,     # get only tags, not results
                           whole_results=0,   # do not retrieve the whole application scope
                           augment=1    # -> this parameter is what we need
                           )

    # get share id from tags splitting dict key
    share_id = list(isogeo.shares_id.keys())[0].split(":")[1]

    ## -- ONCE SHARE ID RETRIEVED ---------------------------------------------

    # make an augmented share request
    share_augmented = isogeo.share(token, share_id, augment=1)

    if "oc_url" in share_augmented:
        print("OpenCatalog is set: {}"
              .format(share_augmented.get("oc_url"))
              )
    else:
        print("OpenCatalog is not set in this share")


Check if a metadata is in a share
---------------------------------

With the augmented share, it's also possible to check if a metadata is present within.

.. code-block:: python

    # -- see above to get augmented share
    # get a metadata
    search = isogeo.search(token,
                           page_size=1,     # get only one result
                           whole_results=0    # do not retrieve the whole application scope
                           )
    md = search.get("results")[0]

    # check
    if md.get("_id") in share_augmented.get("mds_ids"):
        print("Metadata is present in this share")
    else:
        print("No present").


Load API credentials from a JSON or INI file
--------------------------------------------

Isogeo delivers API credentials in a JSON file. Its structure depends on the kind of oAuth2 application you are developing. Please referer to the API documentation to know more about different types of oAuth2 application.

For example, here is the JSON structure for a "workgroup" application:

.. code-block:: json

    {
    "web": {
        "client_id": "python-minimalist-sdk-test-uuid-1a2b3c4d5e6f7g8h9i0j11k12l",
        "client_secret": "application-secret-1a2b3c4d5e6f7g8h9i0j11k12l13m14n15o16p17Q18rS",
        "auth_uri": "https://id.api.isogeo.com/oauth/authorize",
        "token_uri": "https://id.api.isogeo.com/oauth/token"
        }
    }

The module isogeo_pysdk.utils comes with a method to load automatically credentials from JSON and INI files:

.. code-block:: python

    # load package
    from isogeo_pysdk import Isogeo, IsogeoUtils

    # instanciate IsogeoUtils as utils
    utils = IsogeoUtils()

    # load from file
    api_credentials = utils.credentials_loader("client_secrets_group.json")

    # could also be:
    # api_credentials = utils.credentials_loader("client_secrets_user.json")
    # api_credentials = utils.credentials_loader("client_secrets.ini")

    # authenticate your client application
    isogeo = Isogeo(client_id=api_credentials.get("client_id"),
                    client_secret=api_credentials.get("client_secret")
                    )

    # get the token
    token = isogeo.connect()

Keys of returned dict:
       
    - auth_mode
    - client_id
    - client_secret
    - scopes
    - uri_auth
    - uri_base
    - uri_redirect
    - uri_token

URL Builder for web applications
--------------------------------

Isogeo metadata can be displyed in others web applications. Some webapps are built-in:
    - OpenCatalog (oc)
    - Data portal by PixUp (pixup_portal)
    - CSW GetCapabilities (for a share)
    - CSW GetRecords (for a metadata)

It's also possible to register a custom web app (see below).

---------------------------------------
Get URL to online editor for a metadata
---------------------------------------

A metadata can only be edited by an authenticated Isogeo user (with editor level at least). A built-in method make it easy to contruct it:

.. code-block:: python

    from isogeo_pysdk import IsogeoUtils
    utils = IsogeoUtils()
    url = utils.get_edit_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                             md_type="vector-dataset",
                             owner_id="32f7e95ec4e94ca3bc1afda960003882",
                             tab="attributes")

----------------------------------
Get OpenCatalog URL for a metadata
----------------------------------

.. code-block:: python

    from isogeo_pysdk import IsogeoUtils
    utils = IsogeoUtils()
    oc_url = utils.get_view_url(webapp="oc",
                                md_id="0269803d50c446b09f5060ef7fe3e22b",
                                share_id="1e07910d365449b59b6596a9b428ecd9",
                                share_token="TokenOhDearToken")

-----------------------------------
Get CSW GetCapabilities for a share
-----------------------------------

.. code-block:: python

    from isogeo_pysdk import IsogeoUtils
    utils = IsogeoUtils()
    csw_getcap_url = utils.get_view_url(webapp="csw_getcap",
                                        share_id="1e07910d365449b59b6596a9b428ecd9",
                                        share_token="TokenOhDearToken")

--------------------------------
Get CSW GetRecords for a share
--------------------------------

.. code-block:: python

    from isogeo_pysdk import IsogeoUtils
    utils = IsogeoUtils()

    csw_getrecords_url = utils.get_view_url(webapp="csw_getrecords",
                                            share_id="ShareUniqueIdentifier",
                                            share_token="TokenOhDearToken")

--------------------------------
Get CSW GetRecordById for a metadata
--------------------------------

.. code-block:: python

    from isogeo_pysdk import IsogeoUtils
    utils = IsogeoUtils()

    uuid_md_source = "82e73458e29a4edbaf8bfce9e16fa78b"

    csw_getrecord_url = utils.get_view_url(webapp="csw_getrec",
                                           md_uuid_urn=utils.convert_uuid(uuid_md_source, 2),
                                           share_id="ShareUniqueIdentifier",
                                           share_token="TokenOhDearToken")

------------------------------------
Register a custom webapp and get URL
------------------------------------

.. code-block:: python

    from isogeo_pysdk import IsogeoUtils
    utils = IsogeoUtils()
    # register the web app
    utils.register_webapp(webapp_name="PPIGE v3",
                          webapp_args=["md_id", ],
                          webapp_url="https://www.ppige-npdc.fr/portail/geocatalogue?uuid={md_id}")
    # get url
    custom_url = utils.get_view_url(md_id="0269803d50c446b09f5060ef7fe3e22b",
                                    webapp="PPIGE v3")


-----

Download metadata as XML ISO 19139
----------------------------------

In Isogeo, every metadata resource can be downloaded in its XML version (ISO 19139 compliant). The Python SDK package inclue a shortcut method:

.. code-block:: python

    from isogeo_pysdk import Isogeo

    # authenticate your client application
    isogeo = Isogeo(client_id=app_id,
                    client_secret=app_secret)

    # get the token
    token = isogeo.connect()

    # search metadata
    search_to_be_exported = isogeo.search(token,
                                          page_size=10,
                                          query="type:dataset",
                                          whole_results=0
                                          )

    # loop on results and export
    for md in search_to_be_exported.get("results"):
        title = md.get('title')
        xml_stream = isogeo.xml19139(token,
                                     md.get("_id")
                                     )

        with open("{}.xml".format(title), 'wb') as fd:
            for block in xml_stream.iter_content(1024):
                fd.write(block)


Others examples:

- `Batch export into XML within Isogeo to Office application <https://github.com/isogeo/isogeo-2-office/blob/master/modules/threads.py#L253-L330>`_.
- `Batch export into XML in the package sample <https://github.com/isogeo/isogeo-api-py-minsdk/blob/master/isogeo_pysdk/samples/export_batch_xml19139.py>`_.


Download hosted data from Isogeo cloud
--------------------------------------

Administrators and editors can link raw data and docs (.zip, .pdf...) to metadata to allow final users to access the data. To do that, it's possible to upload data to Isogeo cloud (Azure blob storage).Through the API, it's possible to download these data:

.. code-block:: python

    from isogeo_pysdk import Isogeo

    # authenticate your client application
    isogeo = Isogeo(client_id=app_id,
                    client_secret=app_secret)

    # get the token
    token = isogeo.connect()

    # search with _include = links and action = download
    latest_data_modified = isogeo.search(token,
                                         page_size=10,
                                         order_by="modified",
                                         whole_results=0,
                                         query="action:download",
                                         include=["links"],
                                         )

    # parse links and download hosted data recursively
    for md in latest_data_modified.get("results"):
        for link in filter(lambda x: x.get("type") == "hosted", md.get("links")):
            dl_stream = isogeo.dl_hosted(token,
                                         resource_link=link)
            filename = re.sub(r'[\\/*?:"<>|]', "", dl_stream[1])
            with open(filename, 'wb') as fd:
                for block in dl_stream[0].iter_content(1024):
                    fd.write(block)

Example:

- `Batch export hosted data in the package sample <https://github.com/isogeo/isogeo-api-py-minsdk/blob/master/isogeo_pysdk/samples/download_batch_hosted_data.py>`_.

