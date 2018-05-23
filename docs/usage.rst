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
