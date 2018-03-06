# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# -----------------------------------------------------------------------------
# Name:         UData Python Client
# Purpose:      Abstraction class to manipulate data.gouv.fr API
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      22/04/2017
# Updated:      10/06/2017
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import os

# 3rd party library
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

# ############################################################################
# ########## Globals #############
# ##################################

client_id = 
client_secret = 
url_auth = "https://id.api.isogeo.com/oauth/authorize"
url_token = "https://id.api.isogeo.com/oauth/token"

# ############################################################################
# ########## Functions #############
# ##################################

app = Flask(__name__)


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    isogeo = OAuth2Session(client_id)
    authorization_url, state = isogeo.authorization_url(url_auth)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    isogeo = OAuth2Session(client_id, state=session['oauth_state'])
    token = isogeo.fetch_token(url_token, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    isogeo = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(isogeo.get('http://v1.api.isogeo.com/resources/search?').json())


# ##############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == '__main__':
    # this disable HTTPS requirement : SHOULD NOT BE USED IN PRODUCTION
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    if __name__ == "__main__":
        # This allows us to use a plain HTTP callback
        os.environ['DEBUG'] = "1"

        # app.secret_key = os.urandom(24)
        app.secret_key = client_secret
        app.run(debug=True)
