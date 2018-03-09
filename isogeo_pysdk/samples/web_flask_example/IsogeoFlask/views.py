"""
    Sample Isogeo User Dashboard based on Flask
"""

# Standard library
from configparser import RawConfigParser
from datetime import datetime
from pprint import pformat

# 3rd party library
from flask import render_template, request, redirect, session, url_for
from flask.json import jsonify
from IsogeoFlask import app

from requests_oauthlib import OAuth2Session

# ############################################################################
# ########## Globals ###############
# ##################################

# GET SECRET SETTINGS
config = RawConfigParser()
config.read(r"isogeo_secret.ini")
ISOGEO_OAUTH_CLIENT_ID = config.get('auth', 'CLIENT_ID')
ISOGEO_OAUTH_CLIENT_SECRET = config.get('auth', 'CLIENT_SECRET')
ISOGEO_OAUTH_URL_AUTH = config.get('auth', 'URL_AUTH')
ISOGEO_OAUTH_URL_TOKEN = config.get('auth', 'URL_TOKEN')
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
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
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


# SEARCH AND PROFILE ----------------------------------------------------------
@app.route("/search", methods=["GET"])
def search():
    """Fetching a protected resource using an OAuth 2 token.
    """
    if not session.get("oauth_token"):
        return redirect(url_for('.login'))
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID, token=session['oauth_token'])
    # print(dir(isogeo))
    # print(isogeo.access_token, isogeo.scope)
    return jsonify(isogeo.get('https://v1.api.isogeo.com/resources/search?q=owner:0bccc739602f4c709486a0fd5e034f7b keyword:isogeo:donnees-ouvertes routes') .json())


@app.route("/profile", methods=["GET"])
def profile():
    """
        Displaying basic metrics about authenticated user
    """
    if not session.get("oauth_token"):
        return redirect(url_for('.login'))
    isogeo = OAuth2Session(ISOGEO_OAUTH_CLIENT_ID, token=session['oauth_token'])
    search = isogeo.get('https://v1.api.isogeo.com/resources/search?_limit=0').json()
    ct_workgroups = len([i for i in search.get("tags") if i.startswith("owner:")])
    print(search.keys(), len(search.get("results")))
    # raw print
    return """
    <h1>Isogeo basic metrics</h1>
    <p>You have access to {} metadata in {} workgroups!</p>
    """.format(search.get("total"), ct_workgroups)

