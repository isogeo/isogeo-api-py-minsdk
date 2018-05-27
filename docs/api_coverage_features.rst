================================
Isogeo API coverage and features
================================

This page is about the functional coverage between Isogeo API and the Python package.

Authentication
--------------

- [X] group application (oAuth2 Credentials Grant)
- [ ] user confidential application (oAuth2 Authorization Code Grant)
- [ ] user public application (oAuth2 Implicit Grant)
- [X] token auto refresh

Resources search ( GET /resources/search )
------------------------------------------

Resources search parameters:

- [X] q (query)
- [X] ob (order by)
- [X] od (order direction)
- [X] _id (filter on specific resources id list)
- [X] _include (subresources management)
- [X] _lang (French or English with complete translation)
- [X] _limit (results length)
- [X] _offset (pagination)
- [X] box (filter on WGS84 boundging box)
- [X] geo (filter on WKT polygon)
- [X] rel (geometric operation to apply on 2 previous filters)
- [X] s share segregation


Resource details ( GET /resources/{rid} )
-----------------------------------------

Resource detailed parameters:

- [X] id (metadata UUID)
- [X] _include (subresources management)

Others:

- [X] download resource in XML ISO-1939 version
- [ ] resource with contacts subresource included ( GET /resources/{rid}/contacts )
- [ ] resource with events subresource included ( GET /resources/{rid}/events )
- [ ] resource with keywords subresource included ( GET /resources/{rid}/keywords )
- [ ] resource with operations subresource included ( GET /resources/{rid}/operationds - only for services)

Keyword details ( GET /keyword/{kid} )
--------------------------------------

- [X] kid (keyword UUID)
- [X] _include (subresources management)
- [X] searches for keywords in a specific workgroup ( GET /groups/{gid}/keywords/search  )

These requests are not publicly available.

Thesaurus ( GET /thesauri )
---------------------------

- [X] list of available thesauri
- [X] specific thesaurus ( GET /thesauri/tid )
- [X] searches for keywords in a specific thesaurus ( GET /thesauri/{tid}/keywords/search )

Shares  ( GET /shares )
-----------------------

- [X] list accessible shares
- [X] specific share ( GET /shares/sid )

Licenses  ( GET /licenses )
---------------------------

- [X] list licenses of a workgroup
- [X] details on a specific license ( GET /license/lid )

These requests are not publicly available.

Miscellaneous & bonus
---------------------

- [X] check API version
- [X] check database version
- [X] pick between different Isogeo API platform (PROD, QA, [INT])
- [X] set protocol requests to HTTPS (default) or HTTP (only for GET requests not for authentication)
- [X] get every API label automatically translated (not only INSPIRE themes)
- [X] additional search parameter to automatically get full results without have to iterate with _limit and _offset
- [X] option (`ALL`) to quickly get every subresources through _include parameter
- [X] option (`augment`) to dynamically add shares ids to a search results tags (#6)
- [X] option (`tags_as_dict`) to get tags as key/values (#26)
- [X] method to easily download Isogeo hosted data
- [X] method to easily get application properties from shares request
- [X] method to easily get metadata edition URL on https://app.isogeo.com (handle direct tabs) - #23
- [X] method to load credentials from structured files (#25)
- [X] UUID checker and converter (hex <-> urn) to handle specific Isogeo UUID
- [X] automatic check on values passed into query parameter to the API
- [-] handle proxies setting (only for basic auth - not PAC nor NTLM)

