"""
    This script runs the IsogeoFlask application using a development server.
"""

from os import environ, urandom
from IsogeoFlask import app

if __name__ == '__main__':
    environ['DEBUG'] = "1"
    # ONLY IN DEBUG MODE - NO MAINTAIN THIS OPTION IN PRODUCTION #############
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # ########################################################################
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.secret_key = urandom(24)
    app.run(HOST, PORT, debug=True)
