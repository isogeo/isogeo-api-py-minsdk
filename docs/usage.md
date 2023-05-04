# Usage

## Manipulate shares

Shares are the features allowing to manage access to metadata catalogs via applications such as GIS plugins or Isogeo2office.

### Get informations about shares (2 methods)

There are several ways to obtain more or less detailed informations about the shares accessible to an API client.

```python
from isogeo_pysdk import Isogeo

# authenticate your client application
isogeo = Isogeo(
    client_id=app_id,
    client_secret=app_secret,
    auto_refresh_url=isogeo_token_uri,
)

# get the token
isogeo.connect()

# -- BASIC INFORMATIONS ------------------------------------------
# by making a search
search = isogeo.search(page_size=0, whole_results=0, augment=1)  # set augment option on True
# retieving shares uuid and name from search tags
shares_basic = ["{}:{}".format(k, v) for k, v in search.tags.items() if k.startswith('share:')]
print(shares_basic)

# -- DETAILED INFORMATIONS ---------------------------------------
# through API client attribute
shares_detailed = isogeo._shares
print(shares_detailed)

# properly closing connection
isogeo.close()
```

### Get OpenCatalog URL for a share

OpenCatalog is an online metadata browser generated on Isogeo platform.
As a third-party application, it can be set or not in a share.

Here is how to check if it's set or not in a share.

```python
from isogeo_pysdk import Isogeo

# authenticate your client application
isogeo = Isogeo(
    client_id=app_id,
    client_secret=app_secret,
    auto_refresh_url=isogeo_token_uri
)

# get the token
isogeo.connect()

# -- RETRIEVE A SHARE UUID USING SEARCH ROUTE ------------------------------------------
# get a list of detailed informations about shares accessible by the API client
shares = isogeo.share.listing()

# get one share UUID in the list
share_id = shares[0].get("_id")

# -- ONCE SHARE UUID RETRIEVED ---------------------------------------------
# make an augmented share request
share_augmented = isogeo.share.get(share_id)

if share_augmented.opencatalog_url() is not None:
    print("OpenCatalog is set: {}".format(share_augmented.opencatalog_url()))
else:
    print("OpenCatalog is not set in this share")

```

### Check if a metadata is in a share

With the augmented share, it's also possible to check if a metadata is present within.

```python
# -- see above to get augmented share

# get a metadata
search = isogeo.search(
    page_size=1,     # get only one result
    whole_results=0    # do not retrieve the whole application scope
)
# retrieve metadata uuid
md_id = md_search.results[0].get("_id")

# make a search on metadatas accessibles through the share
share_search = isogeo.search(
    share=share_augmented.get("_id"),  # filter on the share
    whole_results=1  # retrieve the whole application scope
)
# check if the metadata is in the result
share_mds_ids = [md.get("_id") for md in share_search.results]

if md_id in share_mds_ids:
    print("Metadata is present in this share.")
else:
    print("Not present.")

# properly closing connection
isogeo.close()
```

---

## URL Builder for web applications

All examples in this section must be precede by the following code:

```python

from isogeo_pysdk import IsogeoUtils, Isogeo

utils = IsogeoUtils()
# authenticate your client application
isogeo = Isogeo(
    client_id=app_id,
    client_secret=app_secret,
    auto_refresh_url=isogeo_token_uri
)

# get the token
isogeo.connect()
```

**Isogeo metadata can be displyed in others web applications. Some webapps are built-in:**

* OpenCatalog (oc)
* *Data portal by PixUp (pixup_portal)
* *CSW GetCapabilities (for a share)
* *CSW GetRecords (for a metadata)

It's also possible to register a custom web app (see below).

### Get URL to online editor for a metadata

A metadata can only be edited by an authenticated Isogeo user (with editor level at least). A built-in method make it easy to contruct it:

```python
md = isogeo.metadata.get(md_id="36fde4261bcb4ef2a849d94a50488713")

url = utils.get_edit_url(metadata=md, tab="attributes")
```

### Get OpenCatalog URL for a metadata

```python
oc_args = {
    "md_id": "36fde4261bcb4ef2a849d94a50488713",
    "share_id": "344d51c3edfb435daf9d98d948fa207e",
    "share_token": "TokenOhDearToken"
}

oc_url = utils.get_view_url(webapp="oc", **oc_args)
```

### Get CSW GetCapabilities for a share

```python
csw_getcap_args = {
    "share_id": "344d51c3edfb435daf9d98d948fa207e",
    "share_token": "TokenOhDearToken",
}

csw_getcap_url = utils.get_view_url(webapp="csw_getcap", **csw_getcap_args)
```

### Get CSW GetRecords for a share

```python
csw_getrecords_args = {
    "share_id": "344d51c3edfb435daf9d98d948fa207e",
    "share_token": "TokenOhDearToken",
}

csw_getrecords_url = utils.get_view_url(webapp="csw_getrecords", **csw_getrecords_args)
```

### Get CSW GetRecordById for a metadata

```python
uuid_md_source = "36fde4261bcb4ef2a849d94a50488713"

csw_getrec_args = {
    "md_uuid_urn": utils.convert_uuid(uuid_md_source, 2),
    "share_id": "344d51c3edfb435daf9d98d948fa207e",
    "share_token": "TokenOhDearToken"
}

csw_getrec_url = utils.get_view_url(webapp="csw_getrec", **csw_getrec_args)
```

### Register a custom webapp and get URL

```python
# register the web app
utils.register_webapp(
    webapp_name="PPIGE v3",
    webapp_args=["md_id", ],
    webapp_url="https://www.ppige-npdc.fr/portail/geocatalogue?uuid={md_id}"
)
# get url
custom_url_args = {
    "md_id": "36fde4261bcb4ef2a849d94a50488713",
    "share_id": "344d51c3edfb435daf9d98d948fa207e",
    "share_token": "TokenOhDearToken"
}
custom_url = utils.get_view_url(webapp="PPIGE v3", **custom_url_args)
```

---

## Download metadata as XML ISO 19139

In Isogeo, every metadata resource can be downloaded in its XML version (ISO 19139 compliant). The Python SDK package inclue a shortcut method:

```python

from isogeo_pysdk import Isogeo, Metadata

# authenticate your client application
isogeo = Isogeo(
    client_id=app_id,
    client_secret=app_secret,
    auto_refresh_url=isogeo_token_uri
)

# get the token
isogeo.connect()

# search metadata
search_to_be_exported = isogeo.search(
    page_size=10,
    query="type:dataset",
    whole_results=0
)

# loop on results and export
for md in search_to_be_exported.results:
    metadata = Metadata.clean_attributes(md)
    title = metadata.title
    xml_stream = isogeo.metadata.download_xml(metadata)

    with open("{}.xml".format(title), 'wb') as fd:
        for block in xml_stream.iter_content(1024):
            fd.write(block)

# properly closing connection
isogeo.close()
```

Others examples:

* [Batch export into XML within Isogeo to Office application](https://github.com/isogeo/isogeo-2-office/blob/master/modules/threads.py#L253-L330).
* [Batch export into XML in the package sample](https://github.com/isogeo/isogeo-api-py-minsdk/blob/master/isogeo_pysdk/samples/export_batch_xml19139_sync.py).

---

## Download hosted data from Isogeo cloud

Administrators and editors can link raw data and docs (.zip, .pdf...) to metadata to allow final users to access the data. To do that, it's possible to upload data to Isogeo cloud (Azure blob storage).Through the API, it's possible to download these data:

```python

from isogeo_pysdk import Isogeo

# authenticate your client application
isogeo = Isogeo(
    client_id=app_id,
    client_secret=app_secret,
    auto_refresh_url=isogeo_token_uri
)

# get the token
isogeo.connect()

# search with _include = links and action = download
latest_data_modified = isogeo.search(
    page_size=10,
    order_by="modified",
    whole_results=0,
    query="action:download",
    include=("links",),
)

# parse links and download hosted data recursively
for md in latest_data_modified.results:
    for link in filter(lambda x: x.get("type") == "hosted", md.get("links")):
        dl_stream = isogeo.metadata.links.download_hosted(link=link)
        filename = re.sub(r'[\\/*?:"<>|]', "", dl_stream[1])
        with open(dl_stream[1], "wb") as fd:
            for block in dl_stream[0].iter_content(1024):
                fd.write(block)

# properly closing connection
isogeo.close()
```

Example:

* [Batch export hosted data in the package sample](https://github.com/isogeo/isogeo-api-py-minsdk/blob/master/isogeo_pysdk/samples/download_batch_hosted_data.py).

---
