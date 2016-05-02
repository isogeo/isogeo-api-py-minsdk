Python minimalist SDK to use Isogeo REST API
==========

Lib still under development.

Installing
==========

For developers:

.. code-block:: shell

    git clone git@github.com:Guts/isogeo-api-py-minsdk.git
    cd isogeo-api-py-minsdk
    python setup.py install

Getting Help
============

There is a basic documentation about the  `Isogeo API <https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing>`_.

Sample
==========================

.. code-block:: python

    from isogeo_pysdk import Isogeo
    isogeo = Isogeo(client_id=share_id,
                    client_secret=share_token)

    # check which sub resources are available
    print(isogeo.sub_resources_available)
    print(isogeo.tr_types_label_fr)

    # getting a token
    jeton = isogeo.connect()

    search = isogeo.search(jeton)

    print(search.keys())
    print(search.get('query'))
    print("Total count of metadatas shared: ", search.get("total"))
    print("Count of resources got by request: {}\n".format(len(search.get("results"))))
