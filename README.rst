|Version| |Travis_Build_Status| |AzureDevOps_Build_Status| |coverage| |rtdocs| |compat_py27| |compat_py34| |compat_py35| |compat_py36|

Isogeo API Python SDK
=====================

A Python package to use Isogeo REST API.

Getting API keys
================

API keys are required to use it. `Send us your request by email <mailto:projects+api@isogeo.com>`_.

Getting Help
------------

There is a basic documentation about the  `Isogeo API <https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing>`_.

Installing
----------

To use:

::

    pip install --user isogeo-pysdk

For developers:

.. code-block:: console

    git clone git@github.com:isogeo/isogeo-api-py-minsdk.git
    cd isogeo-api-py-minsdk
    python setup.py install

Quickstart
----------

.. code-block:: python

    from isogeo_pysdk import Isogeo

    # authenticate your client application
    isogeo = Isogeo(client_id=app_id,
                    client_secret=app_secret)

    # get the token
    token = isogeo.connect()

    # search within catalogs shared to the application
    search = isogeo.search(token)

    # print some statements
    print(isogeo.SUBRESOURCES)  # available sub resources
    print("Search __dict__ keys: ", search.keys())  # search response basic structure
    print("Search query parameters: ", search.get('query'))  # search response query passed
    print("Total count of metadatas shared: ", search.get("total"))  # total of available resources
    print("Count of resources got by request: {}\n".format(len(search.get("results"))))  # total of resources returned by search request

Samples are available in `the source repository <https://github.com/isogeo/isogeo-api-py-minsdk/tree/master/isogeo_pysdk/samples>`_.

For more details, please have a look to the documentation on `Read the Docs <http://isogeo-api-pysdk.readthedocs.io/en/latest/>`_.

Tests
=====

Tests are performed for each published commit by `Travis <https://travis-ci.org/isogeo/isogeo-api-py-minsdk>`_

To run tests:

.. code-block:: shell

    pip install --upgrade -r tests/requirements_test.txt
    python setup.py install
    python -m unittest discover

Or using the `included Powershell script <https://github.com/isogeo/isogeo-api-py-minsdk/blob/master/tool_test_coverage.ps1>`_:

.. code-block:: powershell

    .\tool_test_coverage.ps1

Build
=====

To package and upload:

.. code-block:: powershell

    .\tool_build_upload.ps1

To build docs:

.. code-block:: powershell

    .\tool_docs_build.ps1


.. |Version| image:: https://badge.fury.io/py/isogeo-pysdk.svg
   :target: https://badge.fury.io/py/isogeo-pysdk
   :alt: PyPI version

.. |Travis_Build_Status| image:: https://travis-ci.org/isogeo/isogeo-api-py-minsdk.svg?branch=master
   :target: https://travis-ci.org/isogeo/isogeo-api-py-minsdk
   :alt: Travis build status

.. |AzureDevOps_Build_Status| image:: https://dev.azure.com/isogeo/Python%20SDK/_apis/build/status/isogeo.isogeo-api-py-minsdk?branchName=master
   :target: https://dev.azure.com/isogeo/Python%20SDK/_build/latest?definitionId=3&branchName=master
   :alt: Azure DevOps build status

.. |coverage| image:: https://codecov.io/gh/isogeo/isogeo-api-py-minsdk/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/isogeo/isogeo-api-py-minsdk
   :alt: Codecov - Coverage status

.. |compat_py27| image:: https://img.shields.io/badge/python-2.7-blue.svg
   :target: https://badge.fury.io/py/isogeo-pysdk
   :alt: Python 2.7.x compatiblity

.. |compat_py34| image:: https://img.shields.io/badge/python-3.4-blue.svg
   :target: https://badge.fury.io/py/isogeo-pysdk
   :alt: Python 3.4.x compatiblity

.. |compat_py35| image:: https://img.shields.io/badge/python-3.5-blue.svg
   :target: https://badge.fury.io/py/isogeo-pysdk
   :alt: Python 3.5.x compatiblity

.. |compat_py36| image:: https://img.shields.io/badge/python-3.6-blue.svg
   :target: https://badge.fury.io/py/isogeo-pysdk
   :alt: Python 3.6.x compatiblity

.. |rtdocs| image:: https://readthedocs.org/projects/isogeo-api-pysdk/badge/?version=latest
   :target: http://isogeo-api-pysdk.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
