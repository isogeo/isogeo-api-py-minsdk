# Authenticate to the API

## Load API credentials from a JSON or INI file

Isogeo delivers API credentials in a JSON file. Its structure depends on the kind of oAuth2 application you are developing. Please referer to the API documentation to know more about different types of oAuth2 application.

For example, here is the JSON structure for a "workgroup" application:

```json
{
"web": {
    "client_id": "python-minimalist-sdk-test-uuid-1a2b3c4d5e6f7g8h9i0j11k12l",
    "client_secret": "application-secret-1a2b3c4d5e6f7g8h9i0j11k12l13m14n15o16p17Q18rS",
    "auth_uri": "https://id.api.isogeo.com/oauth/authorize",
    "token_uri": "https://id.api.isogeo.com/oauth/token"
    }
}
```

The module isogeo_pysdk.utils comes with a method to load automatically credentials from JSON and INI files:

```python
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
isogeo.connect()
```

Keys of returned dict:

- auth_mode
- client_id
- client_secret
- scopes
- uri_auth
- uri_base
- uri_redirect
- uri_token

## Authenticate using oAuth2 Client Credentials Grant ("group application")

This is the oAuth2 Backend Application flow, used by the named "group application" in Isogeo terms.

Supposing secrets are stored as environment variables:

```python
# for oAuth2 Backend (Client Credentials Grant) Flow
isogeo = Isogeo(
    auth_mode="group",
    client_id=environ.get("ISOGEO_API_GROUP_CLIENT_ID"),
    client_secret=environ.get("ISOGEO_API_GROUP_CLIENT_SECRET"),
    auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
    platform=environ.get("ISOGEO_PLATFORM", "qa"),
    max_retries=1,
)

# getting a token
isogeo.connect()
```
