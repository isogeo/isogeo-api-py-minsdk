# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# -----------------------------------------------------------------------------
# Name:         Isogeo oAuth2 User Web Client
# Purpose:      
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      22/04/2017
# Updated:      10/02/2018
# -----------------------------------------------------------------------------

# INSPIRED FROM: https://github.com/requests/requests-oauthlib/blob/master/docs/examples/real_world_example_with_refresh.rst

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from configparser import RawConfigParser
import logging
import os
from pprint import pformat
from time import time

# 3rd party library
import requests
from requests_oauthlib import OAuth2Session

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

# ############################################################################
# ########## Globals #############
# ##################################

# GET SECRET SETTINGS
config = RawConfigParser()
config.read(r"../isogeo_params.ini")
ISOGEO_OAUTH_CLIENT_ID = config.get('auth', 'CLIENT_ID')
ISOGEO_OAUTH_CLIENT_SECRET = config.get('auth', 'CLIENT_SECRET')
ISOGEO_OAUTH_URL_AUTH = config.get('auth', 'URL_AUTH')
ISOGEO_OAUTH_URL_TOKEN = config.get('auth', 'URL_TOKEN')
ISOGEO_OAUTH_URL_TOKEN_REFRESH = ISOGEO_OAUTH_URL_TOKEN

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
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID)
    authorization_url, state = isogeo.authorization_url(ISOGEO_OAUTH_URL_AUTH)

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

    set http://localhost:5000/callback
    """

    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID,
                           state=session['oauth_state'])
    token = isogeo.fetch_token(ISOGEO_OAUTH_URL_TOKEN, client_secret=ISOGEO_OAUTH_CLIENT_SECRET,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /search.
    session['oauth_token'] = token

    # return redirect(url_for('.search'))
    return redirect(url_for('.menu'))


@app.route("/menu", methods=["GET"])
def menu():
    """
        # Step 4: User pick an option
    """
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/search"> Make a raw search</a></li>
        <li><a href="/profile"> View basic metrics</a></li>
        <li><a href="/automatic_refresh"> Implicitly refresh the token</a></li>
        <li><a href="/manual_refresh"> Explicitly refresh the token</a></li>
    </ul>

    <pre>
    %s
    </pre>
    """ % pformat(session['oauth_token'], indent=4)

# SERACH AND PROFILE ----------------------------------------------------------
@app.route("/search", methods=["GET"])
def search():
    """Fetching a protected resource using an OAuth 2 token.
    """
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID, token=session['oauth_token'])
    print(dir(isogeo))
    print(isogeo.access_token, isogeo.scope)
    return jsonify(isogeo.get('https://v1.api.isogeo.com/resources/search?q=format:shp') .json())


@app.route("/profile", methods=["GET"])
def profile():
    """
        Displaying basic metrics about authenticated user
    """
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID, token=session['oauth_token'])
    search = isogeo.get('https://v1.api.isogeo.com/resources/search?_limit=0').json()
    print(search.keys())
    # raw print
    return """
    <h1>isogeo basic metrucs</h1>
    <p>You have access to %s metadata!</p>
    """ % search.get("total")


# TOKEN MANAGEMENT -----------------------------------------------------------
@app.route("/automatic_refresh", methods=["GET"])
def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Isogeo API.
    token['expires_at'] = time() - 10

    extra = {
        'client_id': ISOGEO_OAUTH_CLIENT_ID,
        'client_secret': ISOGEO_OAUTH_CLIENT_SECRET,
    }

    def token_updater(token):
        session['oauth_token'] = token

    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=ISOGEO_OAUTH_URL_TOKEN_REFRESH,
                           token_updater=token_updater)

    # Trigger the automatic refresh
    jsonify(isogeo.get('https://v1.api.isogeo.com/resources/search?q=format:shp') .json())
    return jsonify(session['oauth_token'])


@app.route("/manual_refresh", methods=["GET"])
def manual_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    extra = {
        'client_id': ISOGEO_OAUTH_CLIENT_ID,
        'client_secret': ISOGEO_OAUTH_CLIENT_SECRET,
    }

    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID, token=token)
    session['oauth_token'] = isogeo.refresh_token(ISOGEO_OAUTH_URL_TOKEN_REFRESH, **extra)
    return jsonify(session['oauth_token'])


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
        app.secret_key = ISOGEO_OAUTH_CLIENT_SECRET
        app.run(debug=True)
