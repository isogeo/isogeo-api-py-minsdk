"""
    Sample Isogeo User Dashboard based on Flask
"""

# Standard library
import json
from datetime import datetime
from pprint import pformat
from random import randint

# 3rd party library
from flask import render_template, request, redirect, session, url_for
from flask.json import jsonify
from IsogeoFlask import app

from requests_oauthlib import OAuth2Session

# ############################################################################
# ########## Globals ###############
# ##################################

# oAuth2 settings from client_secrets.json
with open('client_secrets.json', "r") as j:
    api = json.loads(j.read()).get("installed")

ISOGEO_OAUTH_CLIENT_ID = api.get('client_id')
ISOGEO_OAUTH_CLIENT_SECRET = api.get('client_secret')
ISOGEO_OAUTH_URL_301 = api.get('redirects_uri')
ISOGEO_OAUTH_URL_AUTH = api.get('auth_uri')
ISOGEO_OAUTH_URL_TOKEN = api.get('token_uri')
ISOGEO_OAUTH_URL_TOKEN_REFRESH = ISOGEO_OAUTH_URL_TOKEN

# ############################################################################
# ########## Functions #############
# ##################################


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title="Page d'accueil",
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Contact Isogeo to get your developper credentials'
    )


# AUTHENTICATION ----------------------------------------------------------
@app.route("/login")
def login():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID)
    authorization_url, state = isogeo.authorization_url(ISOGEO_OAUTH_URL_AUTH)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


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
    token = isogeo.fetch_token(ISOGEO_OAUTH_URL_TOKEN,
                               client_secret=ISOGEO_OAUTH_CLIENT_SECRET,
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
    return render_template(
        'menu.html',
        title='Menu utilisateur authentifié',
        year=datetime.now().year,
    )

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


# TOKEN MANAGEMENT -----------------------------------------------------------
@app.route("/automatic_refresh", methods=["GET"])
def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Isogeo API.
    token['expires_at'] = 0

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
    jsonify(isogeo.get('https://v1.api.isogeo.com/resources/search?') .json())
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


# SEARCH AND PROFILE ----------------------------------------------------------
@app.route("/search", methods=["GET"])
def search():
    """Fetching a protected resource using an OAuth 2 token.
    """
    if not session.get("oauth_token"):
        return redirect(url_for('.login'))
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID, token=session['oauth_token'])
    return jsonify(isogeo.get("https://v1.api.isogeo.com/resources/search?"
                              "_limit=10"
                              "&_include=conditions,contacts,coordinate-system,feature-attributes,layers") .json())


@app.route("/profile", methods=["GET"])
def profile():
    """
        Displaying basic metrics about authenticated user
    """
    if not session.get("oauth_token"):
        return redirect(url_for('.login'))
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID, token=session['oauth_token'])
    search = isogeo.get('https://v1.api.isogeo.com/resources/search?lang=FR&_limit=100').json()

    # some calculations
    ct_tags = len(search.get("tags"))
    ct_workgroups = len([i for i in search.get("tags")
                         if i.startswith("owner:")])
    ct_catalogs = len([i for i in search.get("tags")
                       if i.startswith("catalog:")])
    # random metadata
    ct_rez = len(search.get("results", ["No results"]))
    a, b = randint(0, ct_rez), randint(0, ct_rez)
    md1, md2 = search.get("results")[a], search.get("results")[b]
    mds = {"md1": [md1.get("title"), md1.get("abstract", "Pas de résumé")],
           "md2": [md2.get("title"), md2.get("abstract", "Pas de résumé")], }

    # pie chart
    stats_types = [isogeo.get('https://v1.api.isogeo.com/resources/search?_limit=0&q=type:vector-dataset').json().get("total", 0),
                   isogeo.get('https://v1.api.isogeo.com/resources/search?_limit=0&q=type:raster-dataset').json().get("total", 0),
                   isogeo.get('https://v1.api.isogeo.com/resources/search?_limit=0&q=type:service').json().get("total", 0),
                   isogeo.get('https://v1.api.isogeo.com/resources/search?_limit=0&q=type:resource').json().get("total", 0),
                   ]

    # NOT USED
    # # line chart
    # stats_creation = [md.get("_created") for md in search.get("results")]

    # to display
    return render_template(
        'metrics.html',
        title='Métriques utilisateur',
        year=datetime.now().year,
        ct_mds=search.get("total"),
        ct_wgs=ct_workgroups,
        ct_cats=ct_catalogs,
        ct_tags=ct_tags,
        ct_rez=ct_rez,
        mds=mds,
        stats_types=stats_types,
    )
