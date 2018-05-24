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
                    client_secret=app_secret.get("client_secret")
                    )

    # get the token
    token = isogeo.connect()
