========
Usage
========


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
    search = isogeo.search(token, page_size=0, whole_share=0, augment=1)

    # through search tags
    print(search.get("tags"))

    # through attributes
    print(isogeo.shares_id)


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
    from isogeo_pysdk import Isogeo, IsogeoUtils as utils

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
Get CSW GetRecord for a metadata
--------------------------------

.. code-block:: python

    from isogeo_pysdk import IsogeoUtils
    utils = IsogeoUtils()
    csw_getrec_url = utils.get_view_url(webapp="csw_getrec",
                                        md_uuid_urn=self.uuid_urnIsogeo,
                                        share_id="1e07910d365449b59b6596a9b428ecd9",
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
